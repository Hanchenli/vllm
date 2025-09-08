from enum import Enum

from openai import BadRequestError, OpenAI
from pydantic import BaseModel

openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8000/v1"


def get_weather(location: str, unit: str):
    return f"Getting the weather for {location} in {unit}..."
tool_functions = {"get_weather": get_weather}

tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "City and state, e.g., 'San Francisco, CA'"},
                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
            },
            "required": ["location", "unit"]
        }
    }
}]


def without_structure_tag_completion(client: OpenAI, model: str):

    completion = client.chat.completions.create(
        model=client.models.list().data[0].id,
        messages=[{
            "role": "user",
            "content": "What's the weather like in San Francisco? "
            }],
        response_format={
            "type": "structural_tag",
            "structures": [
                {           
                    "begin": "<|channel|>analysis_111",
                    "schema": {
                        "type": "string",
                    },  
                    "end": "</think>",
                }
            ],
            "triggers": ["<|channel|>analysis"],
        },
        max_tokens=100,
    )

    
    return completion.choices[0].message.content


def main():
    client: OpenAI = OpenAI(
        base_url=openai_api_base,
        api_key=openai_api_key,
    )

    model = client.models.list().data[0].id

    print("\nWithout Structure Tag Completion:")
    print(without_structure_tag_completion(client, model))
    

if __name__ == "__main__":
    main()