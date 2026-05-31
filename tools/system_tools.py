import subprocess
import os
import logging

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
