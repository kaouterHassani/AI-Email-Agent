import os
import fitz  # PyMuPDF
import docx
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_text_from_pdf(path):
    try:
        doc = fitz.open(path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        return f"[Error extracting PDF: {e}]"

def extract_text_from_docx(path):
    try:
        doc = docx.Document(path)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        return f"[Error extracting DOCX: {e}]"

def summarize_text(text):
    prompt = f"Summarize the following document content: {text[:2000]}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"[Error summarizing: {e}]"

def parse_attachments(file_paths):
    summaries = []
    for path in file_paths:
        ext = os.path.splitext(path)[1].lower()
        if ext == ".pdf":
            text = extract_text_from_pdf(path)
        elif ext == ".docx":
            text = extract_text_from_docx(path)
        else:
            summaries.append(f"[Unsupported file: {path}]")
            continue
        summaries.append(f"Summary of {os.path.basename(path)}:" + summarize_text(text))
    return summaries
