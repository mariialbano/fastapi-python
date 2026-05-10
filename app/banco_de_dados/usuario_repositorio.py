from app.banco_de_dados.local import BancoLocal
from app.modelos.usuario import Usuario, UsuarioCriarAtualizar


class UsuarioRepositorio:
    def __init__(self, banco_de_dados: BancoLocal):
        self.db = banco_de_dados

    async def buscar_usuario_email_senha(
        self, email: str, senha: str
    ) -> Usuario | None:
        with self.db.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                """SELECT id, nome, email FROM usuarios
                   WHERE lower(email) = lower(?) AND senha = ?""",
                (email.strip(), senha),
            )
            linha = cursor.fetchone()
            if linha:
                return Usuario(id_=linha[0], nome=linha[1], email=linha[2], senha=senha)
            return None

    async def existe_email(self, email: str) -> bool:
        with self.db.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                "SELECT 1 FROM usuarios WHERE lower(email) = lower(?)",
                (email.strip(),),
            )
            return cursor.fetchone() is not None

    async def criar_usuario(self, dados: UsuarioCriarAtualizar) -> Usuario:
        nome_limpo = dados.nome.strip()
        email_limpo = dados.email.strip().lower()
        senha_valor = dados.senha or ""
        with self.db.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
                (nome_limpo, email_limpo, senha_valor),
            )
            usuario_id = cursor.lastrowid
            return Usuario(
                id_=usuario_id,
                nome=nome_limpo,
                email=email_limpo,
                senha=senha_valor,
            )
