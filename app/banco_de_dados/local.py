import sqlite3
from contextlib import contextmanager


class BancoLocal:
    def __init__(self, nome_arquivo="techlog.db"):
        self.nome_arquivo = nome_arquivo

    @contextmanager
    def conectar(self):
        conexao = sqlite3.connect(self.nome_arquivo)
        try:
            yield conexao
            conexao.commit()
        except Exception as e:
            conexao.rollback()
            raise e
        finally:
            conexao.close()

    def inicializar_banco(self):
        with self.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute("""
                    CREATE TABLE IF NOT EXISTS clientes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        email TEXT NOT NULL,
                        telefone TEXT NOT NULL
                    )
                """)
            cursor.execute("""
                    CREATE TABLE IF NOT EXISTS usuarios (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        email TEXT NOT NULL UNIQUE,
                        senha TEXT NOT NULL
                    )
                """)

            print("Banco de dados inicializado!")
