import ollama


MODEL = "gemma4"


def ask_llm(messages: list[dict]) -> str:
    response = ollama.chat(
        model=MODEL,
        messages=messages,
    )

    return response["message"]["content"]


def main():
    print("AI CLI Assistant")
    print("Type 'exit' to quit.\n")

    messages = []

    while True:
        question = input("You: ")

        if question.lower() == "exit":
            print("Goodbye!")
            break



        if not question.strip():
            continue

        messages.append({"role": "user", "content": question})

        answer = ask_llm(messages)

        messages.append({
            "role": "assistant",
            "content": answer,
        })


        print(f"\nAI: {answer}\n")


if __name__ == "__main__":
    main()