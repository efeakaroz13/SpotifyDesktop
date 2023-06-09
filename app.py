from flask import Flask,render_template,redirect,request
from mp3fy import MP3fy
import json

app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")


class API:
    @app.route("/api/search")
    def search_api():
        q = request.args.get("q")
        q = q.strip()
        if q == None:
            return {"SCC":False}
        if q == "":
            return {"tracks":{"items":[]}}
        output = MP3fy.search(q)
        return output
class CorePages:
    @app.route("/playlist/<playlistID>")
    def getPlaylist(playlistID):
        playlist = MP3fy.getPlaylist("https://open.spotify.com/playlist/" + playlistID)
        return render_template("playlist.html", data=playlist, dumps=json.dumps, ds=json.dumps(playlist))
    @app.route("/user/<userID>")
    def userprofiler(userID):
        userData = MP3fy.getUser(userID)
        return userData

if __name__ == "__main__":
    app.run(debug=True,port=3000)