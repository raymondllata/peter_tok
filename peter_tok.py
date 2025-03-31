import os
import sys
from pathlib import Path
import asyncio
import time
from vid_gen_srt import remote_main
from agent import MistralAgent
from create_captions import generate_captions, extract_string

# Add the fish directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
fish_dir = os.path.join(current_dir, 'fish')
sys.path.append(fish_dir)

# Now you can import your modules from fish
from model_gen_fish import *
from speech_gen_fish import *
from fuzzy_json import FuzzyJsonStorage

# Your other imports


# Assuming your modules are in the same directory or subdirectories
# Add appropriate imports for your script generation and processing modules

def display_intro():
    """Displays an introduction to the program."""
    print("\n" + "="*60)
    print("SHORT FORM CONTENT VIDEO GENERATOR".center(60))
    print("="*60)
    print("\nWelcome to the Short Form Content Generator!")
    print("This program will help you create engaging short-form videos")
    print("by generating content with character impersonations.")
    print("\nThe process is simple:")
    print("1. Select a character to impersonate")
    print("2. Choose a topic for your script")
    print("3. The program will generate the script, audio, and captions")
    print("4. You'll receive a complete video ready for sharing")
    print("\nLet's get started!")

def get_available_characters():
    """Returns a list of available characters to impersonate."""
    # This could read from a file or database
    # For now, we'll use a hardcoded list as an example
    characters = [
        "Peter Griffin",
        "Homer Simpson",
        "Rick Sanchez",
        "SpongeBob",
        "Batman",
        "Yoda"
        # Add more characters as needed
    ]
    return characters

def display_characters(characters):
    """Displays all available characters with numbers for selection."""
    print("\nAvailable Characters:")
    print("-" * 30)
    for i, character in enumerate(characters, 1):
        print(f"{i}. {character}")

def get_character_choice(characters):
    """Prompts user to select a character and returns the choice."""
    while True:
        try:
            choice = int(input("\nEnter the number of your chosen character: "))
            if 1 <= choice <= len(characters):
                return characters[choice-1]
            else:
                print(f"Please enter a number between 1 and {len(characters)}.")
        except ValueError:
            print("Please enter a valid number.")

def get_topic():
    """Prompts user for a topic for the script."""
    print("\nWhat topic would you like the character to talk about?")
    print("Examples: space exploration, cooking tips, dating advice, etc.")
    return input("Enter topic: ")

async def main():
    """Main function to run the program."""
    display_intro()
    agent = MistralAgent()
    

    # Open Storage
    storage = FuzzyJsonStorage.load_from_file("fish/models.json")
    characters = [c for c in storage.get_all_data()]
    
    # Get character selection
    # characters = get_available_characters()
    display_characters(characters)
    selected_character = get_character_choice(characters)
    
    # Get topic for script
    topic = get_topic()



    
    print(f"\nGreat! Generating a short video with {selected_character} talking about {topic}...")
    print("This may take a moment...")
    
    # Call your script generation function here
    # Example: script = generate_script(selected_character, topic)
    # Generate Script and Speech
    script = await agent.phonetic_script_gen(selected_character, topic)
    print("Script Done!")
    audio_path = generate_speech(script, selected_character)
    print("Phonetic Speech DOne")
    time.sleep(2)

    display_script = await agent.display_script_gen(script)
    print("Display Speech Done")
    srt_path = generate_captions(audio_path, "display_script.txt")
    print("Captions Done")
    video_path = "video/test-video-five.mp4"
    logo_path = "logos/Peter Griffin.png"

    unique_path = extract_string(audio_path)
    output_path = "final_product_output/" + unique_path + ".mp4"

    remote_main(video_path, audio_path, srt_path, output_path, logo_path)
    
    # Call your audio generation function here
    # Example: audio_file = generate_audio(selected_character, script)
    
    # Call your caption generation function here
    # Example: caption_file = generate_captions(audio_file, script)
    
    # Call your video assembly function here
    # Example: video_file = assemble_video(audio_file, caption_file)
    
    print("\nVideo generation complete!")
    # print(f"Your video is ready at: {video_file}")
    print("\nThank you for using the Short Form Content Generator!")

if __name__ == "__main__":
    asyncio.run(main())