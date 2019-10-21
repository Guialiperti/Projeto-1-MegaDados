import pymysql

#Funcoes tabela USUARIOS

def adiciona_usuario(conn, nome, email, cidade):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO usuario (nome, email, cidade) VALUES (%s, %s, %s)', (nome, email, cidade))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir {nome} na tabela usuario')

def acha_usuario(conn, nome):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id FROM usuario WHERE nome = %s', (nome))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

def muda_nome_usuario(conn, nome, novo_nome):
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE usuario SET nome=%s where nome=%s', (novo_nome, nome))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso alterar nome do usuario com id: {nome} para {novo_nome} na tabela usuario')

def remove_usuario(conn, nome):
    with conn.cursor() as cursor:
        try:
            cursor.execute('DELETE usuario where nome=%s', (nome))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso remover o usuario: {nome}')

def lista_usuarios(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT nome from usuario')
        res = cursor.fetchall()
        usuarios = tuple(x[0] for x in res)
        return usuarios

#Funcoes tabela POST

def adiciona_post(conn, titulo, texto, url, visivel, ip, id_usuario):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO post (titulo, texto, url, visivel, ip, id_usuario) VALUES (%s, %s, %s, %s, %s)', (titulo, texto, url, visivel, ip, id_usuario))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir o post com titulo: {titulo} na tabela post')

def acha_post(conn, titulo):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id FROM post WHERE titulo = %s', (titulo))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

def acha_post_ativo(conn, id_post):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id FROM post WHERE id_post = %s AND visivel = 1', (id_post))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

def remove_post(conn, id_post):
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE post SET visivel=0 where id_post=%s', (id_post))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso remover o post de id: {id_post} (colocar como nao visivel)')



#Funcoes tabela usuario_ve_post
def usuario_ve_post(conn, id_usuario, id_post, aparelho, browser, ip):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO usuario_ve_post (id_usuario, id_post, aparelho, browser, ip) VALUES (%s, %s, %s, %s, %s)', (id_usuario, id_post, aparelho, browser, ip))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso adicionar a usuario_ve_post o post de id: {id_post} na tabela')


#Funcoes da tabela post_menciona_passaro

def menciona_passaro(conn, id_post, especie_passaro):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO post_menciona_passaro (id_post, especie_passaro) VALUES (%s, %s)', (id_post, especie_passaro))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso adicionar a post_menciona_passaro de nome: {especie_passaro} no post de id: {id_post} na tabela')


#Funcoes da tabela post menciona usuario
def marca_usuario(conn, id_post, id_usuario):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO post_menciona_usuario (id_post, id_usuario) VALUES (%s, %s)', (id_post, id_usuario))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso marcar o usuario de id: {id_usuario} no post de id: {id_post} na tabela post_menciona_usuario')


#Funcoes da tabela usuario_prefere_passaro

def cria_preferencia(conn, id_usuario, especie_passaro):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO usuario_prefere_passaro (id_usuario, especie_passaro) VALUES (%s, %s)', (id_usuario, especie_passaro))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso adicionar a preferencia do usuario de id: {id_usuario} ao passaro: {especie_passaro} na tabela usuario_prefere_passaro')
