# LLM-VERSE-voice-assistant

## Overview

This AI Voice Assistant is a powerful and intelligent voice-controlled assistant designed to provide a seamless user experience. It is built using advanced AI models, including Gemini 1.5 Flash and LLaMA 3-70b-8192 (through groq api), and incorporates speech recognition, text-to-speech, and multimodal capabilities. This project is especially useful for individuals with disabilities, as it allows hands-free operation and responds to voice commands. It only requires an internet connection and can even run efficiently on a low-end system like an Intel i3 processor.

LLMs are notorious for their high system reqirements and time consuming processing time, this project provides a refreshing and innovatively method to run massive LLMs like the llama 70b on systems with even very low processing power. In fact the entire code and execution was done on cpu(i3) allowing us to now use 

## Features

- **Voice Activation**: Wake word-based activation using speech recognition.
- **Multimodal Capabilities**: Processes screenshots, webcam captures, and clipboard text for contextual responses.
- **Web Browsing**: Opens websites based on voice commands.
- **Clipboard Integration**: Reads and utilizes clipboard content in responses.
- **Screen Capture**: Takes screenshots to provide visual context.
- **Camera Integration**: Captures webcam images for enhanced context.
- **Conversational AI**: Uses Groq's LLaMA3-70B and Gemini 1.5 Flash models for intelligent responses.
- **Text-to-Speech**: Speaks responses back to the user for an interactive experience.
- **Low System Requirements**: Runs smoothly even on an Intel i3 processor.

## Installation

### Prerequisites

Ensure you have the following installed:

- **Python 3.8+**
- **Required Python libraries** (install using the command below):
  ```sh
  pip install asyncio groq google-generativeai pyperclip opencv-python pillow SpeechRecognition edge-tts webbrowser pygame
  ```

## Usage

1. **Run the script:**
   ```sh
   python chatbot.py
   ```
2. **Activate the assistant:** Say the wake word "Friday" followed by your command.
3. **Perform tasks:**
   - **"Take a screenshot"** → Captures a screenshot and analyzes its content.
   - **"Capture webcam"** → Captures an image using the webcam.
   - **"Open [website]"** → Opens the specified website in the browser.
   - **"Read clipboard"** → Processes copied text for contextual responses.
4. **Receive spoken responses:** The assistant will speak back the generated response.

## Example Commands

- "Friday, what is on my screen?"
- "Friday, open YouTube."
- "Friday, summarize my clipboard content."
- "Friday, take a picture from my webcam."

## Technical Details

- **Speech Recognition**: Uses `speech_recognition` for converting spoken input to text.
- **Text Generation**: Uses Groq’s LLaMA3-70B and Google Gemini 1.5 Flash for intelligent responses.
- **Vision Processing**: Uses OpenCV and PIL for image handling and analysis.
- **Text-to-Speech**: Converts AI-generated responses into spoken output.

## Why This Assistant?

- **Accessibility**: Ideal for users with disabilities as it provides a hands-free experience.
- **Lightweight**: Runs efficiently even on low-end hardware like an i3 processor.
- **AI-Powered**: Uses state-of-the-art language and vision models.
- **Simple Setup**: Requires only Python and an internet connection.

## Future Enhancements

- Adding support for more voice commands.
- Implementing a GUI for easier interaction.
- Integrating with smart home devices.
- Offline functionality for limited features.

## Contributing

Contributions are welcome! Feel free to fork this repository and submit pull requests with improvements or bug fixes.

## License

This project is open-source and available.

## Acknowledgments

- **Google Gemini AI**
- **Groq AI**
- **OpenCV**
- **SpeechRecognition**
- **Python Community**

