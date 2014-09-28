import sqlite3
import requests
from flask import *
from contextlib import closing

DATABASE = 'playerdata.db'
DEBUG = True
URL = 'http://garsh0p.no-ip.biz:5100/'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        regreq = requests.get(URL + 'regions')
        for region in regreq.json()['regions']:

        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exeception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def show_comparison():
    players = [session.get('player1'), session.get('player2')]
    return render_template('show_comparison.html', players=players)

@app.route('/search', methods=['POST'])
def search_players():
    error = None
    if request.method == 'POST':
        cur = g.db.execute('select name from playerdata')
        players = [row[0] for row in curr.fetchall()]
        p1 = request.form['player1']
        p2 = request.form['player2']
        session.pop('player1', None)
        session.pop('player2', None)
        if p1 not in players or p2 not in players:
            flash('Could not find player(s)')
        else:
            session['player1'] = p1
            session['player2'] = p2
    return redirect(url_for('show_comparison'))

if __name__ == '__main__':
    app.run()

