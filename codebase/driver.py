from flask import Flask, render_template, request
from retrieval_model.retrieval import ui_response
app = Flask(__name__)

wing_map = {"left": "chat_left.html", "right": "chat_right.html"}

user = None
wing = None
tweet = None
reply1 = None
reply2 = None

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/tweet", methods=["POST"])
def post_tweet():
    global wing, tweet, reply1, reply2
    tweet = request.form.get("tweet")
    res = ui_response(tweet)
    wing = res[0]
    reply1 = res[1]
    reply2 = res[2]
    return chat()

@app.route("/chat", methods=["GET"])
def chat():
    global wing, tweet, reply1, reply2
    return render_template(wing_map[wing], tweet=tweet, wing=wing, reply1=reply1, reply2=reply2)

if __name__ == "__main__":
    app.run(debug=True)