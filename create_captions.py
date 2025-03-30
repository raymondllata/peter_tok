import os
import wave
import contextlib
import numpy as np
from moviepy import TextClip
import re
from pydub import AudioSegment
import tempfile
from vosk import Model, KaldiRecognizer, SetLogLevel
# import librosa
import json
import sys
import stable_whisper

# def get_audio_duration(audio_path):
#     """Get the duration of an audio file in seconds."""
#     try:
#         with contextlib.closing(wave.open(audio_path, 'r')) as f:
#             frames = f.getnframes()
#             rate = f.getframerate()
#             duration = frames / float(rate)
#             return duration
#     except Exception as e:
#         print(f"Error reading WAV file: {e}")
#         # Fallback to using pydub
#         audio = AudioSegment.from_file(audio_path)
#         duration = len(audio) / 1000.0  # pydub duration is in milliseconds
#         return duration

# def generate_timestamps_from_script(script, audio_duration):
#     """
#     Generate timestamps for each word in the script based on audio duration.
#     Returns list of (word, start_time, end_time) tuples.
#     """
#     # Clean the script text
#     script = script.strip()
    
#     # Handle special markers
#     script = re.sub(r'\(break\)', ' ', script)
#     script = re.sub(r'\(long-break\)', ' ', script)
#     script = re.sub(r'\(laugh\)', ' ', script)
    
#     # Split into words and clean
#     words = []
#     for line in script.split('\n'):
#         line = line.strip()
#         if line:
#             line_words = [w for w in re.split(r'[\s.]+', line) if w]
#             words.extend(line_words)
    
#     # Remove empty words and punctuation-only words
#     words = [word for word in words if word and not re.match(r'^[.,;:!?]*$', word)]
    
#     # Calculate times
#     total_words = len(words)
#     avg_word_duration = audio_duration / total_words
    
#     # Create timestamps
#     result = []
#     current_time = 0.0
    
#     for word in words:
#         # Adjust duration based on word length (longer words take more time)
#         word_duration = avg_word_duration * (0.5 + (len(word) / 5))
        
#         # Add a small gap between words
#         end_time = current_time + word_duration
        
#         result.append((word, current_time, end_time))
#         current_time = end_time + 0.05  # small gap between words
    
#     return result

# def create_caption_clips(timestamps, video_width, video_height):
#     """Create text clips for each word in the script with proper timing and positioning."""
#     text_clips = []
    
#     for word, start_time, end_time in timestamps:
#         try:
#             # Create the text clip with all necessary properties
#             text_clip = TextClip(
#                 text=word,
#                 font_size=70, 
#                 font="Arial",
#                 color="white",
#                 bg_color=None,
#                 stroke_color="black",
#                 stroke_width=2,
#                 method="label"
#             )
            
#             # Set duration and start time
#             text_clip = text_clip.with_duration(end_time - start_time)
            
#             text_clip = text_clip.with_start(start_time)
            
#             # Position at the bottom center of the frame
#             #text_clip = text_clip.set_position(('center', 'bottom'))
            
#             text_clips.append(text_clip)
#         except Exception as e:
#             print(f"Error creating clip for word '{word}': {e}")
#             continue
    
#     return text_clips

# def break_into_phrases(script, max_words=4):
#     """Break a script into phrases of at most max_words words."""
#     words = script.split()
#     phrases = []
    
#     for i in range(0, len(words), max_words):
#         phrase = ' '.join(words[i:i+max_words])
#         phrases.append(phrase)
    
#     return phrases

# def clean_word_timestamps_enhanced(word_time_map, total_duration, script_words=None):
#     """
#     More robust function to clean up word timestamps, especially when there are severe 
#     ordering issues. Optionally uses the expected word order from a script.
    
#     Parameters:
#     word_time_map (dict): Dictionary with words as keys and tuples of (start_time, end_time) as values
#     total_duration (float): Total duration of the audio/video in seconds
#     script_words (list, optional): The expected order of words from the script
    
