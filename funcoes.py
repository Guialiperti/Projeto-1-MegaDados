import pymysql

#MARCACOES
def marcacoes(texto): 
	palavras = texto.split()
	p = []
	u = []
	for word in palavras:
		if(word[0] == "#"):	
			p.append(word[1:])
		if(word[0] == "@"):   
			u.append(word[1:])
	return p,u

def marca_passaro(conn,especie_passaro,id_post):
	with conn.cursor() as cursor:
		try:
			cursor.execute('CALL marca_passaro(%s, %i)', (especie_passaro, id_post))
		except pymysql.err.IntegrityError as e:
			raise ValueError(f'Não posso marcar o passaro de nome: {especie_passaro} no post de id: {id_post}')


def marca_usuario(conn, nome_usuario, id_post):
	with conn.cursor() as cursor:
		try:
			cursor.execute('CALL marca_usuario(%s, %i)', (nome_usuario, id_post))
		except pymysql.err.IntegrityError as e:
			raise ValueError(f'Não posso adicionar marcar o usuario de nome: {nome_usuario} no post de id: {id_post}')

#POSTS
def adiciona_post(conn, titulo, texto, url, visivel, id_usuario):
	p,u = marcacoes(texto)
	with conn.cursor() as cursor:
		try:
			cursor.execute('INSERT INTO post (titulo, texto, url, visivel, id_usuario) VALUES (%s, %s, %s, %i)', (titulo, texto, url, visivel, id_usuario))
			cursor.execute('SELECT id_post FROM posts WHERE id_post = LAST_INSERT_ID() LIMIT 1')
			r = cursor.fetchone()
			for i in p:
				marca_passaro(conn,i,r[0])
			for i in u:
				marca_usuario(conn, i,r[0])
		except pymysql.err.IntegrityError as e:
			raise ValueError(f'Não posso inserir o post com titulo: {titulo} na tabela posts')

def remove_post(conn, id_post):
	with conn.cursor() as cursor:
		try:
			cursor.execute('UPDATE posts SET visivel = 0 WHERE post_id=%s', (id_post))
		except pymysql.err.IntegrityError as e:
			raise ValueError(f'Não posso remover o post da tabela post')


def posts_usuario_ordem_cronologica_reversa(conn, id_usuario):
	with conn.cursor() as cursor:
		try:
			cursor.execute('SELECT texto FROM posts WHERE id_usuario=%s ORDER BY data_post DESC', (id_usuario))
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
					usuarios, COUNT(id_usuario) AS nvezes
				FROM
					usuarios
					INNER JOIN post_menciona_usuario USING (id_usuario)
				WHERE 
				cidade=%s
				ORDER BY
					nvezes DESC
				LIMIT by 5
			
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
						passaro.especie, post.Url
					FROM
						passaro, posts, post_menciona_passaro
					WHERE 
						passaro.especie = post_menciona_passaro.especie_passaro AND post_menciona_passaro.id_post = posts.id_post
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
						browser, aparelho
					FROM
						posts
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

def adiciona_reacao(conn, id_usuario, id_post, reacao):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO JoinhaPost (id_usuario, id_post, reacao) VALUES (%i, %i, %s)', (id_usuario, id_post, reacao))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso reagir. usuario: {id_usuario}, post: {id_post} na tabela JoinhaPost')

def acha_reacao_post(conn, id_usuario, id_post):
	with conn.cursor() as cursor:
		cursor.execute('SELECT reacao FROM JoinhaPost WHERE id_post = %i', (id_post))
		res = cursor.fetchone()
		if res:
			return res[0]
		else:
			return None

def remove_reacao(conn, id_usuario, id_post):
	with conn.cursor() as cursor:
		try:
			cursor.execute('DELETE FROM JoinhaPost WHERE id_usuario=%i AND id_post=%i', (id_usuario, id_post))
		except pymysql.err.IntegrityError as e:
			raise ValueError(f'Não posso remover a reacao do usuario de id: {id_usuario} no post de id: {id_post} da tabela JoinhaPost')

def atualiza_reacao(conn, id_usuario, id_post, reacao):
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE JoinhaPost SET reacao=%s WHERE id_usuario=%i AND id_post=%i', (reacao, id_usuario, id_post))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso atualizar a reacao do usuario de id: {id_usuario} no post de id: {id_post} da tabela JoinhaPost')