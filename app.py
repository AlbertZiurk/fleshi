from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/profile/<username>')
def perfil(username):
    return render_template("profile.html", username=username)

if __name__ == '__main__':
    app.run(debug=True)