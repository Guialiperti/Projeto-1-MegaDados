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
            database='REDE'
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

        id_usuario = acha_usuario(conn, nome)
        remove_usuario(conn, id_usuario)

        id_usuario = acha_usuario(conn, nome)
        self.assertIsNone(id_usuario)

    def test_adiciona_preferencia(self):
        conn = self.__class__.connection

        nome = 'Guilherme Aliperti'
        email = 'gui.aliperti9@gmail.com'
        cidade = 'Sao Paulo'
        especie_passaro = 'pombo'

        adiciona_usuario(conn, nome, email, cidade)

        adiciona_passaro(conn, especie_passaro)
        id_usuario = acha_usuario(conn, nome)
        cria_preferencia(conn, id_usuario, especie_passaro)

    def test_adiciona_post(self):
        conn = self.__class__.connection
        
        id_post = '1'
        titulo = 'Passaromaniaco'
        texto = 'Bla bla bla passaros sao legais'
        nome = 'Guilherme Aliperti'
        ip = '44.2.45'
        email = 'guirin@gmail.com'
        cidade = 'SP'
        url = 'https://insper.edu.br'
        visivel = '1'
        
        adiciona_usuario(conn, nome, email, cidade)
        id_usuario = acha_usuario(conn, nome)
        adiciona_post(conn, titulo, texto, url, visivel, id_usuario)

        id_post = acha_post_ativo(conn, titulo)
        self.assertIsNotNone(id_post)

        id = acha_post_ativo(conn, 123)
        self.assertIsNone(id)

    def test_remove_post(self):
        conn = self.__class__.connection

        usuario = 'Guilherme Aliperti'
        usuario_marcado = 'Nicolas Stegmann'
        email_usuario = 'gg@gmail.com'
        usuario_vizualizacao = 'Gabriel Moura'
        url = 'https://insper.edu.br'
        aparelho = 'android'
        browser = 'firefox'
        id_post = '1'
        titulo = 'Passaromaniaco'
        texto = 'Bla bla bla passaros sao legais'
        visivel = '1'
        ip = '1.2.3.4'
        cidade = 'Sao Paulo'
        especie_passaro = 'pombo'

        id_usuario = acha_usuario(conn, usuario)
        adiciona_post(conn, titulo, texto, url, visivel, id_usuario)

        id_post = acha_post_ativo(conn, titulo)
        self.assertIsNotNone(id_post)

        adiciona_passaro(conn, especie_passaro)
        menciona_passaro(conn, id_post, especie_passaro)

        adiciona_usuario(conn, usuario_marcado, email_usuario, cidade)
        id_usuario = acha_usuario(conn, usuario_marcado)
        marca_usuario(conn, id_post, id_usuario)

        adiciona_usuario(conn, usuario_vizualizacao, email_usuario, cidade)
        id_usuario = acha_usuario(conn, usuario_vizualizacao)
        usuario_ve_post(conn, id_usuario, id_post,
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
        ip = '10.2.3'
        email = 'guirin@gmail.com'
        cidade = 'SP'
        titulo = 'Passaromaniaco'
        texto = 'Bla bla bla passaros sao legais'
        
        adiciona_usuario(conn, nome, email, cidade)
        id_usuario = acha_usuario(conn, nome)
        adiciona_post(conn, titulo, texto, url, visivel, id_usuario)

        id_post = acha_post_ativo(conn, titulo)
        self.assertIsNotNone(id_post)

        marca_usuario(conn, id_post, id_usuario)

    def teste_adiciona_reacao(self):
        conn = self.__class__.connection

        titulo = 'Passaromaniaco'
        texto = 'Bla bla bla passaros sao legais'
        nome = 'Guilherme Aliperti'
        url = 'https://insper.edu.br'
        visivel = '1'
        ip = '10.2.3'
        email = 'guirin@gmail.com'
        cidade = 'SP'
        titulo = 'Passaromaniaco'
        texto = 'Bla bla bla passaros sao legais'

        adiciona_usuario(conn, nome, email, cidade)
        id_usuario = acha_usuario(conn, nome)
        adiciona_post(conn, titulo, texto, url, visivel, id_usuario)
        id_post = acha_post(conn, titulo)

        adiciona_reacao(conn, id_usuario, id_post, 'joinha')

        reacao = acha_reacao_post(conn, id_usuario, id_post)
        self.assertIsNotNone(reacao)

    def teste_altera_reacao(self):
        conn = self.__class__.connection

        titulo = 'Passaromaniaco'
        texto = 'Bla bla bla passaros sao legais'
        nome = 'Guilherme Aliperti'
        url = 'https://insper.edu.br'
        visivel = '1'
        ip = '10.2.3'
        email = 'guirin@gmail.com'
        cidade = 'SP'
        titulo = 'Passaromaniaco'
        texto = 'Bla bla bla passaros sao legais'

        adiciona_usuario(conn, nome, email, cidade)
        id_usuario = acha_usuario(conn, nome)
        adiciona_post(conn, titulo, texto, url, visivel, id_usuario)
        id_post = acha_post(conn, titulo)

        adiciona_reacao(conn, id_usuario, id_post, 'joinha')

        reacao = acha_reacao_post(conn, id_usuario, id_post)
        self.assertIsNotNone(reacao)

        atualiza_reacao(conn, id_usuario, id_post, 'Love')
        reacao = acha_reacao_post(conn, id_usuario, id_post)
        self.assertEqual('Love', reacao)

    def testa_funcao_post_cronologica_reversa(self):
        conn = self.__class__.connection

        titulo = 'Passaromaniaco'
        texto = 'Bla bla bla passaros sao legais'
        nome = 'Guilherme Aliperti'
        url = 'https://insper.edu.br'
        visivel = '1'
        ip = '10.2.3'
        email = 'guirin@gmail.com'
        cidade = 'SP'
        titulo2 = 'depois'
        titulo = 'Passaromaniaco'
        texto = 'Bla bla bla passaros sao legais'

        adiciona_usuario(conn, nome, email, cidade)
        id_usuario = acha_usuario(conn, nome)
        adiciona_post(conn, titulo, texto, url, visivel, id_usuario)
        id_post1 = acha_post(conn, titulo)

        adiciona_post(conn, titulo2, texto, url, visivel, id_usuario)
        id_buscado = posts_usuario_ordem_cronologica_reversa(conn, id_usuario)
        self.assertEqual(id_post1, id_buscado)
        
    def testa_usuario_popular(self):
        conn = self.__class__.connection

        titulo = 'Passaromaniaco'
        texto = 'Bla bla bla passaros sao legais'
        nome = 'Guilherme Aliperti'
        nome2 = 'Nicolas Stegmann'
        url = 'https://insper.edu.br'
        visivel = '1'
        ip = '10.2.3'
        email = 'guirin@gmail.com'
        cidade = 'SP'
        titulo2 = 'depois'
        titulo = 'Passaromaniaco'
        texto = 'Bla bla bla passaros sao legais'

        adiciona_usuario(conn, nome, email, cidade)
        id_usuario = acha_usuario(conn, nome)

        adiciona_usuario(conn, nome2, email, cidade)
        id_usuario2 = acha_usuario(conn, nome2)

        adiciona_post(conn, titulo, texto, url, visivel, id_usuario)
        id_post = acha_post(conn, titulo)
        marca_usuario(conn, id_post, id_usuario2)

        pop = usuarios_mais_populares(conn, cidade)
        self.assertEqual(nome2, pop)




        


def run_sql_script(filename):
    global config
    with open(filename, 'rb') as f:
        subprocess.run(
            [
                config['MYSQL'], 
                '-u', config['USER'], 
                '-p' + config['PASS'], 
                '-h', config['HOST']
            ], 
            stdin=f
        )

def setUpModule():
    filenames = [entry for entry in os.listdir() 
        if os.path.isfile(entry) and re.match(r'.*_\d{3}\.sql', entry)]
    for filename in filenames:
        run_sql_script(filename)

def tearDownModule():
    run_sql_script('deltaScriptEntrega2.sql')
    run_sql_script('trigger.sql')
    run_sql_script('store_procedures.sql')

if __name__ == '__main__':
    global config
    with open('config_tests.json', 'r') as f:
        config = json.load(f)
    logging.basicConfig(filename=config['LOGFILE'], level=logging.DEBUG)
    unittest.main(verbosity=2)
