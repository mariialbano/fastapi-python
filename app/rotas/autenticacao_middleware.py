from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

VALOR_TOKEN_SESSAO = "token_senha"

_CAMINHOS_PUBLICOS_EXATOS = frozenset(
    {"/", "/health", "/login", "/logout", "/registro"}
)
_CAMINHO_STATIC_PREFIX = "/static"


def _camino_publico(caminho: str) -> bool:
    norm = caminho.rstrip("/") or "/"
    if norm in _CAMINHOS_PUBLICOS_EXATOS:
        return True
    return caminho.startswith(_CAMINHO_STATIC_PREFIX)


class AuthenticationToken(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        caminho = request.url.path

        if _camino_publico(caminho):
            return await call_next(request)

        token = request.cookies.get("session_token")
        if token != VALOR_TOKEN_SESSAO:
            return RedirectResponse(url="/login", status_code=303)

        return await call_next(request)
