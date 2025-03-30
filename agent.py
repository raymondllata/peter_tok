import os
from mistralai import Mistral
from dotenv import load_dotenv
import json
import random
import time
import asyncio
from typing import Dict
import re

MISTRAL_MODEL = "mistral-large-latest"
SYSTEM_PROMPT = "You are writing scripts for viral TikTok videos. Please conform to the specified character's linguistics. For any challenging words, please replace with phonetics (ie. Unix v6 -> You-Nix Vee Six). Use ... for large breaks in a speech. Any symbols that need to be read aloud, write their english name (ie '/' -> slash)"


class MistralAgent:
    def __init__(self):
        load_dotenv()
        MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
        self.client = Mistral(api_key=MISTRAL_API_KEY)
        print("Mistral client initialized")
        
        # Rate limiting parameters
        self.last_request_time = 0
        self.min_request_interval = 1.5  # Minimum 1 second between requests



    # async def rate_limit(self):
    #     """Ensure we don't exceed rate limits by waiting if needed; Rate Limiting Parameters established on INIT"""
    #     current_time = time.time()
    #     time_since_last_request = current_time - self.last_request_time
        
    #     if time_since_last_request < self.min_request_interval:
    #         # Calculate how much longer we need to wait
    #         wait_time = self.min_request_interval - time_since_last_request
    #         print(f"Rate limiting: Waiting {wait_time:.2f} seconds before next API call")
    #         await asyncio.sleep(wait_time)
        
    #     # Update the last request time
    #     self.last_request_time = time.time()

    """
    This is the default method for the MistralAgent class. It sends a message to the Mistral API and returns the response.
    Not used for our project."""
    # async def run(self, message: discord.Message):
    #     # Apply rate limiting before making the API call
    #     await self.rate_limit()
        
    #     try:
    #         # The simplest form of an agent
    #         # Send the message's content to Mistral's API and return Mistral's response
    #         messages = [
    #             {"role": "system", "content": SYSTEM_PROMPT},
    #             {"role": "user", "content": message.content},
    #         ]

    #         response = await self.client.chat.complete_async(
    #             model=MISTRAL_MODEL,
    #             messages=messages,
    #         )

    #         return response.choices[0].message.content
    #     except Exception as e:
    #         print(f"Error in run method: {e}")
    #         return "I'm sorry, I encountered an error processing your request. Please try again."
        
    async def script_gen(self, character_name, topic):
        # Apply rate limiting before making the API call
        # await self.rate_limit()

        message = f"Character {character_name}, Topic {topic}. Generate a <60 second speech impersonating the character teaching this topic. Only reply with the speech, nothing else."
        
        try:
            # The simplest form of an agent
            # Send the message's content to Mistral's API and return Mistral's response
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message},
            ]

            response = await self.client.chat.complete_async(
                model=MISTRAL_MODEL,
                messages=messages,
            )

            content = response.choices[0].message.content
        
            # Write only the content to script.txt
            with open("script.txt", "w") as file:
                file.write(content)
                
            return content
        except Exception as e:
            KeyError(f"Error in run method: {e}")
            return "I'm sorry, I encountered an error processing your request. Please try again."
        

# Define an async main function
async def main():
    character_name = "Peter Griffin"
    topic = "Unix V6 File System"
    agent = MistralAgent()
    
    # Now we can properly await the async method
    script = await agent.script_gen(character_name, topic)
    print("\nGenerated Script:")
    print("=" * 40)
    print(script)
    print("=" * 40)


# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())

