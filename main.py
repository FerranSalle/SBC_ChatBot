from flask import Flask, render_template, request

app = Flask(__name__, static_folder='static', template_folder='templates')


@app.route('/')
def index():
    return render_template('index.html')


# Only post requests are allowed
@app.route('/api/message', methods=['POST'])
def message():
    # Get the JSON data sent from the front-end.
    data = request.get_json()
    print(data)
    return 'Message received!'
