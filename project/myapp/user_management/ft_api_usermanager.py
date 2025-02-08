
from myapp.models import CustomUser
from typing import Dict, Tuple
from authlib.integrations.httpx_client import OAuth2Client
from django.conf import settings

from pydantic import BaseModel
from typing import List, Union, Optional



class FourtyTwoUserInfo(BaseModel):
    id: int
    url: str
    login: str
    first_name: str
    last_name: str
    email: str
    avatar_image_link: Optional[str] = None



class PongUserManager:
    def __init__(self) -> None:
        self.client = OAuth2Client(
            client_id=settings.TRANSCENDENCE_APP_INTRA42_UID,
            client_secret=settings.TRANSCENDENCE_APP_INTRA42_SECRET,
            redirect_uri=settings.TRANSCENDENCE_APP_INTRA42_REDIRECT_URI,
        )
        self.token_url = 'https://api.intra.42.fr/oauth/token'
        self.user_info_url = 'https://api.intra.42.fr/v2/me'

    def get_authorization_url(self) -> Tuple[str, str]:
        authorization_endpoint = 'https://api.intra.42.fr/oauth/authorize'
        return self.client.create_authorization_url(authorization_endpoint)

    def fetch_token(self, code: str) -> Dict[str, str]:
        token = self.client.fetch_token(
            self.token_url,
            code=code,
            grant_type='authorization_code',
        )

        #set token 
        self.client.token = token

        return token

    def get_user_info(self) -> Dict[str, str]:
        if not self.client.token:
            raise ValueError("Token is not set. Please fetch the token first.")

        response = self.client.get(self.user_info_url)
        response.raise_for_status()
        return response.json()
    
    def extract_fields_from_user_info(self, user_info: Dict) -> FourtyTwoUserInfo:

        return FourtyTwoUserInfo(
            id=user_info["id"],
            url=user_info["url"],
            login=user_info["login"],
            first_name=user_info["first_name"],
            last_name=user_info["last_name"],
            email=user_info["email"],
            avatar_image_link=user_info.get("image", {}).get("link")
        )


