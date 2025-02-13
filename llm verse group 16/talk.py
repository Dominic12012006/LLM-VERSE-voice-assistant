import pygame
import os

# Initialize pygame mixer
pygame.mixer.init()

def play(p):
    output_dir = r"C:\Users\Happy Home\OneDrive\Desktop\hackathon\llm verse group 16\outputs"
    file_path = os.path.join(output_dir, f"output{p}.mp3")
    pygame.mixer.music.load(file_path)

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the script running while the music is playing
    while pygame.mixer.music.get_busy():
        continue


