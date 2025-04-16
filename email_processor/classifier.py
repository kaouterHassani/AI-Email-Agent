import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def classify_email(email):
    prompt = f"""
You are an email classifier. Classify the following email into one of the categories:
- ticketCreation
- ticketClosing
- NegativeReview
- Normal

Email:
Subject: {email.get('subject')}
Content: {email.get('plainText')[:1000]}

Respond with only the category name.
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )

        category = response.choices[0].message["content"].strip()
        return category
    except Exception as e:
        return "Normal"
