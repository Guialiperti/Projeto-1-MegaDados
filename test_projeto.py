import io
import json
import logging
import os
import os.path
import re
import subprocess
import unittest
import pymysql

from projeto import *

class TestProjeto(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global config
        cls.connection = pymysql.connect(
            host=config['HOST'],
            user=config['USER'],
            password=config['PASS'],
            database='mydb'
        )
    @classmethod
    def tearDownClass(cls):
        cls.connection.close()

    def setUp(self):
        conn = self.__class__.connection
        with conn.cursor() as cursor:
            cursor.execute('START TRANSACTION')

    def tearDown(self):
        conn = self.__class__.connection
        with conn.cursor() as cursor:
            cursor.execute('ROLLBACK')

    def test_meu_teste(self):
        print(" \n-Teste 0")
        print("Isso deve funcionar")
        pass

    def test_adiciona_usuario(self):
        conn = self.__class__.connection

        nome = 'Guilherme Aliperti'
        email = 'gui.aliperti9@gmail.com'
        cidade = 'Sao Paulo'

        # Adiciona um usuario não existente.
        adiciona_usuario(conn, nome, email, cidade)

        # Tenta adicionar o mesmo usuario duas vezes.
        try:
            adiciona_usuario(conn, nome, email, cidade)
            self.fail('Nao deveria ter adicionado o mesmo usuario duas vezes.')
        except ValueError as e:
            pass

        # Checa se o usuario existe.
        id = acha_usuario(conn, nome)
        self.assertIsNotNone(id)

        # Tenta achar um usuario inexistente.
        id = acha_usuario(conn, "Cristiano Ronaldo")
        self.assertIsNone(id)

    def test_remove_usuario(self):
        conn = self.__class__.connection

        nome = 'Guilherme Aliperti'
        email = 'gui.aliperti9@gmail.com'
        cidade = 'Sao Paulo'

        adiciona_usuario(conn, nome, email, cidade)
        id = acha_usuario(conn, nome)

        res = lista_usuarios(conn)
        self.assertCountEqual(res, (id,))

        remove_usuario(conn, nome)

        res = lista_usuarios(conn)
        self.assertFalse(res)

    def test_adiciona_preferencia(self):
        conn = self.__class__.connection

        nome = 'Guilherme Aliperti'
        email = 'gui.aliperti9@gmail.com'
        cidade = "Sao Paulo"
        especie_passaro = 'pombo'

        adiciona_usuario(conn, nome, email, cidade)

        cria_preferencia(conn, email, especie_passaro)

    def test_adiciona_post(self):
        conn = self.__class__.connection
        
        id_post = '1'
        titulo = 'Passaromaniaco'
        texto = 'Bla bla bla passaros sao legais'
        nome = 'Guilherme Aliperti'
        url = 'https://insper.edu.br'
        visivel = '1'

        id_usuario = acha_usuario(conn, nome)
        adiciona_post(conn, titulo, texto, url, visivel, id_usuario)

        id_post = acha_post_ativo(conn, id_post)
        self.assertIsNotNone(id_post)

        id = acha_post_ativo(conn, 123)
        self.assertIsNone(id)

    def test_remove_post(self):
        conn = self.__class__.connection

        usuario = 'Guilherme Aliperti'
        usuario_marcado = 'Nicolas Stegmann'
        usuario_vizualizacao = 'Gabriel Moura'
        url = 'https://insper.edu.br'
        aparelho = 'android'
        browser = 'firefox'
        ip = '200.108.175.255'
        id_post = '1'
        titulo = 'Passaromaniaco'
        texto = 'Bla bla bla passaros sao legais'
        url = 'https://insper.edu.br'
        visivel = '1'
        especie_passaro = 'pombo'

        id_usuario = acha_usuario(conn, usuario)
        adiciona_post(conn, titulo, texto, url, visivel, id_usuario)

        id_post = acha_post_ativo(conn, id_post)
        self.assertIsNotNone(id_post)

        menciona_passaro(conn, id_post, especie_passaro)

        marca_usuario(conn, id_post, usuario_marcado)

        usuario_ve_post(conn, usuario_vizualizacao, id_post,
                       aparelho, browser, ip)

        remove_post(conn, id_post)
        id = acha_post_ativo(conn, id_post)
        self.assertIsNone(id)

    def test_marca_usuario(self):
        conn = self.__class__.connection

        id_post = '1'
        titulo = 'Passaromaniaco'
        texto = 'Bla bla bla passaros sao legais'
        nome = 'Guilherme Aliperti'
        url = 'https://insper.edu.br'
        visivel = '1'
        titulo = 'Passaromaniaco'
        texto = 'Bla bla bla passaros sao legais'

        id_usuario = acha_usuario(conn, nome)
        adiciona_post(conn, titulo, texto, url, visivel, id_usuario)

        id_post = acha_post_ativo(conn, id_post)
        self.assertIsNotNone(id_post)

        marca_usuario(conn, id_post, id_usuario)