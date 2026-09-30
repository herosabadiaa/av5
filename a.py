from sqlalchemy import create_engine, String, Text, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship
from typing import Optional, List
from dotenv import load_dotenv
import os, pymysql

class Base(DeclarativeBase):
    pass

class Empresa(Base):
    __tablename__ = "empresa"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(250))
    localidade: Mapped[str] = mapped_column(String(250))
    fundacao: Mapped[Optional[str]] = mapped_column(String(250), nullable=True)
    consoles: Mapped[List["Console"]] = relationship(back_populates="empresa")



class Console(Base):
    __tablename__ = "console"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(250))
    ano: Mapped[str] = mapped_column(String(250))
    geracao: Mapped[Optional[str]] = mapped_column(String(250), nullable=True)
    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresa.id"))
    empresa: Mapped["Empresa"] = relationship(back_populates="consoles")    


def alter_engine():
    while True: 
        print('Sqlite || Mysql')
        alter = input().strip().capitalize()    
        if alter == 'Sqlite':   
            engine = create_engine("sqlite:///Companhia.db")
            return engine

        elif alter == 'Mysql':
            load_dotenv()
            MYSQL_USER = os.getenv("MYSQL_USER")
            MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
            MYSQL_HOST = os.getenv("MYSQL_HOST")
            MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
            MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
            
            connection = pymysql.connect(host = MYSQL_HOST, user = MYSQL_USER, password = MYSQL_PASSWORD, port = MYSQL_PORT)
            try:
                with connection.cursor() as cursor:
                    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DATABASE};")
            finally:
                connection.close()

            engine = create_engine(f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}")
            return engine

def inserir():
    while True:
        with Session(engine) as session:
            print('Empresa || Console')
            escolha = input().capitalize().strip()
            if escolha == 'Empresa':
                nome, localidade, fundacao = input('Nome,Localidade,Fundacao: ').split(',')
                emp = Empresa(nome, localidade, fundacao)
                session.add(emp)
                session.commit()
            elif escolha == 'Console':
                nome, ano, geracao, empresa = input('Nome,Ano,Geracao,Empresa: ').split(',')
                con = Console(nome, ano, geracao)
 

                con.empresa = empresa
                session.add(con)
                session.commit()

engine = alter_engine()
Base.metadata.create_all(engine)

while True:
    print('Inserir || Listar || Excluir || Database')
    escolha = input().capitalize().strip()

    if escolha == 'Inserir':
        print('inserir')
    elif escolha == 'Listar':
        print('listar')
    elif escolha == 'Excluir':
        print('excluir')
    elif escolha == 'Database':
        alter_engine()