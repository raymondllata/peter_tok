# PeterTok

A tool for generating short-form content videos with character voice impersonations.

## Overview

PeterTok automatically generates entertaining short-form videos where famous characters explain various topics. The system:

1. Uses Mistral AI to generate scripts in a character's voice/style
2. Synthesizes audio using Fish Audio API for voice cloning
3. Creates captions synchronized with the audio
4. Combines everything into a final video with branding

## Setup and Installation

### Requirements

- [Conda](https://docs.conda.io/en/latest/) for environment management
- [Fish Audio API Key](https://fish.audio/) - for voice synthesis
- [Mistral API Key](https://mistral.ai/) - for script generation

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/raymondllata/peter_tok.git
   cd peter_tok
   ```

2. Create and activate the conda environment using the provided `environment.yml` file:
   ```
   conda env create -f environment.yml
   conda activate peter_tok
   ```

3. Create a `.env` file in the main directory with your API keys:
   ```
   fish_api=your_fish_audio_api_key_here
   MISTRAL_API_KEY=your_mistral_api_key_here
   ```

4. Ensure all required directories exist:
   ```
   mkdir -p audio_model_output caption_model_output final_product_output
   ```

## Usage

1. Make sure you're in the main PeterTok directory
2. Activate the conda environment if not already active:
   ```
   conda activate peter_tok
   ```
3. Run the application:
   ```
   python3 peter_tok.py
   ```
4. Follow the interactive prompts to:
   - Select a character
   - Choose a topic for the script
   - Wait while the system generates the content

5. Find your completed video in the `final_product_output` folder

## How It Works

1. **Script Generation**: Uses MistralAI to create a script in the chosen character's style
2. **Voice Synthesis**: Utilizes Fish Audio API to generate character voice
3. **Caption Creation**: Aligns text with audio to create accurate subtitles
4. **Video Assembly**: Combines background video, synthesized audio, captions, and branding

## Adding New Characters

To add a new character to the system:

1. Check the README file in the `audio_training_data` folder for detailed instructions
2. You'll need to:
   - Collect clean audio samples of the character
   - Process training data using Fish Audio tools
   - Add character information to the models registry

## Planned Updates

- **Auto-Generated Graphics**: Automatically pull suitable photos and graphics to integrate into the generated reels
- **Improved Caption Alignment**: Enhanced synchronization between audio and captions
- **Extended Character Library**: Support for a growing list of character voices

## Project Structure

- `agent.py`: Manages interactions with the Mistral AI for script generation
- `create_captions.py`: Creates and aligns captions with audio
- `environment.yml`: Conda environment configuration
- `fish/`: Directory containing Fish Audio API integration
  - `fuzzy_json.py`: Utility for fuzzy matching character names
  - `model_gen_fish.py`: Handles Fish Audio model generation
  - `models.json`: Registry of trained voice models
  - `speech_gen_fish.py`: Generates speech from text using Fish Audio
- `peter_tok.py`: Main application entry point
- `vid_gen_srt.py`: Assembles the final video with all components

## Troubleshooting

- **API Errors**: Ensure your API keys are correctly set in the `.env` file
- **Missing Directories**: Make sure all required directories exist
- **Audio Issues**: Check that audio files are in supported formats (MP3/WAV)

## Demo

### Option 1: Link to MP4 in the repository

You can view a demo of PeterTok in action [here](https://github.com/raymondllata/peter_tok/blob/main/final_product_output/Peter%20Griffin_c27ad494a5992529f688fe96a77e7a6b.mp4).

*Note: Be aware that GitHub has file size limits (typically 100MB), so you may need to compress your video.*

## License

MIT License

Copyright (c) 2025 Raymond Llata

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Acknowledgements

- Fish Audio for voice synthesis capabilities
- Mistral AI for text generation