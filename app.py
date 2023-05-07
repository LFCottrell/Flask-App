from flask import Flask,render_template, request

app = Flask(__name__)

@app.route('/')
def home(name):
    return render_template("form.html")

@app.route('/test')
def test():
    return render_template("new.html")

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    # Do something with the form data
    return 'Thanks for submitting the form!'

if __name__ == '__main__':
    app.run(debug=True)