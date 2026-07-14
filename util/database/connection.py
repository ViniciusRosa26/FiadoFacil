import os
import sys
import sqlite3


def obter_pasta_base():
    """
    Quando rodando como .exe empacotado (PyInstaller), sys.frozen existe
    e sys.executable aponta pro próprio .exe — usamos a pasta dele.
    Quando rodando como script normal (python main.py), usamos a pasta
    do projeto normalmente.
    """
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


DATABASE = os.path.join(obter_pasta_base(), "fiado.db")


def get_connection():
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
    return sqlite3.connect(DATABASE)