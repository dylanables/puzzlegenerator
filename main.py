from flask import Flask, render_template
from cross import crossword_blueprint
from search import wordsearch_blueprint

app = Flask(__name__)

app.register_blueprint(crossword_blueprint)
app.register_blueprint(wordsearch_blueprint)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)