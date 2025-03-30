#!/bin/bash

# Create a temporary directory for working files
TEMP_DIR="$(mktemp -d)"
echo "Created temporary directory: $TEMP_DIR"

# Create a temporary file listing all MP3 files
CONCAT_LIST="$TEMP_DIR/concat_list.txt"
touch "$CONCAT_LIST"

# Track the number of files processed
COUNT=0

# Process each MP3 file
for file in *.mp3; do
    # Skip if no files match the pattern
    [ -e "$file" ] || continue
    
    COUNT=$((COUNT+1))
    # Create a simple numbered filename to avoid special character issues
    wav_file="$TEMP_DIR/${COUNT}.wav"
    
    echo "Converting: $file to $wav_file"
    ffmpeg -i "$file" -acodec pcm_s16le "$wav_file"
    
    # Add the converted WAV file to the list (with proper escaping)
    echo "file '$wav_file'" >> "$CONCAT_LIST"
done


# Create output directory if it doesn't exist
mkdir -p output

# Ask for output filename
echo "Enter the output filename (default: new_char.wav):"
read user_filename

# Use the provided name or the default if nothing was entered
filename=${user_filename:-new_char.wav}

# Set the full output path in the output directory
OUTPUT_FILE="output/$filename"

echo "Output will be saved as: $OUTPUT_FILE"

# Concatenate all converted files in the list to create a new WAV file
echo "Concatenating files to $OUTPUT_FILE..."
ffmpeg -f concat -safe 0 -i "$CONCAT_LIST" -c copy "$OUTPUT_FILE"

# Check if concatenation was successful
if [ $? -eq 0 ]; then
    echo "Successfully created $OUTPUT_FILE with $COUNT audio clips"
else
    echo "Error: Failed to concatenate audio files"
fi

# Clean up
echo "Cleaning up temporary files..."
rm -rf "$TEMP_DIR"
rm concat_list.txt

echo "All done! Output is in $OUTPUT_FILE"