#     Returns:
#     dict: Cleaned dictionary with corrected timestamps
#     """
#     # Step 1: Group words into sequences
#     # Convert to list of (word, start_time, end_time) sorted by start_time
#     word_times = [(word, start, end) for word, (start, end) in word_time_map.items()]
#     word_times.sort(key=lambda x: x[1])
    
#     # First pass: Identify sequences of timestamps using a reasonable threshold
#     sequences = []
#     current_sequence = [word_times[0]]
#     max_jump_threshold = 1.5  # Maximum allowed time jump in seconds
    
#     for i in range(1, len(word_times)):
#         prev_word, prev_start, prev_end = current_sequence[-1]
#         curr_word, curr_start, curr_end = word_times[i]
        
#         # If the current start time is reasonably close to the previous end time,
#         # consider it part of the same sequence
#         if curr_start >= prev_start and (curr_start - prev_end) < max_jump_threshold:
#             current_sequence.append(word_times[i])
#         else:
#             # Start a new sequence
#             sequences.append(current_sequence)
#             current_sequence = [word_times[i]]
    
#     # Add the last sequence
#     if current_sequence:
#         sequences.append(current_sequence)
    
#     # Step 2: Analyze and reposition the sequences
    
#     # Sort sequences by length (assuming longer sequences are more reliable)
#     sequences.sort(key=len, reverse=True)
    
#     # If we have a script to use as reference, use it to help order the sequences
#     ordered_sequences = []
#     if script_words:
#         # For each script word, try to find it in our sequences
#         script_word_index = {}
#         for i, word in enumerate(script_words):
#             script_word_index[word.lower()] = i
        
#         # Calculate average script position for each sequence
#         for seq in sequences:
#             positions = []
#             for word, _, _ in seq:
#                 if word.lower() in script_word_index:
#                     positions.append(script_word_index[word.lower()])
            
#             # If we have positions, use their average to order this sequence
#             if positions:
#                 avg_pos = sum(positions) / len(positions)
#                 ordered_sequences.append((seq, avg_pos))
#             else:
#                 # Use the start time as a fallback ordering method
#                 avg_time = sum(item[1] for item in seq) / len(seq)
#                 rel_pos = avg_time / total_duration * len(script_words)
#                 ordered_sequences.append((seq, rel_pos))
        
#         # Sort sequences by their script position
#         ordered_sequences.sort(key=lambda x: x[1])
#         sequences = [seq for seq, _ in ordered_sequences]
#     else:
#         # Without a script, try to order by average timestamp
#         sequences_with_timing = []
#         for seq in sequences:
#             avg_time = sum(item[1] for item in seq) / len(seq)
#             sequences_with_timing.append((seq, avg_time))
        
#         sequences_with_timing.sort(key=lambda x: x[1])
#         sequences = [seq for seq, _ in sequences_with_timing]
    
#     # Step 3: Reconstruct a proper timeline
#     corrected_map = {}
#     current_time = 0.0
#     min_word_spacing = 0.05  # Minimum space between words in seconds
    
#     for sequence in sequences:
#         # Calculate sequence duration based on its current timestamps
#         if len(sequence) > 0:
#             seq_start = sequence[0][1]
#             seq_end = sequence[-1][2]
#             seq_duration = seq_end - seq_start
            
#             # Preserve relative durations within the sequence
#             for word, orig_start, orig_end in sequence:
#                 # Calculate the relative position within the sequence
#                 if seq_duration > 0:
#                     rel_pos = (orig_start - seq_start) / seq_duration
#                 else:
#                     rel_pos = 0
                
#                 # Calculate the word duration
#                 word_duration = orig_end - orig_start
                
#                 # Place the word at its new position
#                 new_start = current_time + (rel_pos * seq_duration)
#                 new_end = new_start + word_duration
                
#                 corrected_map[word] = (new_start, new_end)
            
#             # Update the current time for the next sequence
#             current_time = max(current_time, corrected_map[sequence[-1][0]][1]) + min_word_spacing
    
