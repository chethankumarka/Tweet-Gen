from flask import Flask, render_template, request
from retrieval_model.retrieval import response
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    print("****")
    print(request.form['username'])
    print(request.form['password'])
    if request.method == 'POST':
        if request.form['username'] == 'user' or request.form['password'] == 'password':
            return render_template('chat.html')
        else:
            return render_template('welcome.html')
    # print(error)
    return render_template('chat.html')

@app.route('/chat', methods=['GET'])
def chat():
    return render_template('chat.html')

@app.route('/response', methods=['POST'])
def response():
    print(request.form)
    tweet = request.form.get('tweet')
    model_response = response(tweet)
    return model_response

if __name__ == '__main__':
    app.run(debug=True)