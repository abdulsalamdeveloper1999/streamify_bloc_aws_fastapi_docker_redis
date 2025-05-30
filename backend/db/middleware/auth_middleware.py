import boto3
from fastapi import Cookie, HTTPException

from cognito_secrets import SecretKeys


cognito_client=boto3.client("cognito-idp",region_name=SecretKeys().REGION_NAME,)



def _get_user_from_cognito(access_token:str):
    try:
        user_res=cognito_client.get_user(AccessToken=access_token)
        return { attr["Name"]:attr["Value"] for attr in user_res.get("UserAttributes")}
        return user_res


    except Exception as e:
        raise HTTPException(status_code=500,detail="Error fetching user")
    
def get_current_user(access_token:str=Cookie(None)):
    try:
        if not access_token:
            raise HTTPException(status_code=401,detail="User not logged in!")
        return _get_user_from_cognito(access_token=access_token)
    

    except Exception as e:
        error_message=e.response["Error"]["Message"]
        raise HTTPException(status_code=401,detail=f"Error:{error_message}")
