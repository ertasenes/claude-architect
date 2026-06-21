import os
from dotenv import load_dotenv 
from anthropic import Anthropic

load_dotenv()

client = Anthropic()

message = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1000,
    messages=[
        {"role": "user", "content": "Merhaba! Kendini bir cümleyle tanıtır mısın?"}
    ]
)

print(message.content[0].text)
