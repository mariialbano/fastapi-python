from app.banco_de_dados.local import BancoLocal
from app.modelos.usuario import Usuario


class UsuarioRepositorio:
    def __init__(self, banco_de_dados: BancoLocal):
        self.db = banco_de_dados

    async def buscar_usuario_email_senha(
        self, email: str, senha: str
    ) -> Usuario | None:
        with self.db.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                "SELECT id, nome, email FROM usuarios WHERE email = ? AND senha = ?",
                (email, senha),
            )
            linha = cursor.fetchone()
            if linha:
                return Usuario(
                    id_=linha[0], nome=linha[1], email=linha[2], senha=linha[3]
                )
            return None
