import os
from google import genai
import logging
from PIL import ImageGrab  # Adds screen capturing ability

from audio.tts import speak
from audio.stt import listen_to_user
from audio.wake_word import wait_for_wake_word

# Import the tools you built
from tools.web_tools import open_dsa_environment, play_youtube_music
from tools.system_tools import open_project_in_vscode, control_media

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
        play_youtube_music,
        control_media
    ]
    
    # 4. System Instruction: Give JARVIS a personality and instructions
    jarvis_persona = """
    You are JARVIS, a highly capable, concise, and helpful AI assistant.
    You control the user's Lenovo LOQ laptop using the tools provided to you.
    When the user asks you to do something, determine which tool is appropriate and execute it.
    CRITICAL INSTRUCTION: You MUST always generate a brief, 1-2 sentence text response 
    confirming what you just did AFTER using a tool. Never return an empty response.
    """
    
    print("Initializing JARVIS Brain (Gemini 2.0 Flash)...")
    
    # 5. Start the chat session with Automatic Function Calling enabled
    chat = client.chats.create(
        model="gemini-2.5-flash",
        config=dict(
            tools=jarvis_tools,
            system_instruction=jarvis_persona,
            temperature=0.2 # Low temperature makes it more robotic/precise
        )
    )
    
    print("\nJARVIS is online. (Type 'exit' to quit)")
    print("-" * 50)
    
    # 6. The Agentic Loop
    print("\nJARVIS Framework fully loaded. Entering main system routine.")
    
    while True:
        # ====================================================================
        # STAGE 1: PASSIVE SLEEP STATE
        # ====================================================================
        # System halts right here, pulling 0% network data, waiting for the wake word
        wait_for_wake_word()
        
        print("\n[JARVIS: Awakened. Opening continuous session...]")
        speak("Online and ready, boss.")
        
        # ====================================================================
        # STAGE 2: ACTIVE CONTINUOUS CONVERSATION SESSION
        # ====================================================================
        # Once awake, enter a dedicated loop that keeps listening back-to-back
        while True:
            user_input = listen_to_user()
            
            # If the mic caught complete silence, loop back and listen again
            if not user_input:
                continue
                
            print(f"You (Spoken): {user_input}")
            spoken_lower = user_input.lower()
            
            # --- SPLIT TERMINATION LOGIC ---
            # 1. Check for HARD SHUTDOWN (Kills the entire program)
            hard_shutdown_phrases = ['exit', 'quit', 'power off', 'full shutdown', 'completely shut down']
            if any(phrase in spoken_lower for phrase in hard_shutdown_phrases):
                print("JARVIS: Completely shutting down core systems. Goodbye.")
                speak("Completely shutting down core systems. Goodbye.")
                import sys
                sys.exit(0) # Instantly kills the entire Python script cleanly
                
            # 2. Check for SOFT STANDBY (Goes back to waiting for "Hey Jarvis")
            standby_phrases = ['power down', 'go to sleep', 'stop listening', 'standby']
            if any(phrase in spoken_lower for phrase in standby_phrases):
                print("JARVIS: Entering standby mode. Standing by...")
                speak("Entering standby mode.")
                break # Breaks inner loop, falls back to wake word listening
            # -------------------------------
                
            try:
                # Visual Brain Context routing
                if "look" in spoken_lower or "see" in spoken_lower or "screen" in spoken_lower:
                    print("[JARVIS is capturing your screen...]")
                    screenshot = ImageGrab.grab()
                    response = chat.send_message([user_input, screenshot])
                else:
                    response = chat.send_message(user_input)
                
                reply_text = response.text
                print(f"\nJARVIS: {reply_text}\n")
                speak(reply_text)
                
            except Exception as e:
                print(f"\nJARVIS: I'm sorry, I encountered an error during session processing: {e}\n")