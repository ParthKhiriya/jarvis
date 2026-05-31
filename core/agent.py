import os
from google import genai
import logging
from audio.tts import speak
from audio.stt import listen_to_user

# Import the tools you built
from tools.web_tools import open_dsa_environment, play_youtube_music
from tools.system_tools import open_project_in_vscode

logger = logging.getLogger(__name__)

def start_jarvis_brain():
    """
    Initializes the Gemini AI model, equips it with tools, 
    and starts the agentic interaction loop.
    """
    # 1. Check for the API key
    if not os.environ.get("GEMINI_API_KEY"):
        print("ERROR: GEMINI_API_KEY environment variable not set.")
        return

    # 2. Initialize the modern Google Gen AI Client
    client = genai.Client()
    
    # 3. Create our Tool Box
    # We pass the actual python functions directly in a list.
    jarvis_tools = [
        open_dsa_environment,
        open_project_in_vscode,
        play_youtube_music
    ]
    
    # 4. System Instruction: Give JARVIS a personality and instructions
    jarvis_persona = """
    You are JARVIS, a highly capable, concise, and helpful AI assistant.
    You control the user's Lenovo LOQ laptop using the tools provided to you.
    When the user asks you to do something, determine which tool is appropriate, execute it, 
    and then give a very brief confirmation message (1-2 sentences max). 
    Do not explain how you did it, just confirm it is done.
    """
    
    print("Initializing JARVIS Brain (Gemini 2.0 Flash)...")
    
    # 5. Start the chat session with Automatic Function Calling enabled
    chat = client.chats.create(
        model="gemini-2.5-flash-lite",
        config=dict(
            tools=jarvis_tools,
            system_instruction=jarvis_persona,
            temperature=0.2 # Low temperature makes it more robotic/precise
        )
    )
    
    print("\nJARVIS is online. (Type 'exit' to quit)")
    print("-" * 50)
    
    # 6. The Agentic Loop
    while True:
        # REPLACE the old input() line with our microphone listener!
        user_input = listen_to_user()
        
        # If the mic heard nothing (or timed out), loop back and keep listening
        if not user_input:
            continue
            
        print(f"You (Spoken): {user_input}")
        
        # --- NEW EXIT LOGIC ---
        # Convert input to lowercase once
        spoken_lower = user_input.lower()
        
        # If ANY of these phrases are found anywhere in your sentence, shut down.
        exit_phrases = ['exit', 'quit', 'power down', 'shut down', 'stop listening']
        
        if any(phrase in spoken_lower for phrase in exit_phrases):
            print("JARVIS: Powering down. Goodbye.")
            speak("Powering down. Goodbye.")
            break
        # ----------------------
            
        try:
            response = chat.send_message(user_input)
            reply_text = response.text
            print(f"\nJARVIS: {reply_text}\n")
            speak(reply_text)
            
        except Exception as e:
            print(f"\nJARVIS: I'm sorry, I encountered an error: {e}\n")