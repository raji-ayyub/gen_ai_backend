import jwt
from dotenv import load_dotenv
import os

from datetime import datetime, timedelta
from fastapi import Depends, Request, security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


bearer = HTTPBearer()

load_dotenv()


secret_key = os.getenv("secret_key")
expiry_time = int(os.getenv("token_time"))

def create_token(details):
    expire = datetime.now() + timedelta(minutes=expiry_time)

    details.update({"exp": expire})

    encoded_jwt = jwt.encode(details, secret_key)

    return encoded_jwt


def verify_token(request: HTTPAuthorizationCredentials = Depends(bearer)):
    # payload = Request.headers.get("Authorization")

    # token = payload.split(" ")[1]

    token = request.credentials

    verified_token = jwt.decode(token, secret_key, algorithms=["HS256"])

    expiry_time = verified_token.get("exp")

    return{
        "email": verified_token.get("email"),
        "usertype": verified_token.get("usertype"),
        "user_id": verified_token.get("user_id")
    }