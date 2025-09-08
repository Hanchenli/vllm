from openai import OpenAI

def main():
    client = OpenAI(
        base_url="http://localhost:8000/v1",
        api_key="EMPTY"
    )
    
    # Test basic response without tools
    response = client.responses.create(
        model="openai/gpt-oss-20b",
        input="Hello, respond hello to me",
    )

    print("Response:", response.output_text)

if __name__ == "__main__":
    main()
