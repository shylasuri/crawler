from flask import Flask, render_template, request
from crawler import scrape_news

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    data = []
    if request.method == "POST":
        topic = request.form["topic"]
        data = scrape_news(topic)
    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)