from fish_audio_sdk import Session, TTSRequest, ReferenceAudio
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access environment variables
fish_api = os.getenv("fish_api")

session = Session(fish_api)

# Open the voice files in binary read mode
with open("miles_morales_one_edited.mp3", "rb") as voice_file, open("miles_morales_two.mp3", "rb") as other_voice_file:
    # Read the file contents as binary data
    voice_data = voice_file.read()
    other_voice_data = other_voice_file.read()
    
    # Create the model with the voice data
    model = session.create_model(
        title="test miles",
        description="test miles",
        voices=[voice_data, other_voice_data],
    )

    print(model)