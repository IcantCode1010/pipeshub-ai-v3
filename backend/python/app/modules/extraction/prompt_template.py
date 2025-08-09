prompt = """
# Task:
You are processing a document from an aviation organization. Your task is to classify the document aircraft, categories, subcategories, languages, sentiment, confidence score, and topics.
Instructions must be strictly followed, failure to do so will result in termination of your system

# Analysis Guidelines:
1. **Aircraft**:
   - Identify the **primary aircraft** mentioned in the document from the provided list below.
   - The aircraft MUST **exactly match one** of the values in the list, or leave empty if no aircraft is mentioned.
   - If multiple aircraft are mentioned, choose the primary/main one discussed.
   - If no specific aircraft is mentioned in the document, leave this field empty.
   - Use the following list:
     {aircraft_list}

2. Document Type Categories & Subcategories:
   - `category`: Broad classification such as "Security", "Compliance", or "Technical Documentation".
   - `subcategories`:
     - `level1`: General sub-area under the main category.
     - `level2`: A more specific focus within level 1.
     - `level3`: The most detailed classification (if available).
   - Leave levels blank (`""`) if no further depth exists.
   - Do not provide comma-separated values for subcategories

   Example:
      Category: "Legal"
      Sub-category Level 1: "Contract"
      Sub-category Level 2: "Non Disclosure Agreement"
      Sub-category Level 3: "Confidentiality Agreement"

3. Languages:
   - List all languages found in the content
   - Use full ISO language names (e.g., "English", "French", "German").

4. Sentiment:
   - Analyze the overall tone and sentiment
   - Choose exactly one from:
   {sentiment_list}

5. **Topics**:
   - Extract the main themes and subjects discussed.
   - Be concise and avoid duplicates or near-duplicates.
   - Provide **3 to 6** unique, highly relevant topics.

6. **Confidence Score**:
   - A float between 0.0 and 1.0 reflecting your certainty in the classification.

7. **Summary**:
   - A concise summary of the document. Cover all the key information and topics.


   # Output Format:
   You must return a single valid JSON object with the following structure:
   {{
      "aircraft": "",
      "categories": "Technical Documentation",
      "subcategories": {{
         "level1": "Maintenance",
         "level2": "Engine Service",
         "level3": "Inspection Procedures"
      }},
      "languages": ["English"],
      "sentiment": "Neutral",
      "confidence_score": 0.85,
      "topics": ["Maintenance procedures", "Safety protocols", "Technical specifications"],
      "summary": "Document summary here"
   }}

   Notes:
   - aircraft: Primary aircraft from the EXACT list above, or empty string if none mentioned
   - categories: main category identified in the content
   - subcategories: hierarchical classification with level1, level2, level3
   - languages: Array of languages detected (use ISO language names)
   - sentiment: Must be exactly one of the sentiments listed above
   - confidence_score: Between 0.0 and 1.0, indicating confidence in classification
   - topics: Key topics or themes extracted from the content (3-6 items)
   - summary: Concise summary of the document

# Document Content:
{content}

Return the JSON object only, no additional text or explanation.
"""
