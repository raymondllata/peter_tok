# Voice Cloning Setup Instructions

## Overview

This guide explains how to prepare audio clips for voice cloning with the Fish API. You'll learn how to collect audio clips, process them, and create a single training file.

## Prerequisites

- FFmpeg installed on your system
- Fish API key set up in your `.env` file
- Basic familiarity with terminal commands

## Step 1: Prepare Your Audio Clips

1. Collect high-quality voice clips of the person/character you want to clone
2. Make sure the clips:
   - Are in MP3 format
   - Contain only the target voice (no background noise or music)
   - Are clear and consistent in audio quality
   - Range from 30 seconds to 5 minutes in total length (more is better)

## Step 2: Organize Your Files

1. Place all your MP3 audio clips in the `audio_training_data` directory
2. Make sure there are no other files in this directory except your MP3 clips

```
project/
├── audio_training_data/
│   ├── clip1.mp3
│   ├── clip2.mp3
│   ├── clip3.mp3
│   └── concat_audio.sh
└── ...
```

## Step 3: Run the Concatenation Script

1. Open your terminal
2. Navigate to the `audio_training_data` directory
3. Run the concatenation script:

```bash
cd audio_training_data
./concat_audio.sh
```

This script will:
- Convert all MP3 files to WAV format
- Concatenate them into a single file called `training_voice.wav`
- Clean up temporary files automatically

## Troubleshooting

- If you encounter errors with special characters in filenames, rename your files to use only letters, numbers, and underscores
- Make sure all audio clips are in MP3 format
- Verify that FFmpeg is properly installed on your system

## Best Practices

- Use high-quality audio with minimal background noise
- Provide diverse vocal samples (different emotions, speaking speeds, etc.)
- For best results, aim for at least 2-3 minutes of clean audio
- Avoid very short clips (less than 5 seconds each)