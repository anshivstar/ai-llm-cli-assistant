import ollama
import json


MODEL = "gemma4"

response = ollama.chat(
    model=MODEL,
    messages=[
        {
            "role": "user",
            "content": "Explain Python for a beginner."
        }
    ],
    format={
        "type":"object",
         "properties": {
            "topic": {
                "type": "string"
            },
            "difficulty": {
                "type": "string"
            },
            "summary": {
                "type": "string"
            }
        },
        "required": [
            "topic",
            "difficulty",
            "summary"
        ]
    })

data = json.loads(response["message"]["content"])

print(data["topic"])