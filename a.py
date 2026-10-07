from sqlalchemy import create_engine, String, Text, Integer, ForeignKey, select, delete
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship
from typing import Optional, List
from dotenv import load_dotenv
import os, pymysql
import time, re


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
                try:
                    nome, localidade, fundacao = input('Nome,Localidade,Fundacao: ').split(',')
                    emp = Empresa(nome = nome.capitalize(), localidade = localidade.capitalize(), fundacao = fundacao)
                    session.add(emp)
                    session.commit()
                    print('Empresa adicionada')
                    break
                except ValueError:
                    print('Digite novamente')
                    time.sleep(0.5)
            elif escolha == 'Console':
                try:
                    nome, ano, geracao, empresa = input('Nome,Ano,Geracao,Empresa: ').split(',')
                    con = Console(nome = nome.capitalize(), ano = ano.capitalize(), geracao = geracao)
                    query = select(Empresa).filter_by(nome=empresa)
                    empr = session.execute(query).scalar_one_or_none()

                    if empr:
                        con.empresa = empr
                        session.add(con)
                        session.commit()
                        print('Console adicionado')
                    else:
                        print('Empresa inexistente')
                    break
                except ValueError:
                    print('Digite novamente')
                    time.sleep(0.5)
def excluir():                   
    while True:
        with Session(engine) as session:
            print('Empresa || Console')
            escolha = input().capitalize().strip()
            if escolha == 'Empresa':
                try:
                    nome = input('Nome: ').strip().capitalize()
                    query = delete(Empresa).where(Empresa.nome == nome)
                    session.execute(query)
                    session.commit()
                    print('Empresa removida')
                    break
                except:
                    print('Empresa associada a um console, remova o console primeiro')
                    time.sleep(0.5)
            elif escolha == 'Console':
                nome = input('Nome: ').strip().capitalize()
                query = delete(Console).where(Console.nome == nome)
                session.execute(query)
                session.commit()
                print('Console removido')
                break

def listar():
    while True:
        with Session(engine) as session:
            query = select(Empresa, Console).join(Console, Empresa.id == Console.empresa_id).order_by(Empresa.id)
            lista = session.execute(query).all()
            for emp, con in lista:
                print(f"Empresa: {emp.nome}, Localidade: {emp.localidade}, Fundação: {emp.fundacao}")
                print(f" Console: {con.nome}, Ano: {con.ano}, Geração: {con.geracao}ª")
            break

engine = alter_engine()
Base.metadata.create_all(engine)

while True:
    print('Inserir || Listar || Excluir || Database')
    escolha = input().capitalize().strip()
    if escolha == 'Inserir':
        inserir()
    elif escolha == 'Listar':
        listar()
    elif escolha == 'Excluir':
        excluir()
    elif escolha == 'Database':
        engine = alter_engine()
        Base.metadata.create_all(engine)
