import asyncio
from groq import Groq
from PIL import ImageGrab,Image
import google.generativeai as genai
import pyperclip
import cv2
from tts import speak
import speech_recognition as sr
import os
import time
import re
from talk import play
import webbrowser


s=0
wake_word='friday'
web_cam=cv2.VideoCapture(1)
genai.configure(api_key='YOUR-GEMINI-API-KEY') #gemini 1.5 flash
groq_client=Groq(api_key="YOUR-GROQ-API-KEY")
model = 'whisper-large-v3'
sys_msg = (
    'You are a multi-modal AI voice assistant. Your user may or may not have attached a photo for context '
    '(either a screenshot or a webcam capture). Any photo has already been processed into a highly detailed '
    'text prompt that will be attached to their transcribed voice prompt. Generate the most useful and '
    'factual response possible, carefully considering all previous generated text in your response before '
    'adding new tokens to the response. Do not expect or request images, just use the context if added. '
    'Use all of the context of this conversation so your response is relevant to the conversation. Make '
    'your responses clear and concise, avoiding any verbosity.'
)

convo = [{'role': 'system', 'content': sys_msg}]


generation_config = {
    'temperature': 0.7,
    'top_p': 1,
    'top_k': 1,
    'max_output_tokens': 2048
}

safety_settings = [
    {
        'category': 'HARM_CATEGORY_HARASSMENT',
        'threshold': 'BLOCK_NONE'
    },
    {
        'category': 'HARM_CATEGORY_HATE_SPEECH',
        'threshold': 'BLOCK_NONE'
    },
    {
        'category': 'HARM_CATEGORY_SEXUALLY_EXPLICIT',
        'threshold': 'BLOCK_NONE'
    },
    {
        'category': 'HARM_CATEGORY_DANGEROUS_CONTENT',
        'threshold': 'BLOCK_NONE'
    },
]

model=genai.GenerativeModel('gemini-1.5-flash-latest',
                            generation_config=generation_config,
                            safety_settings=safety_settings)


r=sr.Recognizer()
source=sr.Microphone()

def groq_prompt(prompt,img_context):
    if img_context:
        prompt=f'USER_CONTENT: {prompt}\n\n IMAGE CONTEXT:{img_context}'
    convo.append({'role': 'user', 'content': prompt})
    chat_completion=groq_client.chat.completions.create(messages=convo,model='llama3-70b-8192')
    response=chat_completion.choices[0].message
    convo.append(response)
    return response.content

def function_call(prompt):
    sys_msg = (
        'You are an AI function calling model. You will determine whether extracting the users clipboard content, '
        'taking a screenshot, capturing the webcam or calling no functions is best for a voice assistant to respond '
        'to the users prompt. The webcam can be assumed to be a normal laptop webcam facing the user. You will '
        'respond with only one selection from this list: ["extract clipboard", "take screenshot", "capture webcam",  "open website", "None"] \n'
        'When "open website"(only when expressly asked to open website) is chosen, do not talk about how to open it YOU ALREADY HAVE, give general information about it instead'
        'Do not respond with anything but the most logical selection from that list with no explanations. Format the '
        'function call name exactly as I listed.'
    )

    function_convo=[{'role':'system','content':sys_msg},
                    {'role':'user','content': prompt}]
    chat_completion=groq_client.chat.completions.create(messages=function_convo,model='llama3-70b-8192')
    response=chat_completion.choices[0].message

    return response.content

def take_screenshot():
    path=r'C:\Users\Happy Home\OneDrive\Desktop\hackathon\llm verse group 16\screenshots\s1.jpg'
    screenshot=ImageGrab.grab()
    rgb_screenshot=screenshot.convert('RGB')
    rgb_screenshot.save(path,quality=15)
    
def web_cam_capture():
    if not web_cam.isOpened():
        print("Error")
        exit()
    path=r'C:\Users\Happy Home\OneDrive\Desktop\hackathon\llm verse group 16\webcam\w1.jpg'
    ret,frame=web_cam.read()
    cv2.imwrite(path,frame)

