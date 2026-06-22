import os
from dotenv import load_dotenv
from anthropic import Anthropic
from datetime import datetime

load_dotenv()
client = Anthropic()


def calculate(operation, a, b):
    """Performs one of four arithmetic operations on two numbers."""
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        if b == 0:
            return "Error: cannot divide by zero"
        return a / b
    else:
        return "Unknown operation"


def get_current_time():
    """Returns the current date and time."""
    return datetime.now().strftime("%d.%m.%Y %H:%M")
    
def get_weather(city):
    """returns the current weather of the city as celsius"""
    return f"{city}: 22c, sunny" 

calculator_tool = {
    "name": "calculate",
    "description": "Performs arithmetic (add, subtract, multiply, divide) on two numbers. Use when exact calculation is needed.",
    "input_schema": {
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "enum": ["add", "subtract", "multiply", "divide"],
                "description": "The operation to perform"
            },
            "a": {"type": "number", "description": "First number"},
            "b": {"type": "number", "description": "Second number"}
        },
        "required": ["operation", "a", "b"]
    }
}

time_tool = {
    "name": "get_current_time",
    "description": "Returns the current date and time. Use when the user asks about today's date, the day, the time, or anything time-related.",
    "input_schema": {
        "type": "object",
        "properties": {},
        "required": []
    }
}

weather_tool = {
    "name": "get_weather",
    "description": "Returns the current weather of the city as a celsius. Use when user asks the weather",
    "input_schema": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "city name"
                }
            },

        "required":["city"]
    }
}

question = "What is the weather in Istanbul right now" """get question depend on tools"""

messages = [
    {"role": "user", "content": question}
]

while True:
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1000,
        tools=[calculator_tool, time_tool, weather_tool],
        messages=messages
    )

    if response.stop_reason == "tool_use":
        messages.append({"role": "assistant", "content": response.content})

        for block in response.content:
            if block.type == "tool_use":
                print(f"[Claude called tool: {block.name}, input: {block.input}]")

                try:
                    if block.name == "calculate":
                        result = calculate(
                            block.input["operation"],
                            block.input["a"],
                            block.input["b"]
                        )
                    elif block.name == "get_current_time":
                        result = get_current_time()
                    elif block.name == "get_weather":
                        result = get_weather(block.input["city"])
                    else:
                        result = f"Error: unknown tool '{block.name}'"
                except Exception as e:
                    result = f"Error while running tool: {e}"
                print(f"[Tool result: {result}]")

                messages.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": str(result)
                        }
                    ]
                })
    else:
        print("\nClaude's final answer:")
        print(response.content[0].text)
        break