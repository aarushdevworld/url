from flask import Flask, render_template, request
import pyshorteners, random

app = Flask(__name__)

def short_url(long_url, choice=None):
    if not (long_url.startswith("https://") or long_url.startswith("http://")):
        return None
    
    shortener = pyshorteners.Shortener()
    services = {
        "tinyurl": shortener.tinyurl,
        "isgd": shortener.isgd,
        "clckru": shortener.clckru,
        "osdb": shortener.osdb,
    }
    
    if choice and choice in services:
        chosen_service = services[choice]
    else:
        chosen_service = random.choice(list(services.values()))
    
    try:
        return chosen_service.short(long_url)
    except Exception:
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    shortened = None
    long_url = None
    choice = None
    if request.method == "POST":
        long_url = request.form.get("long_url")
        choice = request.form.get("shortener")
        shortened = short_url(long_url, choice if choice else None)
    return render_template("index.html", shortened=shortened, long_url=long_url)

if __name__ == "__main__":
    app.run(debug=True)
