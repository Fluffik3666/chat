from flask import Flask
from src.routes.pages import blueprint as b
from src.routes.api import blueprint as a

app = Flask(__name__, static_folder='src/static', static_url_path='/static')

app.secret_key = 'uyawefgiyofydtawef6781q23refyu9124g3btruw78xjuszgywdt0cfhjklmnot5,q2dr.00qdfhjklorstuyz5,a2ewi0qdefijkloprstuy3456789a2weiloprtu34567890qa2ywseijkloprtuy34567890qa2ws5qeijkloprstuy3467890a2w25qeijkloprstuy347890aw'
app.register_blueprint(b)
app.register_blueprint(a, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)