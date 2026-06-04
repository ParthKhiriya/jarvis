import subprocess
import os
import logging
import pyautogui # For simulating mouse clicks and keyboard presses(for starting, stopping music)

# Set up logging for system tools 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# A professional lookup dictionary mapping project names to their actual paths.
PROJECT_DIRECTORY = {
    "agents": r"D:\agentic-ai\agents",
    "jarvis": r"D:\agentic-ai\jarvis-project",
    "agentic-course": r"D:\agentic-ai\agentic-course-udemy"
}

def open_project_in_vscode(project_name: str) -> str:
    """
    Opens a specific coding project folder inside VS Code using the Windows command line.
    
    Args:
        project_name (str): The name of the project to open (e.g., 'agents', 'jarvis').
        
    Returns:
        str: A status message for the AI Agent confirming success or failure.
    """

    # Clean the input string (lowercase and remove spaces) to make matching easier
    cleaned_name = project_name.lower().strip()
    logger.info(f"JARVIS: Searching for project alias: '{cleaned_name}'...")

    # Check if the requested project exists in our database
    if cleaned_name not in PROJECT_DIRECTORY:
        error_msg = f"Project '{project_name}' not found in JARVIS registry."
        logger.warning(error_msg)
        return error_msg
    
    project_path = PROJECT_DIRECTORY[cleaned_name]

    # Safety Check: Verify the folder actually exists on the hard drive
    if not os.path.exists(project_path):
        error_msg = f"Registry path exists, but the physical folder was not found at: {project_path}"
        logger.error(error_msg)
        return error_msg
    

    try:
        logger.info(f"JARVIS: Launching VS Code for path: {project_path}")
        
        # subprocess.run executes a command in the Windows terminal background.
        # shell=True allows us to use standard Windows environment commands like 'code'.
        subprocess.run(f'code "{project_path}"', shell=True, check=True)
        
        success_msg = f"Successfully opened project '{project_name}' in VS Code."
        logger.info(success_msg)
        return success_msg
        
    except subprocess.CalledProcessError as e:
        error_msg = f"Failed to execute VS Code command line shortcut. System error: {str(e)}"
        logger.error(error_msg)
        return error_msg


def control_media(action: str) -> str:
    """
    Controls the computer's media playback and system volume.
    
    Args:
        action (str): The desired action. Valid options include 'play', 'pause', 
                      'mute', 'max volume', 'volume up', 'volume down', 'next', 'previous'.
                      
    Returns:
        str: A confirmation message of the action taken.
    """
    cleaned_action = action.lower().strip()
    logger.info(f"JARVIS: Executing media control for '{cleaned_action}'")
    
    try:
        if "play" in cleaned_action or "pause" in cleaned_action or "stop" in cleaned_action:
            pyautogui.press("playpause")
            success_msg = "Toggled media playback."
            
        elif "mute" in cleaned_action:
            pyautogui.press("volumemute")
            success_msg = "Toggled system mute."
            
        elif "max" in cleaned_action or "maximum" in cleaned_action:
            # Windows volume goes up 2% per keystroke. 
            # 50 presses guarantees 100% volume instantly.
            pyautogui.press("volumeup", presses=50)
            success_msg = "Maximized system volume."
            
        elif "up" in cleaned_action or "increase" in cleaned_action:
            pyautogui.press(["volumeup", "volumeup", "volumeup", "volumeup"])
            success_msg = "Increased system volume."
            
        elif "down" in cleaned_action or "decrease" in cleaned_action:
            pyautogui.press(["volumedown", "volumedown", "volumedown", "volumedown"])
            success_msg = "Decreased system volume."
            
        elif "next" in cleaned_action or "skip" in cleaned_action:
            pyautogui.press("nexttrack")
            success_msg = "Skipped to the next track."
            
        elif "previous" in cleaned_action or "back" in cleaned_action:
            # Fire the key twice to bypass the "restart song" behavior
            pyautogui.press(["prevtrack", "prevtrack"])
            success_msg = "Returned to the previous track."
            
        else:
            return f"I am not sure how to perform the media action: '{action}'."
            
        logger.info(success_msg)
        return success_msg
        
    except Exception as e:
        error_msg = f"Failed to execute media control. Error: {str(e)}"
        logger.error(error_msg)
        return error_msg