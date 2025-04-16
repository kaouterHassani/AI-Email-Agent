import os
import json
from email_processor.classifier import classify_email
from email_processor.extractor import extract_info
from utils.vector_store import VectorStore
import csv

EMAIL_FILE = "emails.json"
CSV_OUTPUT = "results/results.csv"
JSON_OUTPUT = "results/results.json"
FAISS_INDEX = "results/faiss.index"
FAISS_META = "results/faiss_metadata.json"

def main():
    vector_store = VectorStore()
    all_results = []
    
    with open(EMAIL_FILE, "r", encoding="utf-8") as f:
        emails = json.load(f)["emails"]

    for email in emails:
        category = classify_email(email)
        #print(f"\n Email UID: {email.get('uid')} | Category: {category}")

        extracted_data = extract_info(email, category)
        if "attachments" in email:
            attachment_titles = [
                att["filename"] for att in email.get("attachments", [])
                if isinstance(att, dict) and "filename" in att
            ]
            extracted_data["attachment_titles"] = attachment_titles
            
        extracted_data["category"] = category
        extracted_data["email_uid"] = email.get("uid")
        
        all_results.append(extracted_data)
        vector_store.add(extracted_data, uid=email.get("uid"))
        #print(" Extracted Info:", json.dumps(extracted_data, indent=2, ensure_ascii=False))

    # Save to JSON
    with open(JSON_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)

    # Save to CSV
    keys = set(k for r in all_results for k in r.keys())
    with open(CSV_OUTPUT, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(keys))
        writer.writeheader()
        writer.writerows(all_results)

    # Save to FAISS
    vector_store.save_index(FAISS_INDEX, FAISS_META)
    print(f"✅ Results saved to {CSV_OUTPUT}, {JSON_OUTPUT}, {FAISS_INDEX}")

if __name__ == "__main__":
    main()
