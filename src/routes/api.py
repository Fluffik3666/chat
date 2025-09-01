from flask import Blueprint, render_template, jsonify, request, session, send_from_directory
from src.controllers.db import DB
import secrets

blueprint = Blueprint('api', __name__, static_folder='/static', static_url_path='/static')

db = DB()

@blueprint.route('/health')
def health():
    return jsonify({"status": "healthy", "online": True})

@blueprint.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username') if data else None
    token = secrets.token_urlsafe(32)
    result = db.create_user(username=username, token=token)
    
    if result.get('success'):
        session['user_id'] = result['data']['user_id']
        session['token'] = token
    
    return jsonify(result)

@blueprint.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    is_self = session.get('user_id') == user_id
    return jsonify(db.get_user(user_id=user_id, is_self=is_self))

@blueprint.route('/chat', methods=['POST'])
def create_chat():
    data = request.get_json()
    name = data.get('name') if data else None
    members = data.get('members') if data else None
    return jsonify(db.create_chat(name=name, members=members))

@blueprint.route('/chat/<chat_id>', methods=['GET'])
def get_chat(chat_id):
    return jsonify(db.get_chat(chat_id=chat_id))

@blueprint.route('/chat/<chat_id>/messages', methods=['GET'])
def get_messages(chat_id):
    return jsonify(db.get_messages(chat_id=chat_id))

@blueprint.route('/chat/<chat_id>/message', methods=['POST'])
def send_message(chat_id):
    data = request.get_json()
    content = data.get('content') if data else None
    return jsonify(db.send_message(content=content))