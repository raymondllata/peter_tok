import os
import wave
import contextlib
import numpy as np
import re
from moviepy import VideoFileClip, AudioFileClip, CompositeVideoClip, TextClip, ImageClip
from pydub import AudioSegment
import tempfile
from PIL import Image

def get_image_dimensions(image_path):
    """Get the width and height of an image file."""
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            return width, height
    except Exception as e:
        print(f"Error getting image dimensions: {e}")
        return None, None

def get_audio_duration(audio_path):
    """Get the duration of an audio file in seconds."""
    try:
        with contextlib.closing(wave.open(audio_path, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
            return duration
    except Exception as e:
        print(f"Error reading WAV file: {e}")
        # Fallback to using pydub
        audio = AudioSegment.from_file(audio_path)
        duration = len(audio) / 1000.0  # pydub duration is in milliseconds
        return duration

def parse_srt_file(srt_path):
    """
    Parse an SRT file and return a list of subtitle entries.
    Each entry is a tuple of (start_time, end_time, text).
    Handles and removes font color tags.
    """
    with open(srt_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Split the content by subtitle entries (double newline)
    entries = re.split(r'\n\n+', content.strip())
    subtitles = []
    
    for entry in entries:
        lines = entry.strip().split('\n')
        if len(lines) < 3:
            continue  # Skip malformed entries
            
        # Parse the timestamp line
        timestamp_line = lines[1]
        timestamp_match = re.match(r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})', timestamp_line)
        
        if not timestamp_match:
            continue  # Skip entries with invalid timestamps
            
        start_time_str, end_time_str = timestamp_match.groups()
        
        # Convert timestamp strings to seconds
        start_time = convert_timestamp_to_seconds(start_time_str)
        end_time = convert_timestamp_to_seconds(end_time_str)
        
        # Get the subtitle text and remove HTML font tags
        text = ' '.join(lines[2:])
        
        # Remove font color tags (like <font color="#00ff00">word</font>)
        text = re.sub(r'<font color="[^"]*">', '', text)
        text = re.sub(r'</font>', '', text)
        
        # Wrap long text (more than 40 characters) to improve readability
        wrapped_text = text
        if len(text) > 40:
            # Find a space near the middle to break the line
            mid_point = len(text) // 2
            space_index = text.find(' ', mid_point)
            if space_index != -1:
                wrapped_text = text[:space_index] + '\n' + text[space_index+1:]
        
        subtitles.append((start_time, end_time, wrapped_text))
    
    # print(subtitles)
    return subtitles

def convert_timestamp_to_seconds(timestamp):
    """Convert an SRT timestamp (HH:MM:SS,mmm) to seconds."""
    hours, minutes, rest = timestamp.split(':')
    seconds, milliseconds = rest.split(',')
    
    total_seconds = (
        int(hours) * 3600 + 
        int(minutes) * 60 + 
        int(seconds) + 
        int(milliseconds) / 1000
    )
    
    return total_seconds

def create_caption_clips(subtitles, video_width, video_height):
    """Create text clips for each subtitle entry with proper timing and positioning."""
    text_clips = []
    
    for start_time, end_time, text in subtitles:
        try:
            # Create the text clip with all necessary properties
            text_clip = TextClip(
                text=text,
                font_size=60,  # Slightly smaller font size for better fit
                size=(int(video_width * 0.8), int(video_height * 0.2)),
                font="Arial",  # Bold for better readability
                color="white",
                bg_color=None,
                stroke_color="black",
                stroke_width=2,
                method="caption",  # Use caption method which handles multiline better
                text_align="center",  # Center-align text
                horizontal_align="center",
                vertical_align="center",
                interline=-1  # Slightly tighter line spacing
            )
            
            # Set duration and start time
            
            text_clip = text_clip.with_duration(end_time - start_time)
            text_clip = text_clip.with_start(start_time)
            
            # Position at the bottom center of the frame
            text_clip = text_clip.with_position(('center', 'center'))
            
            text_clips.append(text_clip)
        except Exception as e:
            print(f"Error creating clip for text '{text}': {e}")
            continue
    
    return text_clips

def overlay_audio_and_add_captions(video_path, audio_path, srt_path, output_path, logo_path, logo_size = None):
    """
    Overlay audio on video and add captions from an SRT file.
    """
    try:
        # Load video
        print(f"Loading video from {video_path}...")
        video_clip = VideoFileClip(video_path)
        video_width, video_height = video_clip.size
        
        # Load audio and get duration
        print(f"Loading audio from {audio_path}...")
        try:
            # Try to get audio duration directly from the file
            audio_duration = get_audio_duration(audio_path)
            print(f"Audio duration from wave file: {audio_duration} seconds")
            
            # Then load the audio clip
            audio_clip = AudioFileClip(audio_path)
        except Exception as e:
            print(f"Error getting audio duration from wave file: {e}")
            print("Trying alternate method...")
            
            # If WAV file duration reading fails, try using pydub
            try:
                audio_segment = AudioSegment.from_file(audio_path)
                audio_duration = len(audio_segment) / 1000.0  # Convert ms to seconds
                print(f"Audio duration from pydub: {audio_duration} seconds")
                
                # Create a temporary file that MoviePy can read
                temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
                temp_filename = temp_file.name
                temp_file.close()
                
                # Export to the temporary file
                audio_segment.export(temp_filename, format="wav")
                
                # Load the audio clip from the temporary file
                audio_clip = AudioFileClip(temp_filename)
                # Clean up temp file later
            except Exception as audio_err:
                print(f"Error loading audio with pydub: {audio_err}")
                raise
        
        # Replace video's audio with the new audio
        print("Combining video and audio...")
        video_with_audio = video_clip.with_audio(audio_clip)
        
        # Parse SRT file to get subtitles
        print(f"Parsing subtitles from {srt_path}...")
        subtitles = parse_srt_file(srt_path)

        clips = [video_with_audio]

        # Add logo if specified
        if logo_path and os.path.exists(logo_path):
            try:
                print(f"Adding logo from {logo_path}...")
                logo_clip = ImageClip(logo_path)
                
                # Resize logo if size is specified
                if logo_size:
                    new_height = 0.4 * video_height
                    ratio =  new_height / logo_size[1]
                    new_width = ratio * logo_size[0]
                    logo_clip = logo_clip.resized(width=new_width, height=new_height)
                else:
                    logo_clip = logo_clip.resized(width=video_width * 0.25, height=video_height * 0.25)
                
                # Position logo at bottom left with some padding
                logo_clip = logo_clip.with_position((20, video_height - logo_clip.h))
                
                # Set logo duration to match the video
                logo_clip = logo_clip.with_duration(video_with_audio.duration)
                
                # Add logo to clips list
                clips.append(logo_clip)
                print("Logo added successfully.")
            except Exception as logo_err:
                print(f"Error adding logo: {logo_err}")
        
        # Add captions if available
        if not subtitles:
            print("Warning: No subtitles were found in the SRT file.")
        else:
            # Create text clips for each subtitle
            print("Creating caption clips...")
            text_clips = create_caption_clips(subtitles, video_width, video_height)
            
            if not text_clips:
                print("Warning: No caption clips were created.")
            else:
                # Add text clips to the clips list
                print(f"Adding {len(text_clips)} caption clips to video...")
                clips.extend(text_clips)
        
        # Create final composite video with all elements
        final_clip = CompositeVideoClip(clips, size=(video_width, video_height))
        
        # Ensure the final clip duration is set correctly
        final_clip = final_clip.with_duration(min(video_with_audio.duration, audio_duration))
        
        # Write output file
        print(f"Rendering output to {output_path}...")
        final_clip.write_videofile(output_path, codec='libx264', 
                                  audio_codec='aac', fps=24)
        
        # Close clips to free resources
        video_clip.close()
        audio_clip.close()
        if 'video_with_audio' in locals():
            video_with_audio.close()
        if 'logo_clip' in locals():
            logo_clip.close()
        if 'final_clip' in locals() and final_clip is not video_clip:
            final_clip.close()
            
        # Clean up temporary files
        if 'temp_filename' in locals() and os.path.exists(temp_filename):
            os.remove(temp_filename)
        
        print("Done!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


def remote_main(video_path, audio_path, srt_path, output_path, logo_path):

    logo_size = None
    if os.path.exists(logo_path):
        original_width, original_height = get_image_dimensions(logo_path)
        print(f"Logo dimensions: {original_width}x{original_height} pixels")
        logo_size = (original_width, original_height)

    overlay_audio_and_add_captions(video_path, audio_path, srt_path, output_path, logo_path, logo_size)


def main():
    # File paths
    video_path = "video/test-video-five.mp4"  # Update with your actual video path
    audio_path = "audio_model_output/Peter Griffin_01ef0317c9.mp3"  # Update with your actual audio path
    srt_path = "caption_model_output/Peter Griffin_01ef0317c9.srt"  # Update with your actual SRT file path
    output_path = "final_product_output/Peter Griffin_01ef0317c9.mp4"

    logo_path = "logos/Peter Griffin.png"
    logo_size = None
    if os.path.exists(logo_path):
        original_width, original_height = get_image_dimensions(logo_path)
        print(f"Logo dimensions: {original_width}x{original_height} pixels")
        logo_size = (original_width, original_height)

    overlay_audio_and_add_captions(video_path, audio_path, srt_path, output_path, logo_path, logo_size)

if __name__ == "__main__":
    main()