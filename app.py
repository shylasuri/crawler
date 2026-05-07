from flask import Flask, render_template, request
from flask_cors import CORS
import matplotlib
matplotlib.use('Agg')
import traceback
from crawler import scrape_news

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET", "POST"])
def home():
    data = []
    error = None
    if request.method == "POST":
        topic = request.form.get("topic", "").strip()
        try:
            articles = scrape_news()
            if topic:
                data = [a for a in articles if topic.lower() in a['title'].lower()]
            else:
                data = articles
        except Exception as e:
            error = str(e)
            traceback.print_exc()
    return render_template("index.html", data=data, error=error)

if __name__ == "__main__":
    app.run(debug=True)