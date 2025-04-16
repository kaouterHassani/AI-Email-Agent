import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_info(email, category):
    prompt = f"""
You are an email information extractor. Based on the category '{category}', extract relevant structured information.

Categories and expected fields:
- ticketCreation: client_name, client_email, address, telephone, email_id, attachment_titles, required_skills, services_required, estimated_duration, deadline
- ticketClosing: email_id, comments, client_name, client_email, attachment_titles
- NegativeReview: client_name, client_email, feedback, email_id
- Normal: client_name, client_email, content

Here is the email content:
Subject: {email.get('subject')}
From: {email.get('from')}
To: {email.get('to')}
Content: {email.get('plainText')[:1500]}

Respond with a JSON object with the relevant fields.
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        info = response.choices[0].message["content"].strip()
        return eval(info)
    except Exception as e:
        return {"error": str(e)}
