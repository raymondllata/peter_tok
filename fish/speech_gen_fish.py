from fish_audio_sdk import Session, TTSRequest, ReferenceAudio
import os
from dotenv import load_dotenv
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
    hash_object = hashlib.sha256(truncated_bytes.encode('utf-8'))
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

def file_exists(model_name, speech_hash, output_dir="output"):
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

# Load environment variables from .env file
def generate_speech(speech, model_id, model_name):
    load_dotenv()

    # Access environment variables
    fish_api = os.getenv("fish_api")

    session = Session(fish_api)
    PETER_GRIFFIN_MODEL_ID = os.getenv(model_id)
    speech_hash = generate_speech_hash(speech, 10)

    # Check if this file has been generated already (search output directory)
    files = file_exists(model_name, speech_hash)
    # Do not generate repeat files to save API information
    if len(files) > 0:
        print(f"This file has already been generated. To generate again, please delete the following file: %s", files[0])
        return files[0]

    # Generate file
    filename = model_name + speech_hash + ".mp3"
    with open(filename, "wb") as f:
        for chunk in session.tts(TTSRequest(
            reference_id=PETER_GRIFFIN_MODEL_ID,
            text=speech
        )):
            f.write(chunk)
    
    return filename


if __name__ == "__main__":
    default_speech = """\
    alright. so uh. let's talk about the unix v6 file system. it's old but solid. real simple. real clean.  

    first. you got the boot block. it kicks things off. like. without it. the system ain't wakin' up. then. there's the superblock. the big boss. it knows where everything is. mess that up. and uh. you're done. 

    (break)  

    now. files? they don't just sit somewhere. they got inodes. tiny little ID cards. holdin' all the details. name. size. permissions. even where the data is actually stored.  

    then you got data blocks. that's where the real stuff lives. all your files. all your content. locked in those blocks.  

    and uh. don't sleep on the free list. that's how the system keeps track of empty space. makin' sure new files got room to drop in. no free list. no new files.  

    (long-break)  

    so yeah. unix v6? old-school. but still the foundation for so much. keep your inodes tight. watch your superblock. and uh. don’t mess up your file system. 

    (laugh)"""
    model_id = "PETER_GRIFFIN_MODEL_ID"
    generate_speech(default_speech, model_id)