#     # Step 4: Final validation - ensure no overlaps and nothing exceeds total duration
#     # Convert to list and sort by start time
#     corrected_items = [(word, start, end) for word, (start, end) in corrected_map.items()]
#     corrected_items.sort(key=lambda x: x[1])
    
#     final_map = {}
#     current_end = 0
    
#     for word, start, end in corrected_items:
#         # Ensure no overlap with previous word
#         if start < current_end:
#             start = current_end + min_word_spacing
#             end = start + (end - start)
        
#         # Ensure we don't exceed total duration
#         if end > total_duration:
#             # Scale everything down proportionally
#             scale_factor = 0.95 * total_duration / end
#             start *= scale_factor
#             end *= scale_factor
        
#         final_map[word] = (start, end)
#         current_end = end
    
#     return final_map

# def align_speech_to_text(audio_file, script):
#     """
#     Aligns speech audio to text script and returns timestamps for phrases.
    
#     Parameters:
#     audio_file (str): Path to the .wav audio file
#     script (str): The text script that matches the audio
    
#     Returns:
#     list: List of dictionaries with phrases and their timestamps
#     """
#     # Set log level to suppress unnecessary messages
#     SetLogLevel(-1)
    
#     # Load a pre-trained model (you'll need to download this)
#     # For English, download from: https://alphacephei.com/vosk/models
#     # model = Model("vosk-model-small-en-us-0.15")
#     model = Model("vosk-model-en-us-0.22")
    
#     # Check file extension to determine format
#     _, file_ext = os.path.splitext(audio_file)
#     temp_wav_file = None
    
#     # If not a WAV file, convert it
#     if file_ext.lower() != '.wav':
#         print(f"Converting {file_ext} file to WAV format...")
#         try:
#             # Create a temporary file for the WAV conversion
#             temp_fd, temp_wav_file = tempfile.mkstemp(suffix='.wav')
#             os.close(temp_fd)
            
#             # Convert using pydub
#             audio = AudioSegment.from_file(audio_file)
#             # Convert to mono and set sample width to 2 bytes (16 bit)
#             audio = audio.set_channels(1).set_sample_width(2)
#             audio.export(temp_wav_file, format="wav")
#             # audio.export("testing.wav", format="wav")
            
#             # Use the temporary WAV file for processing
#             wf = wave.open(temp_wav_file, "rb")
#             print("Conversion successful.")
#         except Exception as e:
#             print(f"Error converting audio file: {e}")
#             if temp_wav_file and os.path.exists(temp_wav_file):
#                 os.unlink(temp_wav_file)
#             sys.exit(1)
#     else:
#         # Open the WAV file directly
#         wf = wave.open(audio_file, "rb")
        
#         # Check if the audio format is compatible with the model
#         if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
#             print("WAV file must be mono PCM format. Converting automatically...")
#             try:
#                 # Create a temporary file for the properly formatted WAV
#                 temp_fd, temp_wav_file = tempfile.mkstemp(suffix='.wav')
#                 os.close(temp_fd)
                
#                 # Convert using pydub
#                 audio = AudioSegment.from_wav(audio_file)
#                 audio = audio.set_channels(1).set_sample_width(2)
#                 audio.export(temp_wav_file, format="wav")
                
#                 # Close the original file and open the converted one
#                 wf.close()
#                 wf = wave.open(temp_wav_file, "rb")
#                 print("Conversion successful.")
#             except Exception as e:
#                 print(f"Error converting WAV file: {e}")
#                 if temp_wav_file and os.path.exists(temp_wav_file):
#                     os.unlink(temp_wav_file)
#                 sys.exit(1)
    
#     # Create a recognizer
#     recognizer = KaldiRecognizer(model, wf.getframerate())
#     recognizer.SetWords(True)
    
#     # Break the script into phrases
#     phrases = break_into_phrases(script)
    
#     # Dictionary to store phrase timestamps
#     phrase_timestamps = []
    
#     # Process the audio file
#     while True:
#         data = wf.readframes(4000)
#         if len(data) == 0:
#             break
#         if recognizer.AcceptWaveform(data):
#             pass
    
