from abc import ABC, abstractmethod
from typing import Any, Dict

import fitz

from app.config.utils.named_constants.ai_models_named_constants import OCRProvider


class OCRStrategy(ABC):
    """Abstract base class for OCR strategies"""

    def __init__(self, logger):
        self.logger = logger

    @abstractmethod
    async def process_page(self, page) -> Dict[str, Any]:
        """Process a single page with OCR"""
        pass

    @abstractmethod
    async def load_document(self, content: bytes) -> None:
        """Load document content"""
        pass

    @abstractmethod
    async def extract_text(self) -> Dict[str, Any]:
        """Extract text and layout information"""
        pass

    def needs_ocr(self, page) -> bool:
        """Determine if a page needs OCR processing"""
        try:
            self.logger.debug("🔍 Checking if page needs OCR")

            # Get page metrics with error handling for corrupted PDFs
            try:
                text = page.get_text().strip()
                words = page.get_text("words")
                images = page.get_images()
                page_area = page.rect.width * page.rect.height
            except Exception as parse_error:
                self.logger.error(f"❌ PDF parsing error (corrupted PDF detected): {str(parse_error)}")
                self.logger.info("⚠️ Skipping OCR due to corrupted PDF structure")
                return False

            # Log detailed image information
            significant_images = 0
            MIN_IMAGE_WIDTH = 500  # Minimum width in pixels for a significant image
            MIN_IMAGE_HEIGHT = 500  # Minimum height in pixels for a significant image

            for img_index, img in enumerate(images):
                # img tuple contains: (xref, smask, width, height, bpc, colorspace, ...)
                width, height = img[2], img[3]

                self.logger.debug(f"📸 Image {img_index + 1}:")
                self.logger.debug(f"    Width: {width}, Height: {height}")
                self.logger.debug(f"    Bits per component: {img[4]}")
                self.logger.debug(f"    Colorspace: {img[5]}")
                self.logger.debug(f"    XRef: {img[0]}")

                # Consider an image significant if it's larger than our minimum dimensions
                if width > MIN_IMAGE_WIDTH and height > MIN_IMAGE_HEIGHT:
                    significant_images += 1

            # Multiple criteria for OCR need
            has_minimal_text = len(text) < 100  # Less than 100 characters
            has_significant_images = (
                significant_images > 2
            )  # Contains substantial images
            text_density = (
                sum((w[2] - w[0]) * (w[3] - w[1]) for w in words) / page_area
                if words
                else 0
            )
            low_density = text_density < 0.01

            self.logger.debug(
                f"📊 OCR metrics - Text length: {len(text)}, "
                f"Significant images: {significant_images}, "
                f"Text density: {text_density:.4f}"
            )

            # Extract and save images
            for img_index, img in enumerate(images):
                xref = img[0]
                try:
                    # Create pixmap from image
                    pix = fitz.Pixmap(page.parent, xref)
                    if pix.n - pix.alpha > 3:  # CMYK: convert to RGB
                        pix = fitz.Pixmap(fitz.csRGB, pix)

                    self.logger.debug(
                        f"📸 Image {img_index + 1} pixel format: {pix.n} channels"
                    )
                    # Optionally save the image:
                    # pix.save(f"image_{img_index + 1}_{uuid4()}.png")

                    pix = None  # Free memory
                except Exception as e:
                    self.logger.error(
                        f"""❌ Error processing image {
                                 img_index + 1}: {str(e)}"""
                    )

            needs_ocr = (has_minimal_text and has_significant_images) or low_density
            self.logger.debug(f"🔍 OCR need determination: {needs_ocr}")
            return needs_ocr

        except Exception as e:
            self.logger.error(f"❌ Error checking OCR need: {str(e)}")
            return True


