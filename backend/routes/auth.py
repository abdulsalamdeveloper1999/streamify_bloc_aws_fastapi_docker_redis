from fastapi import APIRouter, Cookie, Depends, HTTPException, Response
import boto3
import logging
from botocore.exceptions import ClientError
from sqlalchemy.orm import Session
from cognito_secrets import SecretKeys
from db.db import get_db
from db.middleware.auth_middleware import get_current_user
from helper.helper import get_secret_hash
from models.user import User
from pydantic_models.auth_models import (
    ConfirmCodeRequest,
    ConfirmSignupRequest,
    LoginRequest,
    SignUpRequest,
)

# Setup logging
logger = logging.getLogger(__name__)

# Secret Keys and Configs
secret_keys = SecretKeys()
COGNITO_CLIENT_ID = secret_keys.COGNITO_CLIENT_ID
COGNITO_CLIENT_SECRET = secret_keys.COGNITO_CLIENT_SECRET
REGION_NAME = secret_keys.REGION_NAME

# Initialize FastAPI Router
auth_router = APIRouter()

# Initialize Cognito client
cognito_client = boto3.client("cognito-idp", region_name=REGION_NAME)


@auth_router.post("/signup")
def signup_user(
    data: SignUpRequest,
    db: Session = Depends(get_db),
):
    """
    Sign up a new user to AWS Cognito.
    """
    try:
        secret_hash = get_secret_hash(
            data.email,
            COGNITO_CLIENT_ID,
            COGNITO_CLIENT_SECRET,
        )

        response = cognito_client.sign_up(
            ClientId=COGNITO_CLIENT_ID,
            Username=data.email,
            Password=data.password,
            SecretHash=secret_hash,
            UserAttributes=[
                {"Name": "email", "Value": data.email},
                {"Name": "name", "Value": data.name},
            ],
        )
        # return {
        #     "message": "User sign-up initiated. Please check your email to confirm the account if required.",
        #     "user_sub": response.get("UserSub"),
        # }
        cognito_sub = response.get("UserSub")

        if not cognito_sub:
            raise HTTPException(400, "Cognito did not return a valid user sub")

        new_user = User(
            name=data.name,
            email=data.email,
            cognito_sub=cognito_sub,
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "message": "User sign-up initiated. Please check your email to confirm the account if required.",
            "user_sub": response.get("UserSub"),
        }

    except ClientError as e:
        error_message = e.response["Error"]["Message"]
        logger.error(f"Sign-up error: {error_message}")
        raise HTTPException(status_code=400, detail=error_message)


@auth_router.post("/login")
def login_user(data: LoginRequest, response: Response):
    secret_hash = get_secret_hash(
        data.email,
        COGNITO_CLIENT_ID,
        COGNITO_CLIENT_SECRET,
    )
    try:
        api_response = cognito_client.initiate_auth(
            ClientId=COGNITO_CLIENT_ID,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": data.email,
                "PASSWORD": data.password,
                "SECRET_HASH": secret_hash,
            },
        )

        authentication = api_response["AuthenticationResult"]
        if not authentication:
            raise HTTPException(
                status_code=400, detail="Authentication access not found"
            )

        access_token = authentication["AccessToken"]
        refresh_token = authentication["RefreshToken"]

        response.set_cookie(
            key="refresh_token", value=refresh_token, httponly=True, secure=True
        )

        response.set_cookie(
            key="access_token", value=access_token, httponly=True, secure=True
        )

        return {"message": "User logged in successfully"}

    except ClientError as e:
        error_message = e.response["Error"]["Message"]
        logger.error(f"login error: {error_message}")
        raise HTTPException(status_code=400, detail=error_message)


@auth_router.post("/confirm-signup")
def confirm_signup(
    data: ConfirmSignupRequest,
):
    secret_hash = get_secret_hash(
        data.email,
        COGNITO_CLIENT_ID,
        COGNITO_CLIENT_SECRET,
    )

    try:
        response = cognito_client.confirm_sign_up(
            ClientId=COGNITO_CLIENT_ID,
            Username=data.email,
            ConfirmationCode=data.otp,
            SecretHash=secret_hash,
        )
        return response

    except ClientError as e:
        error_message = e.response["Error"]["Message"]
        raise HTTPException(status_code=400, detail=error_message)


@auth_router.post("/resend-code")
def resend_code(data: ConfirmCodeRequest):
    try:
        response = cognito_client.resend_confirmation_code(
            ClientId=COGNITO_CLIENT_ID,
            SecretHash=get_secret_hash(
                data.email,
                COGNITO_CLIENT_ID,
                COGNITO_CLIENT_SECRET,
            ),
            Username=data.email,
        )
        return response

    except ClientError as e:
        error_message = e.response["Error"]["Message"]
        raise HTTPException(status_code=400, detail=error_message)


@auth_router.post("/confirm-signup")
def confirm_signup(
    data: ConfirmSignupRequest,
):
    secret_hash = get_secret_hash(
        data.email,
        COGNITO_CLIENT_ID,
        COGNITO_CLIENT_SECRET,
    )

    try:
        response = cognito_client.confirm_sign_up(
            ClientId=COGNITO_CLIENT_ID,
            Username=data.email,
            ConfirmationCode=data.otp,
            SecretHash=secret_hash,
        )
        return response

    except ClientError as e:
        error_message = e.response["Error"]["Message"]
        raise HTTPException(status_code=400, detail=error_message)


@auth_router.post("/refresh-token")
def refresh_token(
    refresh_token: str = Cookie(None),
    response: Response = None,
    user_cognito_sub: str = Cookie(None)
):

    secret_hash = get_secret_hash(
        user_cognito_sub,
        COGNITO_CLIENT_ID,
        COGNITO_CLIENT_SECRET,
    )

    try:
        cognito_response = cognito_client.initiate_auth(
            ClientId=COGNITO_CLIENT_ID,
            AuthFlow="REFRESH_TOKEN_AUTH",
            AuthParameters={
                "REFRESH_TOKEN": refresh_token,
                "SECRET_HASH": secret_hash,
            },
        )

        authentication = cognito_response["AuthenticationResult"]
        if not authentication:
            raise HTTPException(
                status_code=400, detail="Authentication access not found"
            )

        access_token = authentication["AccessToken"]

        response.set_cookie(
            key="access_token", value=access_token, httponly=True, secure=True
        )

        return {"message": "Access token refreshed successfully"}

    except ClientError as e:
        error_message = e.response["Error"]["Message"]
        raise HTTPException(status_code=400, detail=error_message)


@auth_router.get("/me")
def protected_route(user=Depends(get_current_user)):
    return {"message":"You are authenticated","user":user}