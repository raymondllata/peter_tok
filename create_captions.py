import stable_whisper

def extract_string(filename):
    """
    Extracts the filename without extension from a file path.
    
    Args:
        filename (str): The full file path including filename and extension.
        
    Returns:
        str: The extracted filename without extension.
             Returns error message if no period or slash is found.
    
    Example:
        >>> extract_string("path/to/file.mp3")
        "file"
    """
    # Find the position of the .mp3 extension
    dot_position = filename.rfind('.')
    
    if dot_position == -1:
        return "No period found in the string"
    
    # Find the last slash before the period
    last_slash_position = filename.rfind('/', 0, dot_position)
    
    if last_slash_position == -1:
        return "No slash found before the period"
    
    # Extract the substring between the slash and the period
    extracted_string = filename[last_slash_position + 1:dot_position]
    
    return extracted_string

def generate_captions(audio_file, script_file):
    """
    Generates SRT caption files by aligning audio with a script using stable_whisper.
    
    This function takes an audio file and a script file, aligns them using the
    stable_whisper model, and outputs an SRT caption file in the caption_model_output
    directory using the base filename of the audio file.
    
    Args:
        audio_file (str): Path to the audio file (MP3 format).
        script_file (str): Path to the text script file containing the transcript.
        
    Returns:
        None: Outputs an SRT file to the caption_model_output directory.
        
    Side Effects:
        - Loads the stable_whisper model
        - Prints alignment results
        - Creates an SRT file in the caption_model_output directory
    """
    # Read the script
    with open(script_file, 'r', encoding='utf-8') as f:
        script = f.read()
    
    model = stable_whisper.load_model('base')
    result = model.align(audio_file, script, language='en')
    print(result)
    string_hash = extract_string(audio_file)
    print(string_hash)
    result.to_srt_vtt('caption_model_output/' + string_hash + '.srt')
    return 'caption_model_output/' + string_hash + '.srt'



# Example usage:
if __name__ == "__main__":
    # try:
        script = "display_script.txt"
        audio = "audio_model_output/Peter Griffin_01ef0317c9.mp3"
        generate_captions(audio, script)
    # except:
    #     import argparse
        
    #     parser = argparse.ArgumentParser(description='Align speech audio to text script')
    #     parser.add_argument('audio_file', help='Path to the .wav audio file')
    #     parser.add_argument('script_file', help='Path to the text script file')
    #     parser.add_argument('--output', default='alignment_results.json', help='Output JSON file path')
        
    #     args = parser.parse_args()
        
    #     # Read the script
    #     with open(args.script_file, 'r', encoding='utf-8') as f:
    #         script = f.read()
        
    #     model = stable_whisper.load_model('base')
    #     result = model.align('cleaned_output1.mp3', script, language='en')
    #     print(result)
    #     result.to_srt_vtt('helloword.srt')