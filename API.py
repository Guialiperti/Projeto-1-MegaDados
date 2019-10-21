from fastapi import FastAPI
import uvicorn
import pymysql
from funcoes import *

connection_options = {
    'host': 'localhost',
    'user': 'megadados',
    'password': 'megadados2019',
    'database': 'rede'
}

connection = pymysql.connect(**connection_options)

app=FastAPI()

@app.post("/addpost")
def addpost(titulo: str, texto: str, url:str, id_usuario:int):
    adiciona_post(connection, titulo, texto, url)
    return{"Message":"done"}

@app.post("/removepost")
def removepost(id_post: int):
    remove_post(connection, id_post)
    return {"Message":"done"}

@app.post("/checkposts")
def checkposts(id_usuario:int):
    result = posts_usuario_ordem_cronologica_reversa(connection, id_usuario)
    return{"Users":result}

@app.post("/popularusers")
def popularusers(cidade: str):
    result = usuarios_mais_populares(connection, cidade)
    return{"Users":result}

@app.post("/referenceusers")
def refereceuser(id_usuario: int):
    result = usuarios_que_referenciam(connection, id_usuario)
    return{"Users":result}

@app.post("/url")
def urlpassaors():
    result = URL_passaros(connection)
    return{"URL":result}

@app.post("/aparelhobrowser")
def aparelhobrowser():
    result = quantidade_aparelho_browser(connection)
    return{"Aparelhos":result}

@app.post("/adicionareacao")
def addreaction(id_usuario: int, id_post: int, reacao:str):
    adiciona_reacao(connection, id_usuario, id_post, reacao)
    return{"Message":"done"}

@app.post("/removereacao")
def removereaction(id_usuario: int, id_post: int):
    remove_reacao(connection, id_usuario, id_post)
    return{"Message":"done"}

@app.post("/atualizareacao")
def updatereaction(id_usuario: int, id_post: int, reacao:str):
    atualiza_reacao(connection, id_usuario, id_post)
    return{"Message":"done"}
