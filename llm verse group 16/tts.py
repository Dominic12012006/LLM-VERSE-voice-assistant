import asyncio
import edge_tts
import os
async def speak(text,s):
    voice = "en-US-AriaNeural"  # Choose an appropriate voice
    rate = "+110%"  # Increase speed (you can adjust this)

    tts = edge_tts.Communicate(text, voice, rate=rate)
    output_dir = r"C:\Users\Happy Home\OneDrive\Desktop\hackathon\llm verse group 16\outputs"
    file_path = os.path.join(output_dir, f"output{s}.mp3")
    await tts.save(file_path)

# Run the async function
#asyncio.run(speak("Hello, world! this is great",1))

