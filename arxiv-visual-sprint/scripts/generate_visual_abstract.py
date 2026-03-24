#!/usr/bin/env python3
"""
Visual Abstract 生成核心脚本
"""

import argparse
import base64
import json
import os
import sys
import time
from pathlib import Path
from typing import Optional

import requests
from pypdf import PdfReader


def _log(message: str, verbose: bool = True):
    if verbose:
        print(message, flush=True)


def _resolve_model_name(api_base: str) -> str:
    explicit_model = os.environ.get("GEMINI_MODEL")
    if explicit_model:
        return explicit_model
    if api_base and "cherryin" in api_base.lower():
        return "google/gemini-3.1-flash-image-preview"
    return "gemini-3.1-flash-image-preview"


def _resolve_endpoint(api_base: Optional[str], model_name: str) -> str:
    if api_base:
        return f"{api_base.rstrip('/')}/v1beta/models/{model_name}:generateContent"
    return f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"


def _resolve_sse_endpoint(api_base: Optional[str], model_name: str) -> str:
    if api_base:
        return f"{api_base.rstrip('/')}/v1beta/models/{model_name}:streamGenerateContent?alt=sse"
    return f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:streamGenerateContent?alt=sse"


def _build_headers(api_key: str, api_base: Optional[str]) -> dict:
    headers = {"Content-Type": "application/json"}
    if api_base and "generativelanguage.googleapis.com" in api_base:
        headers["x-goog-api-key"] = api_key
    elif api_base:
        headers["Authorization"] = f"Bearer {api_key}"
    else:
        headers["x-goog-api-key"] = api_key
    return headers


def _extract_image_bytes(payload: dict) -> Optional[bytes]:
    candidates = payload.get("candidates") or []
    for candidate in candidates:
        content = candidate.get("content") or {}
        parts = content.get("parts") or []
        for part in parts:
            inline_data = part.get("inline_data") or part.get("inlineData")
            if inline_data and inline_data.get("data"):
                return base64.b64decode(inline_data["data"])
    return None


def _extract_pdf_text(pdf_path: str, max_pages: int, verbose: bool) -> str:
    _log(f"📄 开始解析 PDF: {pdf_path}", verbose)
    reader = PdfReader(pdf_path)
    pages = reader.pages[:max_pages]
    chunks = []
    for idx, page in enumerate(pages, start=1):
        text = page.extract_text() or ""
        _log(f"  - 第 {idx} 页提取字符数: {len(text)}", verbose)
        chunks.append(f"[Page {idx}]\n{text}")
    merged = "\n\n".join(chunks).strip()
    _log(f"✅ PDF 解析完成，总字符数: {len(merged)}", verbose)
    return merged


def _build_prompt(
    title: Optional[str],
    problem: Optional[str],
    contributions: Optional[str],
    method: Optional[str],
    pdf_text: Optional[str],
) -> str:
    if pdf_text:
        return f"""
Create a professional academic Visual Abstract from the extracted paper text.

PAPER TITLE: {title or "Unknown"}
EXTRACTED CONTENT (first pages):
{pdf_text[:14000]}

SPEC:
- Style: Professional academic infographic.
- Color: Academic Blue (#1565c0).
- Layout: clear title area, middle key contributions, bottom method cues.
- Format: High-quality PNG, 3:2 aspect ratio.
"""
    return f"""
Create a professional academic Visual Abstract.

TITLE: {title}
PROBLEM: {problem}
CONTRIBUTIONS: {contributions}
METHOD: {method}

SPEC:
- Style: Professional academic infographic.
- Color: Academic Blue (#1565c0).
- Format: High-quality PNG, 3:2 aspect ratio.
"""


