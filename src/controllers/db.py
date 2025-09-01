import pytz
from datetime import datetime

class DB:
    def __init__(self):
        pass
    
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
        
        return self._format_response(
            True,
            data={
                "user_id": "7268A37D-D46F-4A0F-B2AA-54902FEEA729",
                "username": username,
                "token": token,
                "created_at": self._get_time()
            }
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
        
        return self._format_response(
            True,
            data={
                "chat_id": "C4E8F9A2-B3D7-4C5E-8F9A-2B3D7C5E8F9A",
                "name": name,
                "members": members,
                "created_at": self._get_time()
            }
        )
    
    def send_message(
        self,
        content: str = None
    ) -> dict:
        if content is None or content == "":
            return self._format_response(
                False,
                error_msg="No message provided."
            )
        
        return self._format_response(
            True,
            data={
                "message_id": "790C96CB-8877-4870-9AD3-47DF1625175E",
                "content": content,
                "timestamp": self._get_time()
            }
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
        
        user_data = {
            "user_id": user_id,
            "username": "john",
            "created_at": "2025-01-15T14:30:45.123456+00:00"
        }
        
        if is_self:
            user_data["chats"] = [
                {
                    "chat_id": "C4E8F9A2-B3D7-4C5E-8F9A-2B3D7C5E8F9A",
                    "name": "test chat",
                    "created_at": "2025-01-15T14:30:45.123456+00:00"
                },
                {
                    "chat_id": "D5F9G0B3-C4E7-5D6F-9G0B-3C4E7D6F9G0B",
                    "name": "another chat",
                    "created_at": "2025-01-16T10:15:30.789123+00:00"
                }
            ]
        
        return self._format_response(
            True,
            data={
                "user": user_data
            }
        )
    
    def get_chat(
        self,
        chat_id: str = None
    ) -> dict:
        if chat_id is None or chat_id == "":
            return self._format_response(
                False,
                error_msg="No chat_id provided."
            )
        
        return self._format_response(
            True,
            data={
                "chat": {
                    "info": {
                        "chat_id": chat_id,
                        "members": [
                            "7268A37D-D46F-4A0F-B2AA-54902FEEA729",
                            "7268A37D-D46F-4A0F-B2AA-54902FEEA735"
                        ],
                        "name": "test chat",
                        "created_at": "2025-01-15T14:30:45.123456+00:00"
                    },
                    "messages": [
                        {
                            "message_id": "790C96CB-8877-4870-9AD3-47DF1625175E",
                            "content": "hi",
                            "sender_id": "7268A37D-D46F-4A0F-B2AA-54902FEEA729",
                            "timestamp": "2025-01-15T14:30:45.123456+00:00"
                        },
                        {
                            "message_id": "790C96CB-8877-4870-9AD3-47DF1625175F",
                            "content": "hey hru?",
                            "sender_id": "7268A37D-D46F-4A0F-B2AA-54902FEEA735",
                            "timestamp": "2025-01-15T14:31:22.456789+00:00"
                        }
                    ]
                }
            }
        )
    
    def get_messages(
        self,
        chat_id: str = None
    ) -> dict:
        if chat_id is None or chat_id == "":
            return self._format_response(
                False,
                error_msg="No chat_id provided."
            )
        
        return self._format_response(
            True,
            data={
                "messages": [
                    {
                        "message_id": "790C96CB-8877-4870-9AD3-47DF1625175E",
                        "content": "hi",
                        "sender_id": "7268A37D-D46F-4A0F-B2AA-54902FEEA729",
                        "timestamp": "2025-01-15T14:30:45.123456+00:00"
                    },
                    {
                        "message_id": "790C96CB-8877-4870-9AD3-47DF1625175F",
                        "content": "hey hru?",
                        "sender_id": "7268A37D-D46F-4A0F-B2AA-54902FEEA735",
                        "timestamp": "2025-01-15T14:31:22.456789+00:00"
                    }
                ]
            }
        )