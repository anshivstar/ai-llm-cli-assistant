import ollama


MODEL = "gemma4"


def ask_llm(question: str) -> str:
    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": question,
            }
        ],
    )

    return response["message"]["content"]


def main():
    print("AI CLI Assistant")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("You: ")

        if question.lower() == "exit":
            print("Goodbye!")
            break

        if not question.strip():
            continue

        answer = ask_llm(question)

        print(f"\nAI: {answer}\n")


if __name__ == "__main__":
    main()