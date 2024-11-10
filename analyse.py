import os
from flask import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPEN_AI = os.getenv("OPEN_AI")
def analyse_fossil(fossil_name):
    client = OpenAI(api_key=OPEN_AI)
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "user",
                    "content": f"Return specific information about the {fossil_name} fossil. For the fossil, provide 3 key pieces of information: Age: The general age of that type of fossil (give a year -- ie x years old), Location: The location where the fossil is commonly found, Fact_1: A fun fact about the fossil. Fact_2: A different fun fact about the fossil. Fact_3: Another unique fact about the fossil. Return it in the following json format exactly.",
                }
            ],
            functions=[
                {
                    "name": "get_fossil_info",
                    "description": "Retrieve detailed information about a specific fossil",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "Age": {"type": "string"},
                            "Location": {"type": "string"},
                            "Fact_1": {"type": "string"},
                            "Fact_2": {"type": "string"},
                            "Fact_3": {"type": "string"},
                        },
                        "required": ["Age", "Location", "Fact_1", "Fact_2", "Fact_3"],
                    },
                }
            ],
            function_call={"name": "get_fossil_info"},
        )

        # The response structure changed - we need to access it differently
        function_args = response.choices[0].message.function_call.arguments
        
        # Load the arguments as a JSON object
        fossil_info = json.loads(function_args)
        print(fossil_info)

        # Return the complete fossil info
        return {
            "name": fossil_name,
            "Age": fossil_info.get("Age", "Error"),
            "Location": fossil_info.get("Location", "Error"),
            "Fact_1": fossil_info.get("Fact_1", "Error"),
            "Fact_2": fossil_info.get("Fact_2", "Error"),
            "Fact_3": fossil_info.get("Fact_3", "Error"),
        }

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return {
            "name": "Error",
            "Age": "Error",
            "Location": "Error",
            "Fact_1": "Error",
            "Fact_2": "Error",
            "Fact_3": "Error",
        }