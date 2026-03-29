from fastapi import FastAPI
from fastapi.responses import HTMLResponse # Importação para retornar HTML como response
from app.rotas import cliente

app = FastAPI(
    title="Techlog Solutions API (Alura)",
    description="CRM para Techlog Solutions",
    version="0.0.1",
)

app.include_router(cliente.router)

@app.get("/")
async def health_check():
    return {"status":"ok"}

@app.get("/front", response_class=HTMLResponse)
async def frontend():
    return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>
        </head>
        <body>
            <h1>Techlog Solutions</h1>
        </body>
        </html>
    """