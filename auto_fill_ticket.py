import os
import sys
import json
import faiss
import numpy as np
import openai
from typing import List, Optional
from pydantic import BaseModel, Field
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from openai import OpenAI
# === Define schemas for each category ===

class TicketCreationForm(BaseModel):
    client_name: str
    client_email: str
    address: Optional[str] = ""
    telephone: Optional[str] = ""
    email_id: Optional[str] = ""
    attachment_titles: List[str] = []
    required_skills: Optional[str] = ""
    services_required: Optional[str] = ""
    estimated_duration: Optional[str] = ""
    deadline: Optional[str] = ""

class TicketClosingForm(BaseModel):
    email_id: str
    comments: Optional[str] = ""
    client_name: str
    client_email: str
    attachment_titles: List[str] = []

# === Setup ===

INDEX_PATH = "results/faiss.index"
META_PATH = "results/faiss_metadata.json"
#openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
embedding_model = OpenAIEmbeddings(model="text-embedding-ada-002")

def load_vector_db():
    if not os.path.exists(INDEX_PATH) or not os.path.exists(META_PATH):
        raise FileNotFoundError("FAISS index or metadata not found.")
    index = faiss.read_index(INDEX_PATH)
    with open(META_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    return index, metadata

def search_by_uid(uid: int, metadata: list):
    for entry in metadata:
        if entry.get("uid") == uid:
            return entry["data"]
    return None

def search_by_query(query: str, index, metadata, top_k=1):
    embedding = embedding_model.embed_query(query)
    D, I = index.search(np.array([embedding], dtype=np.float32), top_k)
    return metadata[I[0][0]]["data"] if I[0][0] != -1 else None

def fill_form(data):
    category = data.get("category", "Normal")

    if category == "ticketCreation":
        parser = PydanticOutputParser(pydantic_object=TicketCreationForm)
    elif category == "ticketClosing":
        parser = PydanticOutputParser(pydantic_object=TicketClosingForm)
    else:
        print("❗ Unsupported category for form autofill:", category)
        return

    prompt = PromptTemplate(
        template="Given the following structured ticket data:\n{data}\n\n{format_instructions}",
        input_variables=["data"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    formatted_prompt = prompt.format(data=json.dumps(data, ensure_ascii=False))
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": formatted_prompt}],
        temperature=0,
    )
    structured = parser.parse(response.choices[0].message.content)
    print(json.dumps(structured.model_dump(), indent=2, ensure_ascii=False))

def main():
    if len(sys.argv) < 2:
        print("Usage:\n  python auto_fill_ticket.py --uid <number>\n  python auto_fill_ticket.py \"<query string>\"")
        return

    index, metadata = load_vector_db()

    if sys.argv[1] == "--uid":
        try:
            uid = int(sys.argv[2])
            data = search_by_uid(uid, metadata)
            if not data:
                print(f"❌ No data found for UID {uid}")
                return
        except (IndexError, ValueError):
            print("❌ Please provide a valid UID after --uid")
            return
    else:
        query = " ".join(sys.argv[1:])
        data = search_by_query(query, index, metadata)
        if not data:
            print("❌ No relevant match found in vector DB.")
            return

    fill_form(data)

if __name__ == "__main__":
    main()
