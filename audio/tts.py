import edge_tts
import pygame
import asyncio
import os
import logging

logger = logging.getLogger(__name__)

# We use a British Male voice for that JARVIS feel. 
# You can change this later!
VOICE = "en-GB-ThomasNeural" 
OUTPUT_FILE = "response.mp3"

async def generate_audio(text: str):
    """Generates the audio file from text using Edge TTS."""
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(OUTPUT_FILE)

def speak(text: str):
    """
    Takes a string of text, generates an audio file, 
    and plays it through the computer's speakers.
    """
    if not text or text == "None":
        return
        
    logger.info(f"JARVIS Speaking: '{text}'")
    
    # 1. Generate the audio file (we use asyncio.run because edge_tts is asynchronous)
    asyncio.run(generate_audio(text))
    
    # 2. Play the audio file using pygame
    pygame.mixer.init()
    pygame.mixer.music.load(OUTPUT_FILE)
    pygame.mixer.music.play()
    
    # 3. Keep the script paused until the audio finishes playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
        
    # 4. Unload and delete the temporary audio file to keep your system clean
    pygame.mixer.quit()
    try:
        os.remove(OUTPUT_FILE)
    except OSError:
        pass