#     # Get the final result
#     result = json.loads(recognizer.FinalResult())
    
#     # Extract word timestamps
#     words_with_times = result.get("result", [])
#     # print(words_with_times)
    
#     # Create a dictionary with word -> time mapping
#     word_time_map = {word["word"]: (word["start"], word["end"]) for word in words_with_times}
#     # print(word_time_map)
#     maxTime = max(max(word_time_map[key][0], word_time_map[key][1]) for key in word_time_map)
#     tmp_script = ""
#     for word in words_with_times:

#         tmp_script += word["word"]
#     clean_map = clean_word_timestamps_enhanced(word_time_map, maxTime, tmp_script)
#     print(clean_map)
    
#     # Function to find the best match between recognized words and script phrases
#     def find_phrase_timestamps(phrases, word_time_map):
#         results = []
        
#         for phrase in phrases:
#             # Clean the phrase to match recognized format
#             clean_phrase = re.sub(r'[^\w\s]', '', phrase.lower())
#             words_in_phrase = clean_phrase.split()
            
#             # Look for the first and last word in the phrase
#             if words_in_phrase:
#                 first_word = words_in_phrase[0]
#                 last_word = words_in_phrase[-1]
                
#                 # Find the closest match in recognized words
#                 start_time = None
#                 end_time = None
                
#                 for word in word_time_map:
#                     if word.startswith(first_word) or first_word.startswith(word):
#                         start_time = word_time_map[word][0]
#                         break
                
#                 for word in word_time_map:
#                     if word.startswith(last_word) or last_word.startswith(word):
#                         end_time = word_time_map[word][1]
#                         # Continue searching to find the last occurrence
                
#                 if start_time is not None and end_time is not None:
#                     results.append({
#                         "phrase": phrase,
#                         "start_time": start_time,
#                         "end_time": end_time
#                     })
#                 else:
#                     # Fallback for phrases not found
#                     results.append({
#                         "phrase": phrase,
#                         "start_time": None,
#                         "end_time": None
#                     })
            
#         return results
    
#     # Get timestamps for each phrase
#     alignment_results = find_phrase_timestamps(phrases, clean_map)
    
#     # Post-process to fix missing timestamps by interpolation
#     def interpolate_timestamps(results):
#         # Find the first and last valid timestamps
#         valid_indices = [i for i, res in enumerate(results) if res["start_time"] is not None]
        
#         if not valid_indices:
#             return results
        
#         first_valid = valid_indices[0]
#         last_valid = valid_indices[-1]
        
#         # Fix missing timestamps by linear interpolation
#         for i in range(len(results)):
#             if results[i]["start_time"] is None:
#                 # Find nearest valid timestamps before and after
#                 before = next((j for j in range(i-1, -1, -1) if results[j]["start_time"] is not None), None)
#                 after = next((j for j in range(i+1, len(results)) if results[j]["start_time"] is not None), None)
                
#                 if before is not None and after is not None:
#                     # Interpolate
#                     weight = (i - before) / (after - before)
#                     start_before = results[before]["start_time"]
#                     start_after = results[after]["start_time"]
#                     end_before = results[before]["end_time"]
#                     end_after = results[after]["end_time"]
                    
#                     results[i]["start_time"] = start_before + weight * (start_after - start_before)
#                     results[i]["end_time"] = end_before + weight * (end_after - end_before)
#                 elif before is not None and i > first_valid:
#                     # Extrapolate from previous
#                     results[i]["start_time"] = results[before]["end_time"]
#                     results[i]["end_time"] = results[before]["end_time"] + 1.0  # Estimate 1 second
#                 elif after is not None and i < last_valid:
#                     # Extrapolate from next
#                     results[i]["start_time"] = results[after]["start_time"] - 1.0  # Estimate 1 second
#                     results[i]["end_time"] = results[after]["start_time"]
        
#         return results
    
#     return interpolate_timestamps(alignment_results)

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



    