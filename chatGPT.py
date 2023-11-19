from openai import OpenAI

OPENAI_API_KEY = "PASTE YOUR KEY HERE"
client = OpenAI(api_key=OPENAI_API_KEY)


def get_chatgpt_response(message):
    chat_completion = client.chat.completions.create(
        messages=message,
        model="gpt-3.5-turbo",
    )
    return chat_completion.choices[0].message.content
