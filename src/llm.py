import json
import ollama

MODEL = "gemma4"


def analyze_question(question: str) -> dict:
    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": question,
            }
        ],
        format={
            "type": "object",
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
        },
    )

    return json.loads(response["message"]["content"])