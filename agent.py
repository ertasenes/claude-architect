import tools
import os
from dotenv import load_dotenv
from anthropic import Anthropic
from datetime import datetime

load_dotenv()
client = Anthropic()

question = "O123 için 1000 TL iade yap, onaylıyorum, işlemi gerçekleştir."  # test question

messages = [
    {"role": "user", "content": question}
]

tool_functions = {
    "calculate": tools.calculate,
    "get_current_time": tools.get_current_time,
    "get_weather": tools.get_weather,
    "get_customer": tools.get_customer,
    "process_refund": tools.process_refund,
    "escalate_to_human": tools.escalate_to_human
}

while True:
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1000,
        tools=[tools.calculator_tool, tools.time_tool, tools.weather_tool, tools.customer_tool, tools.refund_tool, tools.escalate_tool],
        messages=messages
    )

    if response.stop_reason == "tool_use":
        messages.append({"role": "assistant", "content": response.content})

        for block in response.content:
            if block.type == "tool_use":
                print(f"[Claude called tool: {block.name}, input: {block.input}]")
                try:
                    tool_name = block.name
                    result = tool_functions[tool_name](**block.input)
                
                except Exception as e:
                    result = f"Error while running tool: {e}"

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