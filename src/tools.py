def calculate(a: float, b: float, operation: str) -> float:
    if operation == "add":
        return a + b

    if operation == "subtract":
        return a - b

    if operation == "multiply":
        return a * b

    if operation == "divide":
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    raise ValueError(f"Unknown operation: {operation}")


def get_time(city: str) -> str:
    times = {
        "delhi": "10:00 AM",
        "london": "4:30 AM",
        "new york": "11:30 PM",
        "tokyo": "1:00 PM",
    }

    return times.get(
        city.lower(),
        f"Time information for {city} is not available."
    )