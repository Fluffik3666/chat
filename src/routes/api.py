from flask import Blueprint, render_template, jsonify

blueprint = Blueprint('api', __name__, static_folder='../static/')

@blueprint.route('/health')
def health():
    return jsonify({"status": "healthy", "online":True})