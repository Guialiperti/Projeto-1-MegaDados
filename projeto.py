import pymysql

#Funcoes tabela USUARIOS

def adiciona_usuario(conn, nome, email, cidade):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO usuarios (nome, email, cidade) VALUES (%s, %s, %s)', (nome, email, cidade))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir {nome} na tabela usuario')

def acha_usuario(conn, nome):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_usuario FROM usuarios WHERE nome = %s', (nome))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

def muda_nome_usuario(conn, nome, novo_nome):
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE usuarios SET nome=%s where nome=%s', (novo_nome, nome))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso alterar nome do usuario com id: {nome} para {novo_nome} na tabela usuario')

def remove_usuario(conn, id_usuario):
    with conn.cursor() as cursor:
        try:
            cursor.execute('DELETE FROM usuarios WHERE id_usuario=%s', (id_usuario))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso remover o usuario: {id_usuario}')

def lista_usuarios(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT nome from usuarios')
        res = cursor.fetchall()
        usuarios = tuple(x[0] for x in res)
        return usuarios

#Funcoes tabela POST

def adiciona_post(conn, titulo, texto, url, visivel, id_usuario):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO posts (titulo, texto, url, visivel, id_usuario) VALUES (%s, %s, %s, %s, %s)', (titulo, texto, url, visivel, id_usuario))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir o post com titulo: {titulo} na tabela post')

def acha_post(conn, titulo):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_post FROM posts WHERE titulo = %s', (titulo))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

def acha_post_ativo(conn, titulo):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_post FROM posts WHERE titulo = %s AND visivel = 1', (titulo))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

def remove_post(conn, id_post):
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE posts SET visivel=0 where id_post=%s', (id_post))
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


#Funcao da tabela Joinha

def adiciona_reacao(conn, id_usuario, id_post, reacao):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO JoinhaPost (id_usuario, id_post, reacao) VALUES (%s, %s, %s)', (id_usuario, id_post, reacao))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso reagir. usuario: {id_usuario}, post: {id_post} na tabela JoinhaPost')

def acha_reacao_post(conn, id_usuario, id_post):
	with conn.cursor() as cursor:
		cursor.execute('SELECT reacao FROM JoinhaPost WHERE id_post = %s', (id_post))
		res = cursor.fetchone()
		if res:
			return res[0]
		else:
			return None

def remove_reacao(conn, id_usuario, id_post):
	with conn.cursor() as cursor:
		try:
			cursor.execute('DELETE FROM JoinhaPost WHERE id_usuario=%s AND id_post=%s', (id_usuario, id_post))
		except pymysql.err.IntegrityError as e:
			raise ValueError(f'Não posso remover a reacao do usuario de id: {id_usuario} no post de id: {id_post} da tabela JoinhaPost')

def atualiza_reacao(conn, id_usuario, id_post, reacao):
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE JoinhaPost SET reacao=%s WHERE id_usuario=%s AND id_post=%s', (reacao, id_usuario, id_post))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso atualizar a reacao do usuario de id: {id_usuario} no post de id: {id_post} da tabela JoinhaPost')

#Funcoes da tabela passaros

def adiciona_passaro(conn, especie):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO passaros (especie) VALUES(%s)', especie)
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso adicionar passaro da especie {especie}')

#funcoes especificadas no proj

def posts_usuario_ordem_cronologica_reversa(conn, id_usuario):
	with conn.cursor() as cursor:
		try:
			cursor.execute('SELECT id_post FROM posts WHERE id_usuario=%s ORDER BY data_post DESC', (id_usuario))
			r = cursor.fetchone()
			return r[0]
		except pymysql.err.IntegrityError as e:
			raise ValueError(f'ERROR')


def usuarios_mais_populares(conn, cidade):
	with conn.cursor() as cursor:
		try:
			cursor.execute(
			"""
				SELECT
					nome, COUNT(id_usuario) AS nvezes
				FROM
					usuarios
					INNER JOIN post_menciona_usuario USING (id_usuario)
				WHERE 
				cidade=%s
				ORDER BY
					nvezes DESC
			
			""", (cidade))
			r= cursor.fetchone()
			return r[0]
		except pymysql.err.IntegrityError as e:
			raise ValueError(f'ERROR')


def usuarios_que_referenciam(conn,id_usuario):
	with conn.cursor() as cursor:
		try:
			cursor.execute(
				"""
					SELECT
						posts.id_usuario
					FROM
						posts, post_menciona_usuario
					WHERE 
						posts.id_post = post_menciona_usuario.id_post AND post_menciona_usuario.id_usuario = id_usuario
				""")
			r = cursor.fetchall()
			if len(r) == 0 :
				return None
			else:
				rr = tuple(x[0] for x in r)
				return rr
		except pymysql.err.IntegrityError as e:
			raise ValueError(f'ERROR')


def URL_passaros(conn):
	with conn.cursor() as cursor:
		try:
			cursor.execute(
				"""
					SELECT
						passaros.especie, posts.url
					FROM
						passaros, posts, post_menciona_passaro
					WHERE 
						passaros.especie = post_menciona_passaro.especie_passaro AND post_menciona_passaro.id_post = posts.id_post
				""")
			r = cursor.fetchall()
			if len(r) == 0 :
				return None
			else:
				return r
		except pymysql.err.IntegrityError as e:
			raise ValueError(f'ERROR')

def quantidade_aparelho_browser(conn):
	with conn.cursor() as cursor:
		try:
			cursor.execute(
				"""
					SELECT
						browser, aparelho , COUNT(aparelho)
					FROM
						usuario_ve_post
					GROUP BY 
						browser,aparelho
				""")
			r = cursor.fetchall()
			if len(r) == 0 :
				return None
			else:
				return r
		except pymysql.err.IntegrityError as e:
			raise ValueError(f'ERROR')
