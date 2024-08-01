import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
from dotenv import load_dotenv


class Connection():
    def __init__(self, client_id, client_secret):    
        self.client_id = client_id
        self.client_secret = client_secret
    
    def connection_setting(self):
        client_credentials_manager = SpotifyClientCredentials(self.client_id, self.client_secret)
        connection = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        return connection

class Playlist(): 
    def __init__(self, connection):
        self.connection = connection

    def search_my_top10(self):
        playlists = self.connection.user_playlists('spotify')
        result = self.connection.artist_top_tracks("51Blml2LZPmy7TTiAg47vQ",country='US')
        top10 = result['tracks'][:10]
        return top10

    def convert_mm_ss(self,duration_ms):
        pass
        minutes = duration_ms // 60000
        seconds = (duration_ms % 60000) // 1000
        return f"{minutes}:{seconds:02d}"
    
    def df_tracks(self, top10):
        top10 = self.search_my_top10()
        tracks = [(track["name"], track["popularity"], track["duration_ms"]) for track in top10]
        columns=['Name', 'Popularity', 'Duration (ms)']
        df = pd.DataFrame(tracks, columns = columns)
        df['Duration (mm:ss)'] = df['Duration (ms)'].apply(self.convert_mm_ss)
        return df

    def sort_by_popularity(self,df):
        by_popularity = df.sort_values(by="Popularity", ascending=True)
        print(by_popularity)

    def scatter_plot(self,df):
        by_duration = df.sort_values(by="Duration (mm:ss)", ascending=True)
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=by_duration, x="Duration (mm:ss)", y="Popularity", hue="Duration (mm:ss)", palette="deep", size="Duration (mm:ss)")
        plt.ylabel('Popularity') 
        plt.xlabel('Duration (ms:ss)')
        plt.title('Tracks Popularity vs Duration')
        plt.savefig("scatter_plot.jpg",dpi=300)
        plt.show()

load_dotenv()
client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')
my_connection =  Connection(client_id, client_secret)
spotify_connection = my_connection.connection_setting()

my_playlist = Playlist(spotify_connection)
top10 = my_playlist.search_my_top10()
tracks = my_playlist.df_tracks(top10)
track_sorted = my_playlist.sort_by_popularity(tracks)
my_plot = my_playlist.scatter_plot(tracks)
