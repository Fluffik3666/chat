from flask import Blueprint, render_template, jsonify, session

blueprint = Blueprint('pages', __name__, static_folder='../static/', template_folder='../templates/')

@blueprint.route('/')
def index():
    return render_template('index.html') # landing page, project intro

@blueprint.route('/accounts/create')
def create_account():
    return render_template('create_account.html') # create account, txt file based

@blueprint.route('/chats')
def chats():
    return render_template('chats.html') # view all chats

@blueprint.route('/chats/<id>')
def chat_detail(id):
    if not id:
        return jsonify({
            "success" : False,
            "error": "No chat provided in arguments"
        })
    
    return render_template('chat_detail.html', id=str(id)) # chat detail

@blueprint.route('/accounts/<id>')
def account_detail(id):
    if not id:
        return jsonify({
            "success" : False,
            "error": "No account provided in arguments"
        })
    
    is_self = session.get('user_id') == id
    
    return render_template('account_detail.html', id=str(id), is_self=bool(is_self)) # account detail, management