from pathlib import Path

from pydantic import BaseModel

CERTS_DIR = Path.cwd() / 'certs'


class AuthJWTSettings(BaseModel):
    private_key_path: Path = CERTS_DIR / 'jwt-private.pem'
    public_key_path: Path = CERTS_DIR / 'jwt-public.pem'
    algorithm: str = 'RS256'
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30


auth_jwt_settings = AuthJWTSettings()
