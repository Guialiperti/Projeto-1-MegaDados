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
			cursor.execute('CALL marca_passaro(%s, %s)', (especie_passaro, id_post))
		except pymysql.err.IntegrityError as e:
			raise ValueError(f'Não posso adicionar a tag do passaro de nome: {nome_passaro} no post de id: {post_id} na tabela passaro_tag')


def marca_usuario(conn, nome_usuario, id_post):
	with conn.cursor() as cursor:
		try:
			cursor.execute('CALL marca_usuario(%s, %s)', (nome_usuario, id_post))
		except pymysql.err.IntegrityError as e:
			raise ValueError(f'Não posso adicionar a tag do usuario de email: {email} no post de id: {post_id} na tabela usuario_tag')

#POSTS
def adiciona_post(conn, titulo, texto, url, visivel, id_usuario):
	p,u = marcacoes(texto)
	with conn.cursor() as cursor:
		try:
			cursor.execute('INSERT INTO post (titulo, texto, url, visivel, id_usuario) VALUES (%s, %s, %s, %s)', (titulo, texto, url, visivel, id_usuario))
			cursor.execute('SELECT id_post FROM posts WHERE id_post = LAST_INSERT_ID() LIMIT 1')
			r = cursor.fetchone()
			for i in p:
				marca_passaro(conn,i,r[0])
			for i in u:
				marca_usuario(conn, i,r[0])
		except pymysql.err.IntegrityError as e:
			raise ValueError(f'Não posso inserir o post com titulo: {titulo} na tabela post')

def remove_post(conn, id_post):
	with conn.cursor() as cursor:
		try:
			cursor.execute('UPDATE posts SET visivel = 0 WHERE post_id=%s', (id_post))
		except pymysql.err.IntegrityError as e:
			raise ValueError(f'Não posso inserir o post com titulo: {titulo} na tabela post')


def posts_usuario_ordem_cronologica_reversa(conn, id_usuario):
	with conn.cursor() as cursor:
		try:
			cursor.execute(
			"""
				SELECT
					texto
				FROM
					posts
				WHERE
					id_usuario=%s
				ORDER BY 
					data_post ASC 
				LIMIT by 5
			""", (id_usuario))
			r = cursor.fetchone()
			return r[0]
		except pymysql.err.IntegrityError as e:
			raise ValueError(f'Não posso inserir o post com titulo: {titulo} na tabela post')


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
			raise ValueError(f'Não posso inserir o post com titulo: {titulo} na tabela post')


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
						posts.id_post = post_menciona_usuario.id_post AND post_menciona_usuario.id_usuario = id_usuario;
				""",)
			r = cursor.fetchall()
			if len(r) == 0 :
				return None
			else:
				rr = tuple(x[0] for x in r)
				return rr
		except pymysql.err.IntegrityError as e:
			raise ValueError(f'Não posso inserir o post com titulo: {titulo} na tabela post')


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
						passaro.especie = post_menciona_passaro.especie_passaro AND post_menciona_passaro.id_post = posts.id_post;
				""",)
			r = cursor.fetchall()
			if len(r) == 0 :
				return None
			else:
				return r
		except pymysql.err.IntegrityError as e:
			raise ValueError(f'Não posso inserir o post com titulo: {titulo} na tabela post')

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
						browser,aparelho;
				""",)
			r = cursor.fetchall()
			if len(r) == 0 :
				return None
			else:
				return r
		except pymysql.err.IntegrityError as e:
			raise ValueError(f'Não posso inserir o post com titulo: {titulo} na tabela post')
