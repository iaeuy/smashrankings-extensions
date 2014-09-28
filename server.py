import sqlite3
import requests
from flask import *
from extension import *
from contextlib import closing

DATABASE = 'smashrankings.db'
DEBUG = True
SECRET_KEY = 'smash4lyfe'
URL = 'http://garsh0p.no-ip.biz:5100/'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_db()
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        for region in get_all_regions():
            for player in get_players_in_region(region):
                db.execute('insert into playerdata (name, data) values (?, ?)', [player.name, player.id])
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
    players = [dict(name=session.get('player1')['name'], id=session.get('player1')['data']), \
            dict(name=session.get('player2')['name'], id=session.get('player2')['data'])]
    return render_template('show_comparison.html', players=players)

@app.route('/search', methods=['POST'])
def search_players():
    session.pop('player1', None)
    session.pop('player2', None)
    p1 = request.form['player1'].lower()
    p2 = request.form['player2'].lower()
    cur = g.db.execute('select name from playerdata')
    players = [row[0].lower() for row in cur.fetchall()]
    if p1 not in players or p2 not in players:
        flash('Could not find player(s)')
    else:
        session['player1'] = query_db('select * from playerdata where name = ?', [p1], one=True)
        session['player2'] = query_db('select * from playerdata where name = ?', [p2], one=True)
    return redirect(url_for('show_comparison'))

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run()
