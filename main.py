from flask import Flask
from src.routes.pages import blueprint as b

app = Flask(__name__)
app.register_blueprint(b)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