class OCRHandler:
    """Factory and facade for OCR processing"""

    def __init__(self, logger, strategy_type: str, **kwargs):
        """
        Initialize OCR handler with specified strategy

        Args:
            strategy_type: Type of OCR strategy ("pymupdf" or "azure")
            **kwargs: Strategy-specific configuration parameters
        """
        self.logger = logger
        self.logger.info("🛠️ Initializing OCR handler with strategy: %s", strategy_type)
        self.strategy = self._create_strategy(strategy_type, **kwargs)

    def _create_strategy(self, strategy_type: str, **kwargs) -> OCRStrategy:
        """Factory method to create appropriate OCR strategy"""
        self.logger.debug(f"🏭 Creating OCR strategy: {strategy_type}")

        if strategy_type == OCRProvider.OCRMYPDF.value:
            self.logger.debug("📚 Creating OCRMYPDF OCR strategy")
            from app.modules.parsers.pdf.pymupdf_ocrmypdf_processor import (
                PyMuPDFOCRStrategy,
            )

            return PyMuPDFOCRStrategy(
                logger=self.logger, language=kwargs.get("language", "eng")
            )
        elif strategy_type == OCRProvider.AZURE_DI.value:
            self.logger.debug("☁️ Creating Azure OCR strategy")
            from app.modules.parsers.pdf.azure_document_intelligence_processor import (
                AzureOCRStrategy,
            )

            return AzureOCRStrategy(
                logger=self.logger,
                endpoint=kwargs["endpoint"],
                key=kwargs["key"],
                model_id=kwargs.get("model_id", "prebuilt-document"),
            )
        else:
            self.logger.error(f"❌ Unsupported OCR strategy: {strategy_type}")
            raise ValueError(f"Unsupported OCR strategy: {strategy_type}")

    def _is_pdf_corrupted(self, content: bytes) -> bool:
        """
        Intelligent PDF corruption detection that checks file structure integrity
        
        Args:
            content: PDF document content as bytes
            
        Returns:
            bool: True if PDF appears corrupted, False otherwise
        """
        try:
            # Check PDF header
            if not content.startswith(b'%PDF-'):
                self.logger.debug("❌ Invalid PDF header")
                return True
            
            # Check for PDF trailer
            if b'%%EOF' not in content[-1024:]:
                self.logger.debug("❌ Missing PDF trailer")
                return True
            
            # Convert first 100KB to string for pattern matching (safely)
            content_sample = content[:100000].decode('latin-1', errors='ignore')
            
            # Check for essential PDF structure elements
            required_elements = ['obj', 'endobj', 'stream', 'endstream']
            missing_elements = [elem for elem in required_elements if elem not in content_sample]
            if missing_elements:
                self.logger.debug(f"❌ Missing PDF elements: {missing_elements}")
                return True
            
            # Look for specific corruption patterns that actually cause MuPDF syntax errors
            import re
            
            # Specific corruption patterns found in real corrupted PDFs
            specific_corruption_patterns = [
                # Malformed coordinate sequences (multiple decimals without operators)
                r'\d+\.\d+\.\d+\.\d+',           # '0685.5.64.123' - too many decimals
                # Malformed operator sequences with invalid characters  
                r'\d{4,}[lPRST]{2,}\d*',         # '1234RR45' - multiple invalid operators
                r'\.[0-9]{4,}[lPRST]\d+\.',      # '.1234R56.' - malformed pattern
                # Invalid number sequences that break parsing
                r'\d{6,}[lPRST]\d{6,}',          # Very long number sequences with invalid ops
                # New patterns based on the error logs
                r'\d+l',                          # '178l' - number followed by 'l' operator
                r'\d{10,}S\d+',                   # '8748500188S4' - long number with S operator
                r'\.\d+\.l',                      # '.84.l' - decimal with 'l' operator
                r'\d+\.S\d+',                     # '785.S3' - decimal with S in middle
            ]
            
            corruption_count = 0
            for pattern in specific_corruption_patterns:
                matches = re.findall(pattern, content_sample)
                if matches:
                    corruption_count += len(matches)
                    self.logger.debug(f"🔍 Found {len(matches)} instances of pattern: {pattern}")
                    # Log first few matches for debugging
                    for match in matches[:3]:
                        self.logger.debug(f"   Example match: '{match}'")
            
            # Only consider corrupted if we find multiple instances of corruption patterns
            # Lowered threshold to catch more corrupted files
            if corruption_count > 3:
                self.logger.warning(f"🚨 PDF appears corrupted - found {corruption_count} corruption patterns")
                return True
            
            # Additional check: try to validate basic PDF structure with PyMuPDF
            # This will catch MuPDF syntax errors
            try:
                import fitz
                # Try to open the entire document to catch syntax errors
                test_doc = fitz.open(stream=content, filetype="pdf")
                # Try to access first page to trigger parsing
                if len(test_doc) > 0:
                    _ = test_doc[0].get_text()
                test_doc.close()
                self.logger.debug("✅ PDF structure validation passed")
                return False
            except Exception as validation_error:
                error_msg = str(validation_error).lower()
                # Check for specific MuPDF syntax errors
                if 'syntax error' in error_msg or 'unknown keyword' in error_msg:
                    self.logger.warning(f"🚨 MuPDF syntax error detected: {validation_error}")
                    return True
                # Other errors might not indicate corruption
                self.logger.debug(f"⚠️ PyMuPDF validation warning: {validation_error}")
                return False
            
        except Exception as e:
            self.logger.error(f"❌ Error checking PDF corruption: {str(e)}")
            return False  # Default to not corrupted if we can't check properly

    async def _fallback_simple_extraction(self, content: bytes) -> Dict[str, Any]:
        """
        Fallback method using simple PyMuPDF text extraction without OCR
        
        Args:
            content: PDF document content as bytes
            
        Returns:
            Dict containing basic extracted text and minimal layout information
        """
        self.logger.info("🔄 Using fallback simple extraction method")
        
        try:
            import fitz
            doc = fitz.open(stream=content, filetype="pdf")
            
            result = {
                "pages": [],
                "paragraphs": [],
                "sentences": [],
                "lines": [],
                "tables": [],
                "key_value_pairs": []
            }
            
            for page_idx in range(len(doc)):
                page = doc[page_idx]
                page_width = page.rect.width
                page_height = page.rect.height
                
                # Extract simple text
                text = page.get_text()
                words = page.get_text("words")
                
                # Create basic page structure
                page_dict = {
                    "page_number": page_idx + 1,
                    "width": page_width,
                    "height": page_height,
                    "unit": "pt",
                    "lines": [],
                    "words": [],
                    "tables": [],
                }
                
                # Process words
                for word in words:
                    if len(word) >= 5:
                        x0, y0, x1, y1, word_text = word[:5]
                        if word_text.strip():
                            word_dict = {
                                "content": word_text.strip(),
                                "bounding_box": [
                                    {"x": x0 / page_width, "y": y0 / page_height},
                                    {"x": x1 / page_width, "y": y0 / page_height},
                                    {"x": x1 / page_width, "y": y1 / page_height},
                                    {"x": x0 / page_width, "y": y1 / page_height},
                                ],
                                "confidence": None
                            }
                            page_dict["words"].append(word_dict)
                
                # Create basic paragraphs from text blocks
                text_blocks = page.get_text("dict").get("blocks", [])
                for block_idx, block in enumerate(text_blocks):
                    if block.get("type") == 0:  # Text block
                        block_text = ""
                        for line in block.get("lines", []):
                            line_text = " ".join(span.get("text", "") for span in line.get("spans", []))
                            if line_text.strip():
                                block_text += line_text.strip() + " "
                        
                        if block_text.strip():
                            paragraph = {
                                "content": block_text.strip(),
                                "page_number": page_idx + 1,
                                "block_number": block_idx,
                                "bounding_box": [
                                    {"x": block["bbox"][0] / page_width, "y": block["bbox"][1] / page_height},
                                    {"x": block["bbox"][2] / page_width, "y": block["bbox"][1] / page_height},
                                    {"x": block["bbox"][2] / page_width, "y": block["bbox"][3] / page_height},
                                    {"x": block["bbox"][0] / page_width, "y": block["bbox"][3] / page_height},
                                ],
                                "spans": [],
                                "words": [],
                                "metadata": {"font": None, "size": None, "color": None}
                            }
                            result["paragraphs"].append(paragraph)
                            
                            # Create simple sentences by splitting on periods
                            sentences = [s.strip() + "." for s in paragraph["content"].split(".") if s.strip()]
                            for sent_text in sentences:
                                sentence = {
                                    "content": sent_text,
                                    "page_number": page_idx + 1,
                                    "block_number": block_idx,
                                    "bounding_box": paragraph["bounding_box"],
                                    "block_text": paragraph["content"],
                                    "block_type": 0,
                                    "metadata": paragraph["metadata"]
                                }
                                result["sentences"].append(sentence)
                
                result["pages"].append(page_dict)
            
            doc.close()
            self.logger.info("✅ Fallback extraction completed successfully")
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Fallback extraction failed: {str(e)}")
            raise

    async def process_document(self, content: bytes) -> Dict[str, Any]:
        """
        Process document using the configured OCR strategy with fallback
        
        Args:
            content: PDF document content as bytes

        Returns:
            Dict containing extracted text and layout information
        """
        self.logger.info("🚀 Starting document processing")
        
        # Check for PDF corruption before processing
        if self._is_pdf_corrupted(content):
            self.logger.warning("⚠️ PDF appears corrupted - attempting fallback extraction")
            try:
                return await self._fallback_simple_extraction(content)
            except Exception as fallback_error:
                self.logger.error(f"❌ Fallback extraction also failed: {str(fallback_error)}")
                raise ValueError("PDF document is corrupted and cannot be processed with any method")
        
        try:
            self.logger.debug("📥 Loading document with primary strategy")
            await self.strategy.load_document(content)

            self.logger.debug("📊 Extracting text and layout with primary strategy")
            result = await self.strategy.extract_text()

            self.logger.info("✅ Document processing completed successfully with primary strategy")
            return result
            
        except Exception as e:
            self.logger.warning(f"⚠️ Primary strategy failed: {str(e)}")
            self.logger.info("🔄 Attempting fallback simple extraction")
            
            try:
                return await self._fallback_simple_extraction(content)
            except Exception as fallback_error:
                self.logger.error(f"❌ Both primary and fallback strategies failed")
                self.logger.error(f"Primary error: {str(e)}")
                self.logger.error(f"Fallback error: {str(fallback_error)}")
                raise ValueError(f"PDF processing failed with both primary and fallback methods: {str(e)}")
