from datetime import datetime
    

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

def get_customer(customer_id):
    """Returns the customer info for a given customer_id."""
    customers = {
        "C001": {"name": "Ali Veli", "email": "ali@hotmail.com"},
        "C002": {"name": "Veli Ali", "email": "veli@hotmail.com"},
        "C003": {"name": "Ahmet Ali", "email": "ahmet@hotmail.com"}
        
}
    if customer_id in customers:
        return customers[customer_id]
    else:
        return "Customer not found"

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
customer_tool = {
    "name": "get_customer",
    "description": "Returns the customer info. Use when user need customer info",
    "input_schema": {
        "type": "object",
        "properties": {
            "customer_id": {
                "type": "string",
                "description": "customer_id, for example C001"
                }
            },

        "required":["customer_id"]
    }
}