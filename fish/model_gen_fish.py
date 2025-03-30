from fish_audio_sdk import Session, TTSRequest, ReferenceAudio
import os
from dotenv import load_dotenv
from fuzzy_json import FuzzyJsonStorage
import json

def generate_model(model_name, description, audio_file):
    # Load environment variables from .env file
    load_dotenv()
    # Access environment variables
    fish_api = os.getenv("fish_api")
    session = Session(fish_api)

    table_path = "fish/models.json"
    # Check if json table exists
    if not os.path.exists(table_path):
        # File doesn't exist, create it with default data
        with open(table_path, 'w', encoding='utf-8') as f:
            tmp_storage = FuzzyJsonStorage()
            tmp_storage.save_to_file(table_path)
        print(f"Created new file: {table_path}")

    # Check if model_name exists within the JSON table
    storage = FuzzyJsonStorage.load_from_file(table_path)
    value = storage.get(model_name)
    if value:
        print("Model already exists in table models.json")
        return value

    # Open the voice files in binary read mode
    with open(audio_file, "rb") as voice_file:
        # Read the file contents as binary data
        voice_data = voice_file.read()
        
        # Create the model with the voice data
        model = session.create_model(
            title=model_name,
            description=description,
            voices=[voice_data]
        )

        print(model)

        # Get the model ID
        model_id = model.id  # Adjust this based on how the model object returns its ID
        storage.set(model_name, model_id)
        storage.save_to_file(table_path)
        print(f"Added model ID {model_id} to JSON Table")

if __name__ == "__main__":
    model_name = "Peter Griffin"
    description = "A Clone of Peter Griffin"
    audio_file = "audio_training_output/peter_griffin_training.wav"
    generate_model(model_name, description, audio_file)