from fish_audio_sdk import Session, TTSRequest, ReferenceAudio
import os
from dotenv import load_dotenv
from fuzzy_json import FuzzyJsonStorage
import hashlib

def generate_speech_hash(speech_string, target_length=10):
    """
    Generate a hash for a speech string and ensure it's of the target length.
    
    Args:
        speech_string: The input string to hash
        target_length: The desired length of the output hash string
    
    Returns:
        A string of target_length containing the hash
    """
    # Encode the string to bytes and take only the first n bytes
    input_bytes = speech_string.encode('utf-8')
    truncated_bytes = input_bytes[:target_length]

    # Generate SHA-256 hash of the input string
    hash_object = hashlib.sha256(truncated_bytes)
    hash_hex = hash_object.hexdigest()
    
    # If the hash is shorter than target_length, pad with zeros
    if len(hash_hex) < target_length:
        padded_hash = hash_hex.ljust(target_length, '0')
        return padded_hash
    
    # If the hash is longer than target_length, truncate it
    elif len(hash_hex) > target_length:
        return hash_hex[:target_length]
    
    # If the hash is exactly target_length, return it as is
    else:
        return hash_hex

    # Example usage
    # speech = "This is a sample speech that needs to be hashed."
    # hash_result = generate_speech_hash(speech, 16)
    # print(f"Original speech: {speech}")
    # print(f"Hash (length {len(hash_result)}): {hash_result}")

def file_exists(model_name, speech_hash, output_dir="audio_model_output"):
    """
    Check if a file with the exact model name and speech hash exists.
    
    Args:
        model_name: Name of the model
        speech_hash: The hash generated from the speech
        output_dir: Directory to check for existing files
    
    Returns:
        Boolean indicating if the file exists
    """
    filename = f"{model_name}_{speech_hash}.mp3"
    file_path = os.path.join(output_dir, filename)
    
    return os.path.isfile(file_path)

# Generate the speech .mp3 file
def generate_speech(speech, model_name):
    load_dotenv()

    # Access environment variables
    fish_api = os.getenv("fish_api")
    session = Session(fish_api)
    table_path = "fish/models.json"
    storage = FuzzyJsonStorage.load_from_file(table_path)
    PETER_GRIFFIN_MODEL_ID = storage.get(model_name)
    speech_hash = generate_speech_hash(speech, 10)

    # Generate file
    filename = f"{model_name}_{speech_hash}.mp3"
    filename = os.path.join("audio_model_output", filename)

    # Check if this file has been generated already (search output directory)
    file_exist = file_exists(model_name, speech_hash)
    # Do not generate repeat files to save API information
    if file_exist:
        print(f"This file has already been generated. To generate again, please delete the following file: %s", filename)
        return filename

    with open(filename, "wb") as f:
        for chunk in session.tts(TTSRequest(
            reference_id=PETER_GRIFFIN_MODEL_ID,
            text=speech
        )):
            f.write(chunk)
    
    return filename


if __name__ == "__main__":
    with open("script.txt", 'r', encoding='utf-8') as f:
        script = f.read()
    model_name = "Peter Griffin"
    generate_speech(script, model_name)