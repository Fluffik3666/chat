import os
import pytz
from datetime import datetime
from firebase_admin import firestore
import firebase_admin
from firebase_admin import credentials
import uuid

class DB:
    def __init__(self, credentials_path=None):
        if not firebase_admin._apps:
            if credentials_path:
                cred = credentials.Certificate(credentials_path)
            else:
                cred_dict = {
                    "type": os.environ.get('FIREBASE_TYPE'),
                    "project_id": os.environ.get('FIREBASE_PROJECT_ID'),
                    "private_key_id": os.environ.get('FIREBASE_PRIVATE_KEY_ID'),
                    "private_key": os.environ.get('FIREBASE_PRIVATE_KEY'),
                    "client_email": os.environ.get('FIREBASE_CLIENT_EMAIL'),
                    "client_id": os.environ.get('FIREBASE_CLIENT_ID'),
                    "auth_uri": os.environ.get('FIREBASE_AUTH_URI'),
                    "token_uri": os.environ.get('FIREBASE_TOKEN_URI'),
                    "auth_provider_x509_cert_url": os.environ.get('FIREBASE_AUTH_PROVIDER_X509_CERT_URL'),
                    "client_x509_cert_url": os.environ.get('FIREBASE_CLIENT_X509_CERT_URL'),
                    "universe_domain": os.environ.get('FIREBASE_UNIVERSE_DOMAIN')
                }
                cred = credentials.Certificate(cred_dict)
            
            firebase_admin.initialize_app(cred)
        
        self.db = firestore.client()
    
    def _format_response(self, success: bool, error_msg: str = None, data: dict = None) -> dict:
        rt = {
            "success": success
        }
        
        try:
            if error_msg:
                rt["error_msg"] = str(error_msg)
        
            if data:
                rt["data"] = dict(data)
        except Exception as e:
            return {
                "success": False,
                "error_msg": f"Error when formatting response. The data may be malformed, please check! Error: {str(e)}"
            }
        
        return rt
    
    def _get_time(self) -> str:
        uk_tz = pytz.timezone('Europe/London')
        return str(datetime.now(uk_tz).isoformat())
    
    def create_user(
        self,
        username: str = None,
        token: str = None
    ) -> dict:
        if username is None or username == "":
            return self._format_response(
                False,
                error_msg="No username provided."
            )
        
        if token is None or token == "":
            return self._format_response(
                False,
                error_msg="No token provided."
            )
        
        try:
            user_id = str(uuid.uuid4()).upper()
            created_at = self._get_time()
            
            user_data = {
                "user_id": user_id,
                "username": username,
                "token": token,
                "created_at": created_at
            }
            
            self.db.collection('users').document(user_id).set(user_data)
            
            return self._format_response(
                True,
                data=user_data
            )
        except Exception as e:
            return self._format_response(
                False,
                error_msg=f"Failed to create user: {str(e)}"
            )
    
    def create_chat(
        self,
        name: str = None,
        members: list = None
    ) -> dict:
        if name is None or name == "":
            return self._format_response(
                False,
                error_msg="No chat name provided."
            )
        
        if members is None or len(members) == 0:
            return self._format_response(
                False,
                error_msg="No members provided."
            )
        
        try:
            chat_id = str(uuid.uuid4()).upper()
            created_at = self._get_time()
            
            chat_data = {
                "chat_id": chat_id,
                "name": name,
                "members": members,
                "created_at": created_at
            }
            
            self.db.collection('chats').document(chat_id).set(chat_data)
            
            return self._format_response(
                True,
                data=chat_data
            )
        except Exception as e:
            return self._format_response(
                False,
                error_msg=f"Failed to create chat: {str(e)}"
            )
    
    def send_message(
        self,
        content: str = None,
        chat_id: str = None,
        sender_id: str = None
    ) -> dict:
        if content is None or content == "":
            return self._format_response(
                False,
                error_msg="No message provided."
            )
        
        if chat_id is None or chat_id == "":
            return self._format_response(
                False,
                error_msg="No chat_id provided."
            )
        
        if sender_id is None or sender_id == "":
            return self._format_response(
                False,
                error_msg="No sender_id provided."
            )
        
        try:
            message_id = str(uuid.uuid4()).upper()
            timestamp = self._get_time()
            
            message_data = {
                "message_id": message_id,
                "content": content,
                "sender_id": sender_id,
                "timestamp": timestamp
            }
            
            self.db.collection('chats').document(chat_id).collection('messages').document(message_id).set(message_data)
            
            return self._format_response(
                True,
                data=message_data
            )
        except Exception as e:
            return self._format_response(
                False,
                error_msg=f"Failed to send message: {str(e)}"
            )
    
    def get_user(
        self,
        user_id: str = None,
        is_self: bool = False
    ) -> dict:
        if user_id is None or user_id == "":
            return self._format_response(
                False,
                error_msg="No user_id provided."
            )
        
        try:
            user_ref = self.db.collection('users').document(user_id)
            user_doc = user_ref.get()
            
            if not user_doc.exists:
                return self._format_response(
                    False,
                    error_msg="User not found."
                )
            
            user_data = user_doc.to_dict()
            
            if is_self:
                chats_ref = self.db.collection('chats').where('members', 'array_contains', user_id)
                chats = chats_ref.stream()
                
                user_data["chats"] = []
                for chat in chats:
                    chat_data = chat.to_dict()
                    user_data["chats"].append({
                        "chat_id": chat_data.get("chat_id"),
                        "name": chat_data.get("name"),
                        "created_at": chat_data.get("created_at")
                    })
            
            return self._format_response(
                True,
                data={"user": user_data}
            )
        except Exception as e:
            return self._format_response(
                False,
                error_msg=f"Failed to get user: {str(e)}"
            )
    
    def get_chat(
        self,
        chat_id: str = None,
        requesting_user_id: str = None
    ) -> dict:
        if chat_id is None or chat_id == "":
            return self._format_response(False, error_msg="No chat_id provided.")

        try:
            chat_ref = self.db.collection('chats').document(chat_id)
            chat_doc = chat_ref.get()

            if not chat_doc.exists:
                return self._format_response(False, error_msg="Chat not found.")

            chat_data = chat_doc.to_dict()
            
            if requesting_user_id and requesting_user_id not in chat_data.get('members', []):
                return self._format_response(False, error_msg="You are not a member of this chat.")

            messages_ref = chat_ref.collection('messages').order_by('timestamp')
            messages = messages_ref.stream()

            messages_list = []
            for msg in messages:
                messages_list.append(msg.to_dict())

            return self._format_response(True, data={"chat": {"info": chat_data, "messages": messages_list}})
        except Exception as e:
            return self._format_response(False, error_msg=f"Failed to get chat: {str(e)}")
    
    def get_messages(
        self,
        chat_id: str = None
    ) -> dict:
        if chat_id is None or chat_id == "":
            return self._format_response(
                False,
                error_msg="No chat_id provided."
            )
        
        try:
            messages_ref = self.db.collection('chats').document(chat_id).collection('messages').order_by('timestamp')
            messages = messages_ref.stream()
            
            messages_list = []
            for msg in messages:
                messages_list.append(msg.to_dict())
            
            return self._format_response(
                True,
                data={"messages": messages_list}
            )
        except Exception as e:
            return self._format_response(
                False,
                error_msg=f"Failed to get messages: {str(e)}"
            )
    
    def get_user_by_username(self, username: str = None) -> dict:
        if username is None or username == "":
            return self._format_response(False, error_msg="No username provided.")
        
        try:
            users_ref = self.db.collection('users').where('username', '==', username).limit(1)
            users = list(users_ref.stream())
            
            if not users:
                return self._format_response(False, error_msg="User not found.")
            
            user_data = users[0].to_dict()
            return self._format_response(True, data={"user": user_data})
        except Exception as e:
            return self._format_response(False, error_msg=f"Failed to get user: {str(e)}")
    
    def add_member_to_chat(self, chat_id: str = None, user_id: str = None) -> dict:
        if chat_id is None or chat_id == "":
            return self._format_response(False, error_msg="No chat_id provided.")
    
        if user_id is None or user_id == "":
            return self._format_response(False, error_msg="No user_id provided.")
    
        try:
            chat_ref = self.db.collection('chats').document(chat_id)
            chat_doc = chat_ref.get()

            if not chat_doc.exists:
                return self._format_response(False, error_msg="Chat not found.")

            chat_data = chat_doc.to_dict()
            members = chat_data.get('members', [])

            if user_id in members:
                return self._format_response(False, error_msg="User is already a member.")
        
            members.append(user_id)
            chat_ref.update({'members': members})

            return self._format_response(True, data={"message": "Member added successfully"})
        except Exception as e:
            return self._format_response(False, error_msg=f"Failed to add member: {str(e)}")
    
    def remove_member_from_chat(self, chat_id: str = None, user_id: str = None) -> dict:
        if chat_id is None or chat_id == "":
            return self._format_response(False, error_msg="No chat_id provided.")

        if user_id is None or user_id == "":
            return self._format_response(False, error_msg="No user_id provided.")

        try:
            chat_ref = self.db.collection('chats').document(chat_id)
            chat_doc = chat_ref.get()

            if not chat_doc.exists:
                return self._format_response(False, error_msg="Chat not found.")

            chat_data = chat_doc.to_dict()
            members = chat_data.get('members', [])

            if user_id not in members:
                return self._format_response(False, error_msg="User is not a member.")

            members.remove(user_id)
            chat_ref.update({'members': members})

            return self._format_response(True, data={"message": "Member removed successfully"})
        except Exception as e:
            return self._format_response(False, error_msg=f"Failed to remove member: {str(e)}")
    
    def delete_chat(self, chat_id: str = None) -> dict:
        if chat_id is None or chat_id == "":
            return self._format_response(False, error_msg="No chat_id provided.")

        try:
            chat_ref = self.db.collection('chats').document(chat_id)
            chat_doc = chat_ref.get()

            if not chat_doc.exists:
                return self._format_response(False, error_msg="Chat not found.")

            # Delete all messages in the chat first
            messages_ref = chat_ref.collection('messages')
            messages = messages_ref.stream()

            for message in messages:
                message.reference.delete()

            # Delete the chat document
            chat_ref.delete()

            return self._format_response(True, data={"message": "Chat deleted successfully"})
        except Exception as e:
            return self._format_response(False, error_msg=f"Failed to delete chat: {str(e)}")

    def authenticate_user(self, username: str = None, token: str = None) -> dict:
        if username is None or username == "":
            return self._format_response(False, error_msg="No username provided.")

        if token is None or token == "":
            return self._format_response(False, error_msg="No token provided.")

        try:
            users_ref = self.db.collection('users').where('username', '==', username).where('token', '==', token).limit(1)
            users = list(users_ref.stream())

            if not users:
                return self._format_response(False, error_msg="Invalid username or token.")

            user_data = users[0].to_dict()
            return self._format_response(True, data={"user": user_data})
        except Exception as e:
            return self._format_response(False, error_msg=f"Authentication failed: {str(e)}")