from fish_audio_sdk import Session, TTSRequest, ReferenceAudio
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access environment variables
fish_api = os.getenv("fish_api")

session = Session(fish_api)

# Open the voice files in binary read mode
with open("peter_griffin_audio/peter_griffin_training.wav", "rb") as voice_file:
    # Read the file contents as binary data
    voice_data = voice_file.read()
    
    # Create the model with the voice data
    model = session.create_model(
        title="Peter Griffin",
        description="A Clone of Peter Griffin",
        voices=[voice_data]
    )

    print(model)

    # Get the model ID
    model_id = model.id  # Adjust this based on how the model object returns its ID
    
    # Append the model ID to the .env file
    with open(".env", "a") as env_file:
        env_file.write(f"\nPETER_GRIFFIN_MODEL_ID={model_id}\n")
    
    print(f"Added model ID {model_id} to .env file")