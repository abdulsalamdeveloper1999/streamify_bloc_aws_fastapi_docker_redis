from pydantic import BaseModel


class SignUpRequest(BaseModel):
    name: str
    email:str
    password:str

class LoginRequest(BaseModel):
    email:str
    password:str

class ConfirmSignupRequest(BaseModel):
    email:str
    otp:str

class ConfirmCodeRequest(BaseModel):
    email:str