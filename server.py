from flask import *
from extension import *

DEBUG = True
SECRET_KEY = 'smash4lyfe'
URL = 'http://garsh0p.no-ip.biz:5100/'

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def show_comparison():
    players = [None]
    if session.get('player1'):
        p1 = player_by_name(session.get('player1'), session.get('region'))
        p2 = player_by_name(session.get('player2'), session.get('region'))
        session.pop('player1', None)
        session.pop('player2', None)
        if not isinstance(p1, str) or not isinstance(p2, str):
            players = [dict(name=p1.name, rank=p1.rank), dict(name=p2.name, rank=p2.rank)]
    return render_template('show_comparison.html', regions=get_all_regions(), players=players)

@app.route('/search', methods=['POST'])
def search_players():
    session['player1'] = request.form['player1']
    session['player2'] = request.form['player2']
    session['region'] = request.form['region']
    if not session.get('player1'):
        flash('Could not find player(s)')
    return redirect(url_for('show_comparison'))

if __name__ == '__main__':
    app.run()
