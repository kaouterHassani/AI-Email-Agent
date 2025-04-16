import os
import sys
from utils.attachment_parser import parse_attachments

def main():
    if len(sys.argv) != 2:
        print("Usage: python summarize_attachments.py <attachment_dir>")
        return

    attachment_dir = sys.argv[1]
    if not os.path.isdir(attachment_dir):
        print(f"Invalid directory: {attachment_dir}")
        return

    file_paths = [
        os.path.join(attachment_dir, f)
        for f in os.listdir(attachment_dir)
        if f.lower().endswith((".pdf", ".docx"))
    ]

    summaries = parse_attachments(file_paths)
    for summary in summaries:
        print(summary)
        print("-" * 60)

if __name__ == "__main__":
    main()
