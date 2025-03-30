import numpy as np
from moviepy import TextClip
from pydub import AudioSegment
from vosk import Model, KaldiRecognizer, SetLogLevel
import stable_whisper

# Example usage:
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Align speech audio to text script')
    parser.add_argument('audio_file', help='Path to the .wav audio file')
    parser.add_argument('script_file', help='Path to the text script file')
    parser.add_argument('--output', default='alignment_results.json', help='Output JSON file path')
    
    args = parser.parse_args()
    
    # Read the script
    with open(args.script_file, 'r', encoding='utf-8') as f:
        script = f.read()
    
    model = stable_whisper.load_model('base')
    result = model.align('cleaned_output1.mp3', script, language='en')
    print(result)
    result.to_srt_vtt('helloword.srt')

    # Align speech to text -- commented out bellow
    # alignment_results = align_speech_to_text(args.audio_file, script)
    
    # # Write results to JSON file
    # with open(args.output, 'w', encoding='utf-8') as f:
    #     json.dump(alignment_results, f, indent=2)
    
    # print(f"Alignment results saved to {args.output}")
    
    # # Print a sample of the results
    # print("\nSample alignment results:")
    # for i, result in enumerate(alignment_results[:5]):
    #     print(f"{result['phrase']}: {result['start_time']:.2f}s - {result['end_time']:.2f}s")



    