def get_clipboard_text():
    clipboard_content=pyperclip.paste()
    if isinstance(clipboard_content,str):
        return clipboard_content
    else:
        print("No clipboard text to copy")
        return None

def vision_prompt(prompt, photo_path):
    img = Image.open(photo_path)
    prompt = (
        'You are the vision analysis AI that provides semantic meaning from images to provide context '
        'to send to another AI that will create a response to the user. Do not respond as the AI assistant '
        'to the user. Instead take the user prompt input and try to extract all meaning from the photo '
        'relevant to the user prompt. Then generate as much objective data about the image for the AI '
        f'assistant who will respond to the user. \nUSER PROMPT: {prompt}'
    )

    response = model.generate_content([prompt, img])
    return response.text

def open_website(url):
    try:
        # If the URL doesn't start with http:// or https://, assume it's just a name and build a full URL.
        if not url.startswith(('http://', 'https://')):
            url = 'http://www.' + url + '.com'
        webbrowser.open(url)
        print(f"Opened {url} in your default browser.")
    except Exception as e:
        print(f"Error opening website: {e}")

def wav_to_text(audio_path):
    with open(audio_path, "rb") as file:
        translation = groq_client.audio.translations.create(
            file=(audio_path, file.read()),
            model="whisper-large-v3",
        )
    return translation.text


def callback(recognizer, audio):
    global s
    try:
        prompt_audio_path = 'prompt.wav'
        with open(prompt_audio_path, 'wb') as f:
            f.write(audio.get_wav_data())

        prompt_text = wav_to_text(prompt_audio_path)
        clean_prompt = extract_prompt(prompt_text, wake_word)

        if clean_prompt:
            print(f'USER: {clean_prompt}')
            call = function_call(clean_prompt)

            if 'take screenshot' in call:
                print('Taking screenshot')
                take_screenshot()
                visual_context = vision_prompt(
                    prompt=clean_prompt,
                    photo_path=r'C:\Users\Happy Home\OneDrive\Desktop\hackathon\llm verse group 16\screenshots\s1.jpg'
                )
            elif 'capture webcam' in call:
                print('Capturing webcam')
                web_cam_capture()
                visual_context = vision_prompt(
                    prompt=clean_prompt,
                    photo_path=r'C:\Users\Happy Home\OneDrive\Desktop\hackathon\llm verse group 16\webcam\w1.jpg'
                )
            elif 'extract clipboard' in call:
                print('Copying clipboard text')
                paste = get_clipboard_text()
                # Update clean_prompt so that the clipboard text is included
                clean_prompt = f'{clean_prompt}\n\nCLIPBOARD CONTENT: {paste}'
                visual_context = None
            elif 'open website' in call:
                print('Opening website')
                # Try to extract a URL with a regex.
                match = re.search(r'\bopen\s+(\w+)', clean_prompt, re.IGNORECASE)
                if match:
                    url = match.group(1)
                    if not url.startswith(('http://', 'https://')):
                        url = 'http://www.'+ url+'.com'
                    open_website(url)
                else:
                    # If no full URL is found, assume the website name follows "open"
                    website = clean_prompt.lower().split("open")[-1].strip()
                    if website:
                        open_website(website)
                    else:
                        print("No website name found in the prompt.")
                visual_context = None

            else:
                visual_context = None

            response = groq_prompt(prompt=clean_prompt, img_context=visual_context)
            print(f'ASSISTANT: {response}')
            asyncio.run(speak(response,s))
            play(s)
            s+=1
        

            #speak(response)
    except Exception as e:
        print("Error in callback:", e)




def start_listening():
    with source as s:
        r.adjust_for_ambient_noise(s,duration=2)
    print('\nSay',wake_word,"followed by your prompt. \n")
    r.listen_in_background(source,callback)
    while True:
        time.sleep(0.5)


def extract_prompt(transcribed_text,wake_word):
    pattern=rf'\b{re.escape(wake_word)}[\s,.?!]*([A-Za-z0-9].*)'
    match=re.search(pattern,transcribed_text,re.IGNORECASE)

    if match:
        prompt=match.group(1).strip()
        return prompt
    else:
        return None

start_listening()