def generate(
    title,
    problem,
    contributions,
    method,
    output_path,
    pdf_path: Optional[str] = None,
    pdf_pages: int = 5,
    retries: int = 2,
    timeout_seconds: int = 180,
    verbose: bool = True,
    smoke: bool = False,
    use_sse: bool = True,
):
    api_key = os.environ.get("GEMINI_API_KEY")
    api_base = os.environ.get("GEMINI_API_BASE")

    if not api_key:
        print(
            "❌ Error: GEMINI_API_KEY not found. 请先设置 GEMINI_API_KEY 环境变量。",
            flush=True,
        )
        return False
    _log("🔧 环境变量检查通过。", verbose)
    _log(f"   - GEMINI_API_BASE: {api_base or '(default)'}", verbose)
    model_name = _resolve_model_name(api_base)
    _log(f"   - MODEL: {model_name}", verbose)
    endpoint = (
        _resolve_sse_endpoint(api_base, model_name)
        if use_sse
        else _resolve_endpoint(api_base, model_name)
    )
    headers = _build_headers(api_key, api_base)
    _log(f"   - ENDPOINT: {endpoint}", verbose)

    pdf_text = None
    if pdf_path and not smoke:
        if not Path(pdf_path).exists():
            print(f"❌ Error: PDF 文件不存在: {pdf_path}", flush=True)
            return False
        try:
            pdf_text = _extract_pdf_text(pdf_path, pdf_pages, verbose)
        except Exception as e:
            print(f"❌ Error: PDF 解析失败: {e}", flush=True)
            return False

    if smoke:
        prompt = "Create a simple icon of a blue robot head on white background."
    else:
        prompt = _build_prompt(title, problem, contributions, method, pdf_text)
    _log(f"🧠 Prompt 长度: {len(prompt)} 字符", verbose)
    mode = "SSE" if use_sse else "JSON"
    _log(f"🎨 开始请求 {model_name} 生成图片（requests 直连, {mode}）...", verbose)

    last_error = None
    for attempt in range(1, retries + 2):
        _log(f"⏱️ 第 {attempt}/{retries + 1} 次调用开始", verbose)
        started = time.time()
        try:
            body = {
                "contents": [{"role": "user", "parts": [{"text": prompt}]}],
                "generationConfig": {
                    "responseModalities": ["IMAGE"],
                    "imageConfig": {"aspectRatio": "3:2", "imageSize": "1K"},
                },
            }
            response = requests.post(
                endpoint,
                headers=headers,
                data=json.dumps(body),
                timeout=(15, timeout_seconds),
                stream=use_sse,
            )
            elapsed = time.time() - started
            _log(
                f"📡 HTTP {response.status_code}，用时 {elapsed:.2f}s，content-type={response.headers.get('Content-Type')}",
                verbose,
            )
            if response.status_code >= 400:
                last_error = f"HTTP {response.status_code}: {response.text[:1200]}"
                _log(f"❌ 请求失败响应: {response.text[:1200]}", verbose)
                raise RuntimeError(last_error)

            payload = None
            image_bytes = None
            if use_sse:
                for line in response.iter_lines(decode_unicode=True):
                    if not line:
                        continue
                    if not line.startswith("data:"):
                        continue
                    data = line[5:].strip()
                    if data == "[DONE]":
                        break
                    try:
                        chunk = json.loads(data)
                    except Exception:
                        _log(f"⚠️ SSE 非JSON片段: {data[:200]}", verbose)
                        continue
                    payload = chunk
                    image_bytes = _extract_image_bytes(chunk)
                    if image_bytes:
                        break
            else:
                payload = response.json()
                image_bytes = _extract_image_bytes(payload)

            if image_bytes:
                output_file = Path(output_path).resolve()
                output_file.parent.mkdir(parents=True, exist_ok=True)
                with open(output_file, "wb") as f:
                    f.write(image_bytes)
                _log(f"✅ Saved: {output_file} ({len(image_bytes)} bytes)", verbose)
                print(f"📁 输出文件: {output_file}", flush=True)
                return True

            payload_preview = json.dumps(payload or {}, ensure_ascii=False)[:1200]
            _log(f"⚠️ 响应里没有图片数据，payload预览: {payload_preview}", verbose)
            last_error = "No image data in response payload."
        except Exception as e:
            elapsed = time.time() - started
            last_error = str(e)
            _log(f"❌ 第 {attempt} 次调用失败，用时 {elapsed:.2f}s，错误: {e}", verbose)
        if attempt <= retries:
            wait_s = min(2 * attempt, 8)
            _log(f"🔁 {wait_s}s 后重试...", verbose)
            time.sleep(wait_s)
    print(f"❌ Failed: {last_error}", flush=True)
    return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--title")
    parser.add_argument("--problem")
    parser.add_argument("--contributions")
    parser.add_argument("--method")
    parser.add_argument("--pdf")
    parser.add_argument("--pdf-pages", type=int, default=5)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--timeout-seconds", type=int, default=180)
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--no-sse", action="store_true")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    has_structured_fields = all(
        [args.title, args.problem, args.contributions, args.method]
    )
    if not args.smoke and not args.pdf and not has_structured_fields:
        print(
            "❌ Error: 请提供 --pdf，或同时提供 --title --problem --contributions --method。",
            flush=True,
        )
        sys.exit(1)

    if not generate(
        args.title,
        args.problem,
        args.contributions,
        args.method,
        args.output,
        pdf_path=args.pdf,
        pdf_pages=args.pdf_pages,
        retries=args.retries,
        timeout_seconds=args.timeout_seconds,
        verbose=not args.quiet,
        smoke=args.smoke,
        use_sse=not args.no_sse,
    ):
        sys.exit(1)
