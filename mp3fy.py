import urllib.request
import re
import time
from pytube import YouTube
import os
from colorama import Fore, Back, Style
import json 
import shutil
import requests
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

def compress(basename):
        os.system(f"ffmpeg -y -i '{basename}.mp4' -vcodec libx265 -crf 28 '{basename}_C.mp4'")

class MP3fy:
    def downloadvideo(search,data):
        songname = data["name"]
        data = data["album"]
        d_img=0
        image = data["images"][0]["url"]
        i_r = requests.get(image,stream=True)
        if i_r.status_code == 200:
            with open("cover.png","wb") as f:
                shutil.copyfileobj(i_r.raw,f)
                print("img downloaded")
            d_img = 1

        search = search.lower().replace("ü","u").replace("$","s").replace("ö","").replace("ş","s").replace("ö","o").replace("İ","I").replace("ı","i")
        page = urllib.request.urlopen("https://www.youtube.com/results?search_query={}".format(search.replace(' ','+')))
        videoids=  re.findall(r"watch\?v=(\S{11})",page.read().decode())
        theurl = "https://youtube.com/watch?v="+videoids[0]

        yt = YouTube(theurl)
        
        video = yt.streams.filter(only_audio=True).first()
        
        
        out_file = video.download(output_path="static")
        base, ext = os.path.splitext(out_file)
        compress(base)

        os.system(f"ffmpeg -y -i '{base}.mp4' -b:a 192K -vn '{base}.mp3'")
        if d_img == 1:
            os.system(f"ffmpeg -y -i  '{base}.mp3' -i cover.png -c copy -map 0 -map 1 '{base}_.mp3'")
            os.system("rm cover.png")
        
        aname= data["artists"][0]["name"]
        os.system(f"ffmpeg -y -i '{base}_.mp3' -c copy -metadata artist='{aname}' '{base}.mp3'")

        os.system(f"rm '{base}_.mp3'")
        os.system(f"rm '{base}.mp4'")

        os.system(f"mv '{base}.mp3' 'static/{songname}.mp3'")

        return f"static/{songname}"





    
    def getPlaylist(theurl):
        try:
            theval1 = theurl.split("https://open.spotify.com/playlist/")[1]
            pl_id = f"spotify:playlist:{theval1}"
        except:
            print("Err | Unknown URL")
            exit()
        config = json.loads(open("config.json","r").read())

        os.environ["SPOTIPY_CLIENT_ID"] =config["client_id"]
        os.environ["SPOTIPY_CLIENT_SECRET"] =config["secretclient"]




        try:
            sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
        except:
            print("Check your credentials")
            return False

        offset = 0

        response = sp.playlist(pl_id)

       

        return response

    def search(q):
        config = json.loads(open("config.json","r").read())
        os.environ["SPOTIPY_CLIENT_ID"] =config["client_id"]
        os.environ["SPOTIPY_CLIENT_SECRET"] =config["secretclient"]

        try:
            sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
        except:
            print("Check your credentials")
            return False
        response = sp.search(q=q,limit=15,type="track,artist,playlist")
        return response


    def getAlbum(theurl):
        try:
            theval1 = theurl.split("https://open.spotify.com/album/")[1]
            pl_id = f"spotify:album:{theval1}"
        except:
            print("Err | Unknown URL")
            exit()
        config = json.loads(open("config.json","r").read())

        os.environ["SPOTIPY_CLIENT_ID"] =config["client_id"]
        os.environ["SPOTIPY_CLIENT_SECRET"] =config["secretclient"]




        try:
            sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
        except:
            print("Check your credentials")
            return False

        offset = 0

        response = sp.album(pl_id)

       

        return response
    

if __name__ == "__main__":

    output = MP3fy.getAlbum("https://open.spotify.com/album/0pTcS1HbU01CSjEkjzCMeS")
    open("output.json","w").write(json.dumps(output,indent=4))



        