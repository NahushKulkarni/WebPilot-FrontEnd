from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def search():
    search_term = request.form['search']
    query = search_term.replace(' ', '+')
    return redirect(url_for('search_query', query=query))


@app.route('/results/')
def Results():
    return render_template('results.html', Results=Results)


app.run(debug=True, port=5000)
