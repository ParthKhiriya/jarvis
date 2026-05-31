import webbrowser
import logging
import urllib.parse  # Built-in library to safely format text for URLs
from ytmusicapi import YTMusic


# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



# THIS FUNCTION IS FOR LAUNCHING THE DSA ENVIRONMENT ----------------------------------------------------------------------------

def open_dsa_environment() -> str:
    """
    Opens the user's daily Data Structures and Algorithms (DSA) workspace.
    This launches Google Docs, NeetCode, and LeetCode in the default browser.
    
    Returns:
        str: A status message indicating success or failure.
    """
    logger.info("JARVIS: Initializing DSA environment...")
    
    urls = [
        "https://docs.google.com/document/d/1OwIZXkqpoDlEtN-wvKiVxwoaaFImGR7QKZhph7vMR1o/",  
        "https://neetcode.io/practice",
        "https://leetcode.com/problemset/all/"
    ]
    
    try:
        for i, url in enumerate(urls):
            if i == 0:
                webbrowser.open_new(url)
            else:
                webbrowser.open_new_tab(url)
        
        success_msg = "Successfully opened Google Docs, NeetCode, and LeetCode."
        logger.info(success_msg)
        return success_msg
        
    except Exception as e:
        error_msg = f"Failed to open DSA environment. Error: {str(e)}"
        logger.error(error_msg)
        return error_msg
    


# THE BELOW CODE IS FOR PLAYING A SONG ON YOUTUBE MUSIC -------------------------------------------------------------------------

# Initialize the YTMusic controller once globally
try:
    yt_client = YTMusic()
except Exception as e:
    logger.error(f"Failed to initialize YTMusic client: {e}")
    yt_client = None

def play_youtube_music(song_name: str) -> str:
    """
    Searches YouTube Music for the requested track, extracts the exact 
    Video ID of the top result, and launches it directly in auto-play mode.
    
    Args:
        song_name (str): The name of the song or artist requested.
        
    Returns:
        str: A success message with the track title or an error description.
    """
    cleaned_song = song_name.strip()
    if not cleaned_song:
        return "No song name provided."
        
    if not yt_client:
        return "YouTube Music client is unavailable."

    logger.info(f"JARVIS: Fetching track data for: '{cleaned_song}'...")
    
    try:
        # Search for songs specifically (filtering out full albums or playlists)
        search_results = yt_client.search(query=cleaned_song, filter="songs", limit=1)
        
        if not search_results:
            error_msg = f"Could not find any songs matching '{cleaned_song}' on YouTube Music."
            logger.warning(error_msg)
            return error_msg
            
        # Extract the top track metadata
        top_track = search_results[0]
        video_id = top_track.get("videoId")
        track_title = top_track.get("title", "Unknown Track")
        artist_name = "Unknown Artist"
        
        # Safely extract artist name from the metadata list
        if top_track.get("artists"):
            artist_name = top_track["artists"][0].get("name", "Unknown Artist")
            
        if not video_id:
            return f"Found '{track_title}', but it doesn't have a valid playback ID."
            
        # Construct a direct streaming/watch URL instead of a search URL
        playback_url = f"https://music.youtube.com/watch?v={video_id}"
        
        logger.info(f"JARVIS: Found '{track_title}' by {artist_name}. Streaming URL: {playback_url}")
        
        # Open the direct song link
        webbrowser.open(playback_url)
        
        success_msg = f"Now playing '{track_title}' by {artist_name} on YouTube Music."
        return success_msg
        
    except Exception as e:
        error_msg = f"Failed to execute YouTube Music direct playback. Error: {str(e)}"
        logger.error(error_msg)
        return error_msg