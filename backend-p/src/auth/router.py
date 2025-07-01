from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

http_bearer = HTTPBearer(auto_error=False)
auth_router = APIRouter(
    prefix='/auth', tags=['Auth', 'User'], dependencies=[Depends(http_bearer)]
)
user_router = APIRouter(prefix='/user', tags=['User'])
