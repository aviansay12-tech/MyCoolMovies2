import sys
import xbmcgui
import xbmcplugin
from urllib.parse import parse_qs
from lib.scraper import get_latest_movies, get_video_source

# Get the add-on handle provided by Kodi
_handle = int(sys.argv[1])
_params = parse_qs(sys.argv[2][1:])

def list_movies():
    """Creates the main movie list in the Kodi UI."""
    xbmcplugin.setPluginCategory(_handle, 'Latest Movies')
    
    # Get movie data from our scraper
    movies = get_latest_movies()
    
    if not movies:
        xbmcgui.Dialog().notification('Scraper Error', 'Could not fetch movie list.', xbmcgui.NOTIFICATION_ERROR)
        return

    # Create a list item for each movie
    for movie in movies:
        list_item = xbmcgui.ListItem(label=movie['title'])
        list_item.setArt({'thumb': movie['poster'], 'icon': movie['poster'], 'poster': movie['poster']})
        list_item.setInfo('video', {'title': movie['title'], 'mediatype': 'movie'})
        list_item.setProperty('IsPlayable', 'true')
        
        # The URL that will be called when the user clicks this item.
        # We pass the movie's page URL and an 'action' to tell our script what to do next.
        url = f"plugin://plugin.video.mycoolmovies/?action=play&url={movie['url']}"
        
        xbmcplugin.addDirectoryItem(handle=_handle, url=url, listitem=list_item, isFolder=False)
        
    xbmcplugin.endOfDirectory(_handle)

def play_video(url):
    """Resolves the video source and tells Kodi to play it."""
    # Get the direct video link from our scraper
    video_url = get_video_source(url)
    
    if video_url:
        # Create a playable list item
        play_item = xbmcgui.ListItem(path=video_url)
        # Pass it to Kodi's player
        xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)
    else:
        # Show an error to the user if we couldn't find a source
        xbmcgui.Dialog().notification('Playback Failed', 'Could not find a playable video source.', xbmcgui.NOTIFICATION_ERROR)
        xbmcplugin.setResolvedUrl(_handle, False, listitem=xbmcgui.ListItem())

def router():
    """Simple router to direct actions."""
    action = _params.get('action', [None])[0]
    
    if action == 'play':
        url = _params.get('url', [None])[0]
        play_video(url)
    else:
        # Default action is to show the main movie list
        list_movies()

if __name__ == '__main__':
    router()