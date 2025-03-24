from pydantic import BaseModel
from dotenv import load_dotenv
import os
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")

# # Define the structure for math steps
# class Step(BaseModel):
#     explanation: str
#     output: str

# # Define the overall response structure
# class MathResponse(BaseModel):
#     steps: list[Step]
#     final_answer: str

# Initialize OpenAI client with API key
client = OpenAI(api_key=api_key)

# Make the request to parse a structured output
completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system", "content": "You are a helpful math tutor."},
        {"role": "user", "content": "solve 8x + 31 = 2"},
    ]
    # response_format=MathResponse,
)

# Process the response
# message = completion.choices[0].message
# if message.parsed:
#     print(message)
#     print(message)
# else:
#     print(message.refusal)
print (completion.message)