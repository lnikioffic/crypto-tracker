from fastapi import HTTPException, Request, status
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.security import OAuth2PasswordBearer


class OAuth2PasswordBearerCookie(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> str | None:
        token: str | None = request.cookies.get('access_token')
        if not token:
            token = request.cookies.get('refresh_token')

        scheme, param = get_authorization_scheme_param(token)
        if not token or scheme.lower() != 'bearer':
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Not authenticated',
                    headers={'WWW-Authenticate': 'Bearer'},
                )
            else:
                return None
        return param
