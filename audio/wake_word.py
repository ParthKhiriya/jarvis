import pyaudio
import numpy as np
import openwakeword
from openwakeword.model import Model
import logging

logger = logging.getLogger(__name__)

def wait_for_wake_word():
    """
    Sits in a low-power infinite loop listening purely for the acoustic signature 
    of 'Hey Jarvis'. Uses 0% network bandwidth and minimal CPU.
    """
    # 1. Ask the library for all of its hidden pre-trained model paths
    pretrained_paths = openwakeword.get_pretrained_model_paths()
    
    # 2. Find the exact absolute file path for the 'hey_jarvis' ONNX model
    jarvis_path = [path for path in pretrained_paths if "hey_jarvis" in path][0]
    
    # 3. Initialize the model using the actual absolute file path
    oww_model = Model(wakeword_model_paths=[jarvis_path])
    
    CHUNK = 1280
    audio = pyaudio.PyAudio()
    
    # Open the microphone specifically formatted for the ML model (16khz, mono)
    mic_stream = audio.open(format=pyaudio.paInt16, 
                            channels=1, 
                            rate=16000, 
                            input=True, 
                            frames_per_buffer=CHUNK)
    
    print("\n[Local Engine: Sleeping... Waiting to hear 'Hey Jarvis']")
    
    while True:
        # Grab a tiny chunk of audio safely
        audio_data = np.frombuffer(mic_stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
        
        # Feed the raw audio into the local neural network
        prediction = oww_model.predict(audio_data)
        
        # Check the confidence score
        for model_name, score in prediction.items():
            # 0.5 is the standard confidence threshold
            if score > 0.3:
                # Wake word detected! Clean up the local mic stream to free it for Stage 2
                mic_stream.stop_stream()
                mic_stream.close()
                audio.terminate()
                return True