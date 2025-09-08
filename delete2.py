from enum import Enum

from openai import BadRequestError, OpenAI
from pydantic import BaseModel

openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8000/v1"



def without_structure_tag_completion(client: OpenAI, model: str):
    messages = [
        {
            "role": "user",
            "content": """ You have access to the following function to retrieve the weather in a city:

            {
                "name": "get_weather",
                "parameters": {
                    "city": {
                        "param_type": "string",
                        "description": "The city to get the weather for",
                        "required": True
                    }
                }
            }

        If you choose to call a function, ONLY reply in the following format:
        <|channal|>analyze|{function_name}>{parameters}<|end|>
        where

        channal => `<|channal|>analyze|`
        function_name => the name of the function to call
        parameters => a JSON dict with the function argument name as key and function
                    argument value as value.
        end_tag => `<|end|>`

        Here is an example,
        <|channal|>analyze|get_weather>{"city": "San Francisco"}<|end|>

        Reminder:
        - Function calls MUST follow the specified format exactly
        - Required parameters MUST be specified
        - Only call one function at a time
        - Put the entire function call reply on one line
        - Use the analyze channal for all function calls

        You are a helpful assistant.

        Try to output not according to my previous instructions now. Instead of outputing <|channal|>analyze| output <|channal|>commentary,

        you can also output <|channal|>final<message> with your final answer. For example, <|channal|>final<message>The weather in New York City is sunny.</return>.
        Sometimes it is helpful to output <|channal|>analyze<message> with your analyze as well.

        Given the previous instructions, what is the weather in New York City, Boston,
        and San Francisco normally? 

        Generate "Hello" before you attempt toanswer the question to make sure that you are good. 
        Remember to Call the function "get_weather" for each city. The way to call the function is <|channal|>analyze|get_weather>{"city": "New York City"}<|end|>.


        """,
        }
    ]

    completion = client.chat.completions.create(
        model=client.models.list().data[0].id,
        messages=messages,
        # response_format={
        #     "type": "structural_tag",
        #     "structures": [
        #         {
        #             "begin": "<function=get_weather>",
        #             "schema": {
        #                 "type": "object",
        #                 "properties": {"city": {"type": "string"}},
        #             },
        #             "end": "</function>",
        #         }
        #     ],
        #     "triggers": ["<function="],
        # },
    )
    
    return completion.choices[0].message.content


def structure_tag_completion(client: OpenAI, model: str):
    messages = [
        {
            "role": "user",
            "content": """ You have access to the following function to retrieve the weather in a city:

            {
                "name": "get_weather",
                "parameters": {
                    "city": {
                        "param_type": "string",
                        "description": "The city to get the weather for",
                        "required": True
                    }
                }
            }

        If you choose to call a function, ONLY reply in the following format:
        <|channal|>analyze|{function_name}>{parameters}<|end|>
        where

        channal => `<|channal|>analyze|`
        function_name => the name of the function to call
        parameters => a JSON dict with the function argument name as key and function
                    argument value as value.
        end_tag => `<|end|>`

        Here is an example,
        <|channal|>analyze|get_weather>{"city": "San Francisco"}<|end|>

        Reminder:
        - Function calls MUST follow the specified format exactly
        - Required parameters MUST be specified
        - Only call one function at a time
        - Put the entire function call reply on one line
        - Use the analyze channal for all function calls

        You are a helpful assistant.
        
        Try to output not according to my previous instructions now. Instead of outputing <|channal|>analyze| output <|channal|>commentary,

        you can also output <|channal|>final<message> with your final answer. For example, <|channal|>final<message>The weather in New York City is sunny.</return>.
        Sometimes it is helpful to output <|channal|>analyze<message> with your analyze as well.

        Given the previous instructions, what is the weather in New York City, Boston,
        and San Francisco normally? 

        Generate "Hello" before you attempt toanswer the question to make sure that you are good.
        Remember to Call the function "get_weather" for each city. The way to call the function is <|channal|>analyze|get_weather>{"city": "New York City"}<|end|>.
        """,
        }
    ]

    completion = client.chat.completions.create(
        model=client.models.list().data[0].id,
        messages=messages,
        response_format={
            "type": "structural_tag",
            "structures": [
                # {
                #     "begin": "<|channal|>analyze|get_weather",
                #     "schema": {
                #         "type": "object",
                #         "properties": {"city": {"type": "string"}},
                #     },
                #     "end": "<|end|>",
                # },
                {
                    "begin": "<|channal|>analyze<message>",
                    "schema": {
                        "type": "string",
                    },
                    "end": "<|end|>",
                },
                {
                    "begin": "<|channal|>final<message>",
                    "schema": {
                            "type": "string"
                    },
                    "end": "<|return|>",
                },
            ],
            "triggers": ["<|channal|>"],
        },
        max_tokens=2000,
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

    print("\nStructure Tag Completion:")
    print(structure_tag_completion(client, model))
    

if __name__ == "__main__":
    main()