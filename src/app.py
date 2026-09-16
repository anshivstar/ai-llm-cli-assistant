import ollama

from llm import analyze_question
from tools import calculate


MODEL = "gemma4"


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Perform a basic arithmetic calculation.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "First number",
                    },
                    "b": {
                        "type": "number",
                        "description": "Second number",
                    },
                    "operation": {
                        "type": "string",
                        "enum": [
                            "add",
                            "subtract",
                            "multiply",
                            "divide",
                        ],
                        "description": "Mathematical operation",
                    },
                },
                "required": ["a", "b", "operation"],
            },
        },
    }
]


def ask_llm(messages: list[dict]) -> str:
    response = ollama.chat(
        model=MODEL,
        messages=messages,
        tools=TOOLS,
    )

    tool_calls = response["message"].get("tool_calls", [])

    # No tool needed
    if not tool_calls:
        return response["message"]["content"]

    # Add the assistant's tool-call message to conversation
    messages.append(response["message"])

    # Execute requested tools
    for tool_call in tool_calls:
        function_name = tool_call["function"]["name"]
        arguments = tool_call["function"]["arguments"]

        if function_name == "calculate":
            result = calculate(
                arguments["a"],
                arguments["b"],
                arguments["operation"],
            )

            messages.append({
                "role": "tool",
                "content": str(result),
            })

    # Ask LLM to produce final answer
    final_response = ollama.chat(
        model=MODEL,
        messages=messages,
    )

    return final_response["message"]["content"]


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

        # V2: Conversation History
        messages.append({
            "role": "user",
            "content": question,
        })

        print("\nAI: ", end="")

        # V5: Tool Calling
        answer = ask_llm(messages)

        print(answer)

        messages.append({
            "role": "assistant",
            "content": answer,
        })

        print()


if __name__ == "__main__":
    main()