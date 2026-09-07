import ollama
from llm import analyze_question


MODEL = "gemma4"


def ask_llm(messages: list[dict]) -> str:
    stream = ollama.chat(
        model=MODEL,
        messages=messages,
        stream=True,
    )

    full_response = ""

    for chunk in stream:
        text = chunk["message"]["content"]
        print(text, end="", flush=True)
        full_response += text

    return full_response


def main():
    print("AI CLI Assistant")
    print("Type 'exit' to quit.")
    print("Type '/analyze <question>' for structured output.\n")

    messages = []

    while True:
        question = input("You: ")

        if question.lower() == "exit":
            print("Goodbye!")
            break

        if not question.strip():
            continue

        # V4: Structured Output
        if question.startswith("/analyze "):
            analyze_input = question[len("/analyze "):]

            result = analyze_question(analyze_input)

            print("\nAI:")
            print(f"Topic: {result['topic']}")
            print(f"Difficulty: {result['difficulty']}")
            print(f"Summary: {result['summary']}\n")

            continue

        # V2 + V3: Conversation History + Streaming
        messages.append({
            "role": "user",
            "content": question,
        })

        print("\nAI: ", end="")

        answer = ask_llm(messages)

        messages.append({
            "role": "assistant",
            "content": answer,
        })

        print()


if __name__ == "__main__":
    main()