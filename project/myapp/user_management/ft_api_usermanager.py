from myapp.models import CustomUser
from typing import Dict, Tuple
from authlib.integrations.httpx_client import OAuth2Client
from django.conf import settings
from pydantic import BaseModel
from typing import Optional

class FourtyTwoUserInfo(BaseModel):
    """
    Data model representing user information retrieved from the 42 API.

    Attributes:
        id (int): The unique identifier of the user.
        url (str): The URL to the user's profile.
        login (str): The user's login name.
        first_name (str): The user's first name.
        last_name (str): The user's last name.
        email (str): The user's email address.
        avatar_image_link (Optional[str]): The URL to the user's avatar image, if available.
    """
    id: int
    url: str
    login: str
    first_name: str
    last_name: str
    email: str
    avatar_image_link: Optional[str] = None




class PongUserManager:
    """
    Manager class to handle OAuth2 authentication and user information retrieval
    from the 42 API.

    Attributes:
        client (OAuth2Client): The OAuth2 client used for authentication and API requests.
        token_url (str): The URL to obtain the OAuth2 token.
        user_info_url (str): The URL to retrieve user information from the 42 API.
    """


    def __init__(self) -> None:
        """
        Initialize the PongUserManager with OAuth2 client credentials and endpoints.
        """
        self.client = OAuth2Client(
            client_id=settings.TRANSCENDENCE_APP_INTRA42_UID,
            client_secret=settings.TRANSCENDENCE_APP_INTRA42_SECRET,
            redirect_uri=settings.TRANSCENDENCE_APP_INTRA42_REDIRECT_URI,
        )
        self.token_url = 'https://api.intra.42.fr/oauth/token'
        self.user_info_url = 'https://api.intra.42.fr/v2/me'


    def get_authorization_url(self) -> Tuple[str, str]:
        """
        Generate the authorization URL to redirect users for 42 OAuth2 authentication.

        Returns:
            Tuple[str, str]: A tuple containing the authorization URL and the state parameter.
        """
        authorization_endpoint = 'https://api.intra.42.fr/oauth/authorize'
        return self.client.create_authorization_url(authorization_endpoint)


    def fetch_token(self, code: str) -> Dict[str, str]:
        """
        Exchange the authorization code for an access token.

        Args:
            code (str): The authorization code received from the 42 OAuth2 provider.

        Returns:
            Dict[str, str]: A dictionary containing the access token and related information.

        Raises:
            ValueError: If the token cannot be fetched.
        """
        token = self.client.fetch_token(
            self.token_url,
            code=code,
            grant_type='authorization_code',
        )

        # Set the token for the client
        self.client.token = token

        return token

    def get_user_info(self) -> Dict[str, str]:
        """
        Retrieve the authenticated user's information from the 42 API.

        Returns:
            Dict[str, str]: A dictionary containing the user's information.

        Raises:
            ValueError: If the token is not set before making the request.
            HTTPError: If the request to the user info endpoint fails.
        """
        if not self.client.token:
            raise ValueError("Token is not set. Please fetch the token first.")

        response = self.client.get(self.user_info_url)
        response.raise_for_status()
        return response.json()

    def extract_fields_from_user_info(self, user_info: Dict) -> FourtyTwoUserInfo:
        """
        Extract relevant fields from the raw user information dictionary and
        populate a FourtyTwoUserInfo instance.

        Args:
            user_info (Dict): The raw user information dictionary obtained from the 42 API.

        Returns:
            FourtyTwoUserInfo: An instance containing the extracted user information.
        """
        return FourtyTwoUserInfo(
            id=user_info["id"],
            url=user_info["url"],
            login=user_info["login"],
            first_name=user_info["first_name"],
            last_name=user_info["last_name"],
            email=user_info["email"],
            avatar_image_link=user_info.get("image", {}).get("link")
        )
