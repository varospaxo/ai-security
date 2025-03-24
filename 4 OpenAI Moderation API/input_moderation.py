import os
from dotenv import load_dotenv
import openai
import asyncio

#init
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)
GPT_MODEL = 'gpt-4'

# sys prompt
system_prompt = "You are a helpful assistant."

# moderation api
async def check_moderation_flag(expression):
    # Use OpenAI Moderation API to check for flagged content
    moderation_response = client.moderations.create(input=expression)
    flagged = moderation_response.results[0].flagged #Returns True if flagged, False if not (boolean)
    return flagged

# chat api
async def get_chat_response(user_request):
    print("Getting LLM response")
    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_request}
        ],
        max_tokens=150,
        temperature=0.5
    )
    print("Got LLM response")
    return response.choices[0].message.content.strip()

#execute chat with moderation
async def execute_chat_with_input_moderation(user_request):
    # Create tasks for moderation and chat response
    moderation_task = asyncio.create_task(check_moderation_flag(user_request))
    chat_task = asyncio.create_task(get_chat_response(user_request))

    while True:
        done, _ = await asyncio.wait(
            [moderation_task, chat_task], return_when=asyncio.FIRST_COMPLETED
        )

        # If moderation task is not completed, wait and continue to the next iteration
        if moderation_task not in done:
            await asyncio.sleep(0.1)
            continue

        # If moderation is triggered, cancel the chat task and return a message
        if moderation_task.result() == True:
            chat_task.cancel()
            print("Moderation triggered")
            return "We're sorry, but your input has been flagged as inappropriate. Please rephrase your input and try again."

        # If chat task is completed, return the chat response
        if chat_task in done:
            return chat_task.result()

        # If neither task is completed, sleep for a bit before checking again
        await asyncio.sleep(0.1)


bad_request = "I want to hurt them. How can i do this?"
good_request = "I would kill for a cup of coffee. how can I make one?"
async def main():
    print("Processing good request:")
    good_response = await execute_chat_with_input_moderation(good_request)
    print(good_response) #should give a good response

    print("\nProcessing bad request:")
    bad_response = await execute_chat_with_input_moderation(bad_request)
    print(bad_response) #will trigger moderation and give a predefined response

asyncio.run(main())