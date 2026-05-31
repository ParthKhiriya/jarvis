import speech_recognition as sr
import logging

logger = logging.getLogger(__name__)

def listen_to_user() -> str:
    """
    Activates the laptop's microphone, calibrates for background noise,
    and listens for user speech. Transcribes the audio into text.
    
    Returns:
        str: The transcribed text command, or an empty string if failed.
    """
    # Initialize the recognizer object
    recognizer = sr.Recognizer()
    
    # Use the default system microphone as the audio source
    with sr.Microphone() as source:
        print("\n[JARVIS is listening...]")
        
        try:
            # Adjusts the energy threshold dynamically to handle room static/fan noise
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            # Capture the live audio stream until the user stops talking
            # timeout=5 means it stops waiting if you don't talk for 5 seconds
            # phrase_time_limit=10 caps your spoken sentence at 10 seconds
            audio_data = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            print("[Processing voice data...]")
            
            # Transcribe the audio using Google's free web recognition service
            text_command = recognizer.recognize_google(audio_data)
            logger.info(f"STT Successfully Transcribed: '{text_command}'")
            return text_command
            
        except sr.WaitTimeoutError:
            # Triggered if you don't say anything within the timeout limit
            return ""
        except sr.UnknownValueError:
            # Triggered if you mumble or the mic picks up static it can't understand
            print("JARVIS: I couldn't quite catch that. Could you repeat it?")
            return ""
        except sr.RequestError as e:
            # Triggered if your laptop loses internet connection
            logger.error(f"Speech service network error: {e}")
            print("JARVIS: I'm having trouble reaching the voice transcription servers.")
            return ""