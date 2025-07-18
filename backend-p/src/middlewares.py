import logging
import time
from collections.abc import Callable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

log = logging.getLogger(__name__)


class TracingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next: Callable):
        start_time = time.time()

        route_path = request.url.path
        method = request.method

        response = await call_next(request)

        process_time = time.time() - start_time

        log.info(f'{method} {route_path} processed in {process_time:.4f} seconds')

        response.headers['X-Process-Time'] = str(process_time)

        return response
