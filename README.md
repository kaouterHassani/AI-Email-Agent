# AI-Email-Agent
An intelligent automation tool for processing email inbox data, classifying messages, extracting structured information, parsing attachments, and auto-filling ticket forms — all powered by OpenAI, LangChain, and FAISS.

---
##  Features

-  **Email Classification**: Classifies emails into `ticketCreation`, `ticketClosing`, `NegativeReview`, and `Normal`
-  **Structured Data Extraction**: Uses GPT-4 to extract relevant fields per category
-  **Attachment Parsing**: Extracts & summarizes content from PDF/DOCX files
-  **FAISS Vector DB Integration**: Stores extracted content for semantic retrieval
-  **Auto Form Filling**: Auto-fills ticket creation or closing forms from vector-matched data
-  **Exports**: Saves extracted results to `.csv`, `.json`, and `.faiss` index

---

##  Folder Structure

<pre> ai-email-agent/ 
├── process_emails.py # Extracts & classifies email data into structured JSON 
├── summarize_attachments.py # Summarizes documents in a given directory 
├── auto_fill_ticket.py # Auto-fills a form from stored data (supports --uid or query) 
├── emails.json # email input 
├── requirements.txt # Python dependencies 
├── utils/ 
│ └── attachment_parser.py # Attachment loading and summarizing 
│ └── vector_store.py # FAISS database integration 
├── email_processor/ 
│ └── classifier.py # Email category prediction 
│ └── extractor.py # Field-level structured info extraction based on the category </pre>

---

##  Installation
# 1. Clone the repo or unzip the folder
<pre> cd ai-email-agent </pre>

# 2. Create and activate a virtual environment (recommended)
<pre> python -m venv env
source env/bin/activate  </pre>

# 3. Install dependencies
<pre> pip install -r requirements.txt </pre>

# 4. Set your OpenAI API key
<pre> export OPENAI_API_KEY=your-key-here  # or use a .env file </pre>
