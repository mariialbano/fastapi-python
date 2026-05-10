from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter()


@router.get("/logout")
async def sair():
    resposta = RedirectResponse(url="/login", status_code=303)
    resposta.delete_cookie(key="session_token", httponly=True)
    return resposta
