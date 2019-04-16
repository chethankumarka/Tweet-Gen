from flask import Flask, render_template, request
from retrieval_model.retrieval import response
app = Flask(__name__)

user_profile_map = {"john.daw@asu.edu": "chat_left.html", "mary.sue@asu.edu": "chat_right.html"}
users = {"john.daw@asu.edu": "john123", "mary.sue@asu.edu": "mary123"}

user = ""

@app.route("/")
def home():
    return render_template("welcome.html")

@app.route("/welcome")
def welcome():
    return render_template("welcome.html")

@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        global user
        user = request.form.get("username").lower()

        if user in users.keys() and request.form.get("password") == users[user]:
            return render_template(user_profile_map[user])
        else:
            return render_template("welcome.html")

@app.route("/chat", methods=["GET"])
def chat():
    return render_template(user_profile_map[user])

@app.route("/response", methods=["POST"])
def response_model():
    tweet = request.form.get("tweet")
    model_response = response(tweet)
    return model_response

if __name__ == "__main__":
    app.run(debug=True)