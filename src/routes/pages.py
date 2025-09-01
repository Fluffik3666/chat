from flask import Blueprint, render_template, jsonify

blueprint = Blueprint('pages', __name__, static_folder='../static/', template_folder='../templates/')

@blueprint.route('/')
def index():
    return render_template('index.html')

@blueprint.route('/health')
def health():
    return jsonify({"status": "healthy", "online":True})
