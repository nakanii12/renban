import json
import requests
def get_data(videoid):
    t = json.loads(requests.get(r"https://vid.puffyan.us/api/v1/videos/"+ videoid).text)
    return [{"id":i["videoId"],"title":i["title"]} for i in t["recommendedVideos"]],t["formatStreams"][-1]["url"],t["descriptionHtml"].replace("\n","<br>"),t["title"]

def get_search(q):
    t = json.loads(requests.get(r"https://vid.puffyan.us/api/v1/search?q="+ q).text)
    return [{"title":i["title"],"id":i["videoId"]} for i in t]

from flask import Flask,render_template,request,abort,make_response

def check_cokie():
    if request.cookies.get('yuki', None) == "True":
        return True
    return False
    
app = Flask(__name__, static_folder='./static', static_url_path='')
@app.route("/")
def home():
    if check_cokie():
        return render_template("home.html")
    return """<head><title>連番を簡単に生成！！</title></head><body><form action="/answer" method="get">
    <input type="text" name="q" required>
    <input type="submit" value="生成！！">
</form></body>"""

@app.route('/watch')
def video():
    if not(check_cokie()):
        return abort(404)
    videoid = request.args.get("v")
    t = get_data(videoid)
    return render_template('video.html',videoid=videoid,videourl=t[1],res=t[0],description=t[2],videotitle=t[3])

@app.route("/search")
def search():
    if not(check_cokie()):
        return abort(404)
    q = request.args.get("q")
    return render_template("search.html",results=get_search(q))

@app.route("/answer")
def set_cokie():
    q = request.args.get("q")
    response = make_response("<head><title>連番を簡単に生成！！</title></head><body>"+" ".join([str(i) for i in range(int(q))])+"</body>")
    if q == "85175":
        response.set_cookie("yuki",value="True")
    return response

@app.errorhandler(404)
def page_not_found(error):
    return """<head><title>連番を簡単に生成！！</title></head><body><form action="/answer" method="get">
    <input type="text" name="q" required>
    <input type="submit" value="生成！！">
</form></body>"""
