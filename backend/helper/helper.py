import base64
import hashlib
import hmac

def get_secret_hash(username: str, client_id: str, client_secret: str) -> str:
    """
    Generate the AWS Cognito secret hash for secure user authentication.

    Args:
        username (str): The username (typically the email).
        client_id (str): The Cognito App Client ID.
        client_secret (str): The Cognito App Client Secret.

    Returns:
        str: Base64-encoded HMAC-SHA256 digest as the secret hash.
    """
    message = username + client_id
    digest = hmac.new(
        key=client_secret.encode("utf-8"),
        msg=message.encode("utf-8"),
        digestmod=hashlib.sha256
    ).digest()
    
    return base64.b64encode(digest).decode("utf-8")
