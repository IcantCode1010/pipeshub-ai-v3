import json
import re
from typing import Any, AsyncGenerator, Dict, Union

from app.modules.qna.prompt_templates import AnswerWithMetadata
from app.utils.citations import normalize_citations_and_chunks


def find_unescaped_quote(text: str) -> int:
    """Return index of first un-escaped quote (") or -1 if none."""
    escaped = False
    for i, ch in enumerate(text):
        if escaped:
            escaped = False
        elif ch == '\\':
            escaped = True
        elif ch == '"':
            return i
    return -1


def escape_ctl(raw: str) -> str:
    """Replace literal \n, \r, \t that appear *inside* quoted strings with their escaped forms."""
    string_re = re.compile(r'"(?:[^"\\]|\\.)*"')   # match any JSON string literal

    def fix(match: re.Match) -> str:
        s = match.group(0)
        return (
            s.replace("\n", "\\n")
              .replace("\r", "\\r")
              .replace("\t", "\\t")
        )
    return string_re.sub(fix, raw)


async def aiter_llm_stream(llm, messages) -> AsyncGenerator[str, None]:
    """Async iterator for LLM streaming"""
    if hasattr(llm, "astream"):
        try:
            async for part in llm.astream(messages):
                if part:
                    # Handle different response formats from various LLM providers
                    content = None
                    if hasattr(part, "content") and part.content:
                        content = part.content
                    elif isinstance(part, dict) and "content" in part:
                        content = part["content"]
                    elif isinstance(part, str):
                        content = part
                    
                    if content:
                        yield content
        except Exception as e:
            # Fallback to non-streaming if streaming fails
            print(f"Streaming failed, falling back to non-streaming: {e}")
            response = await llm.ainvoke(messages)
            yield getattr(response, "content", str(response))
    else:
        # Non-streaming – yield whole blob once
        response = await llm.ainvoke(messages)
        yield getattr(response, "content", str(response))


async def stream_llm_response(
    llm,
    messages,
    final_results,
    target_words_per_chunk: int = 5,
) -> AsyncGenerator[Dict[str, Any], None]:
    """
    Incrementally stream the answer portion of an LLM JSON response.
    For each chunk we also emit the citations visible so far.
    """
    full_json_buf: str = ""         # whole JSON as it trickles in
    answer_buf: str = ""            # the running "answer" value (no quotes)
    answer_done = False
    ANSWER_KEY_RE = re.compile(r'"answer"\s*:\s*"')
    CITE_BLOCK_RE = re.compile(r'(?:\s*\[\d+])+')
    INCOMPLETE_CITE_RE = re.compile(r'\[[^\]]*$')

    WORD_ITER = re.compile(r'\S+').finditer
    prev_norm_len = 0  # length of the previous normalised answer
    emit_upto = 0
    words_in_chunk = 0
    # Check if the LLM supports structured output
    supports_structured_output = False
    try:
        # Only use structured output if the LLM explicitly supports it
        if hasattr(llm, "with_structured_output"):
            test_llm = llm.with_structured_output(AnswerWithMetadata)
            supports_structured_output = True
    except (NotImplementedError, AttributeError) as e:
        print(f"LLM provider does not support structured output: {e}")
        supports_structured_output = False

    try:
        async for token in aiter_llm_stream(llm, messages):
            full_json_buf += token

            if not answer_buf:
                match = ANSWER_KEY_RE.search(full_json_buf)
                if match:
                    after_key = full_json_buf[match.end():]
                    answer_buf += after_key

            elif not answer_done:
                answer_buf += token

            if not answer_done:
                end_idx = find_unescaped_quote(answer_buf)
                if end_idx != -1:
                    answer_done = True
                    answer_buf = answer_buf[:end_idx]

            if answer_buf:
                for match in WORD_ITER(answer_buf[emit_upto:]):
                    words_in_chunk += 1
                    if words_in_chunk == target_words_per_chunk:
                        char_end = emit_upto + match.end()

                        if m := CITE_BLOCK_RE.match(answer_buf[char_end:]):
                            char_end += m.end()

                        emit_upto = char_end
                        words_in_chunk = 0

                        current_raw = answer_buf[:emit_upto]
                        if INCOMPLETE_CITE_RE.search(current_raw):
                            continue

                        normalized, cites = normalize_citations_and_chunks(
                            current_raw, final_results
                        )

                        chunk_text = normalized[prev_norm_len:]
                        prev_norm_len = len(normalized)

                        yield {
                            "event": "answer_chunk",
                            "data": {
                                "chunk": chunk_text,
                                "accumulated": normalized,
                                "citations": cites,
                            },
                        }

        # Try to parse as JSON first, then fallback to plain text
        parsed_data = None
        final_answer = answer_buf
        
        # Attempt JSON parsing if we have what looks like JSON
        if full_json_buf.strip().startswith('{'):
            try:
                parsed_data = json.loads(escape_ctl(full_json_buf))
                final_answer = parsed_data.get("answer", answer_buf)
            except Exception:
                # JSON parsing failed, use accumulated answer buffer
                pass
        
        # If we didn't get any answer content, use the full buffer as plain text
        if not final_answer and full_json_buf:
            final_answer = full_json_buf.strip()
            
        normalized, c = normalize_citations_and_chunks(final_answer, final_results)
        
        yield {
            "event": "complete",
            "data": {
                "answer": normalized,
                "citations": c,
                "reason": parsed_data.get("reason") if parsed_data else None,
                "confidence": parsed_data.get("confidence") if parsed_data else None,
            },
        }

    except Exception as exc:
        yield {
            "event": "error",
            "data": {"error": f"Error in LLM streaming: {exc}"},
        }


def create_sse_event(event_type: str, data: Union[str, dict, list]) -> str:
    """Create Server-Sent Event format"""
    return f"event: {event_type}\ndata: {json.dumps(data)}\n\n"
