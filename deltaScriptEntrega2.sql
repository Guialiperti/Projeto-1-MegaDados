USE REDE;

DROP TABLE IF EXISTS JoinhaPost;
CREATE TABLE JoinhaPost(
id_usuario int NOT NULL,
id_post int NOT NULL,
tipoReacao VARCHAR(30),
  PRIMARY KEY (id_usuario,id_post),
  FOREIGN KEY (id_usuario)
    REFERENCES usuarios(id_usuario),
  FOREIGN KEY (id_post)
    REFERENCES post (id_post)
);