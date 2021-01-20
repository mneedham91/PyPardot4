'''

'''
__author__ = 'eb'

from logging import Logger
from typing import Optional, Dict, TypeVar, Generic

import requests

T = TypeVar("T", bound="AuthHandler")


class AuthHandler(Generic[T]):
    """Abstract base class for handling authentication"""

    def __init__(self, logger: Optional[Logger] = None) -> None:
        super().__init__()
        self.logger = logger

    def handle_authentication(self) -> bool:
        raise NotImplementedError(f"handle_authentication() called on abstract base class {self.__class__}")

    def auth_header(self) -> Dict:
        raise NotImplementedError(f"auth_header() called on abstract base class {self.__class__}")


class UserAuthHandler(AuthHandler[T]):
    """Abstract base class for handling authentication that requires a username and password"""

    def __init__(self, username: str, password: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.username = username
        self.password = password

    def handle_authentication(self) -> bool:
        raise NotImplementedError(
            f"handle_authentication() called on {self.__class__}.  Should be handled by PardotAPI")

    def auth_header(self) -> Dict:
        raise NotImplementedError(
            f"auth_header() called on {self.__class__}.  Should be handled by PardotAPI")


class TraditionalAuthHandler(UserAuthHandler[T]):
    """Handles authentication of Pardot-only users"""

    def __init__(self, username: str, password: str, userkey: str, **kwargs) -> None:
        super().__init__(username=username, password=password, **kwargs)
        self.userkey = userkey


class OAuthHandler(UserAuthHandler[T]):
    """
    Handles authentication of SSO Pardot users via OAuth2 when
    dependent on username, password, consumer_key, consumer_secret and busines_unit_id.
    """

    def __init__(self, username: str, password: str,
                 consumer_key: str, consumer_secret: str, business_unit_id: str,
                 token: Optional[str] = None, is_sandbox: bool = False, **kwargs) -> None:
        super().__init__(username=username, password=password, **kwargs)
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.business_unit_id: Optional[str] = business_unit_id
        self.token = token
        self.is_sandbox = is_sandbox
        self.access_token: Optional[str] = None

    def handle_authentication(self) -> bool:
        params = {
            "grant_type": "password",
            "client_id": self.consumer_key,
            "client_secret": self.consumer_secret,
            "username": self.username,
            "password": (self.password + self.token) if self.token is not None else self.password
        }
        prefix = "test" if self.is_sandbox else "login"
        url = f"https://{prefix}.salesforce.com/services/oauth2/token"
        r = requests.post(url, params=params)
        content = r.json()
        self.access_token = content.get("access_token")
        self.logger and self.logger.debug(f"Retrieved oauth access_token for {content.get('instance_url')}")
        return True

    def auth_header(self) -> Dict:
        return {"Authorization": f"Bearer {self.access_token}",
                "Pardot-Business-Unit-Id": self.business_unit_id,
                "Content-Type": "application/x-www-form-urlencoded"}
