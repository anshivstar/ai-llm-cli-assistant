import ollama

from llm import analyze_question
from tools import calculate, get_time


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
                        "description": "Mathematical operation.",
                    },
                },
                "required": ["a", "b", "operation"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "Get the current time for a city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name.",
                    }
                },
                "required": ["city"],
            },
        },
    },
]


def execute_tool(function_name: str, arguments: dict):
    """
    Execute the tool requested by the LLM.
    """

    try:
        if function_name == "calculate":
            return calculate(
                arguments["a"],
                arguments["b"],
                arguments["operation"],
            )

        if function_name == "get_time":
            return get_time(
                arguments["city"]
            )

        return f"Unknown tool: {function_name}"

    except Exception as e:
        return f"Tool execution failed: {str(e)}"


def ask_llm(messages: list[dict]) -> str:

    # First LLM call
    response = ollama.chat(
        model=MODEL,
        messages=messages,
        tools=TOOLS,
    )

    assistant_message = response["message"]

    # Add the assistant's response/tool request to conversation
    messages.append(assistant_message)

    tool_calls = assistant_message.get("tool_calls", [])

    # No tool required
    if not tool_calls:
        return assistant_message.get("content", "")

    # Execute requested tools
    for tool_call in tool_calls:

        function_name = tool_call["function"]["name"]
        arguments = tool_call["function"]["arguments"]

        result = execute_tool(
            function_name,
            arguments,
        )

        print(
            f"\n[Tool: {function_name} → {result}]"
        )

        # Send tool result back to the LLM
        messages.append({
            "role": "tool",
            "content": str(result),
        })

    # Second LLM call using tool result
    final_response = ollama.chat(
        model=MODEL,
        messages=messages,
    )

    return final_response["message"].get("content", "")


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

        # V5 + V6: Tool Calling
        answer = ask_llm(messages)

        print(answer)

        # Store final assistant answer
        messages.append({
            "role": "assistant",
            "content": answer,
        })

        print()


if __name__ == "__main__":
    main()