import time
from typing import Dict
import jwt


def token_response(token: str):
    return {
        "access_token": token
    }


def signJWT(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": 5184000
    }
    token = jwt.encode(payload, 'secret', algorithm='HS256')

    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, 'secret', algorithms='HS256')
        return decoded_token if decoded_token["expires"] >= 5184000 else None
    except:
        return {}