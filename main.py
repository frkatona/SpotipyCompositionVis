import spotipy
from spotipy.oauth2 import SpotifyOAuth
import matplotlib.pyplot as plt

# Set up authentication with Spotify API
scope = "playlist-read-private"

client_id = 'dc41fad6247d4c489596bc6634be5290'
client_secret = 'd8c9b8681d394b24921e6ec6ddff5fba'
redirect_uri = 'http://localhost:8080/callback'
scope = 'user-library-read'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))

# Retrieve the playlist ID
# playlist_id = input("Enter Spotify playlist ID: ")
playlist_URL = 'https://open.spotify.com/playlist/4wxkbE2pTsRH9W2j9YUhF7?si=003b92a2b57f4696'
playlist_id = playlist_URL.split('/')[4].split('?')[0]

# Retrieve the tracks on the playlist
tracks = sp.playlist_tracks(playlist_id)

fig, ax = plt.subplots()
color = ['blue', 'red', 'green', 'yellow', 'orange', 'purple', 'pink', 'brown', 'grey', 'black']
longest_track = 0

# Iterate through the tracks and retrieve the audio analysis for each one
for i, track in enumerate(tracks['items']):
    track_id = track['track']['id']
    analysis = sp.audio_analysis(track_id)
    if analysis['track']['duration'] > longest_track:
        longest_track = analysis['track']['duration']

    # Extract the time intervals for each section of the song
    sections = analysis['sections']
    section_intervals = [(s['start'], s['start'] + s['duration']) for s in sections]
    time_bar_factor = analysis['track']['tempo'] / analysis['track']['time_signature'] / 60

    #label the track name
    ax.text(0, (i + 0.5), track['track']['name'], fontsize=8, weight = 'bold', va='center', ha='right', color='black', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))

    # Plot the section intervals as rectangles
    for j, interval in enumerate(section_intervals):
        ax.add_patch(plt.Rectangle(((time_bar_factor * interval[0] + 1), (i)), time_bar_factor * (interval[1]-interval[0]), 1, color=color[j%len(color)]))

#scale the plot
ax.set_xlim(0, time_bar_factor * longest_track)
ax.set_ylim(0, len(tracks['items']))

#set x ticks distance
ax.set_xticks([i for i in range(0, int(time_bar_factor * longest_track), 16)])
plt.xlabel("Bars")
plt.title('Spotify Audio Analysis')
plt.show()
