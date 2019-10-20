DROP DATABASE IF EXISTS REDE;
CREATE DATABASE REDE;
USE REDE;

DROP TABLE IF EXISTS usuarios ;
CREATE TABLE usuarios (
  id_usuario INT NOT NULL AUTO_INCREMENT,
  nome VARCHAR(32) NOT NULL,
  email VARCHAR(32) NOT NULL,
  cidade VARCHAR(32) NOT NULL,
  PRIMARY KEY (id_usuario)
);


DROP TABLE IF EXISTS posts ;
CREATE TABLE posts (
  id_post INT NOT NULL AUTO_INCREMENT,
  titulo VARCHAR(32) NOT NULL,
  texto VARCHAR(32) NOT NULL,
  url VARCHAR(32) NOT NULL,
  visivel TINYINT NOT NULL,
  id_usuario_post INT NULL,
  PRIMARY KEY (id_post),
  FOREIGN KEY (id_usuario_post)
    REFERENCES usuarios(id_usuario)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);

DROP TABLE IF EXISTS passaros ;
CREATE TABLE passaros (
  especie VARCHAR(32) NOT NULL,
  PRIMARY KEY (especie)
);


DROP TABLE IF EXISTS usuario_prefere_passaro ;
CREATE TABLE usuario_prefere_passaro (
  especie_passaro VARCHAR(32) NOT NULL,
  id_usuario INT NOT NULL,
  PRIMARY KEY (especie_passaro,id_usuario),
  FOREIGN KEY (id_usuario)
    REFERENCES usuarios(id_usuario),
  FOREIGN KEY (especie_passaro)
    REFERENCES passaros (especie)
);



DROP TABLE IF EXISTS usuario_ve_post;
CREATE TABLE usuario_ve_post (
  id_usuario INT NOT NULL,
  id_post INT NOT NULL,
  browser VARCHAR(32) NOT NULL,
  ip VARCHAR(32) NOT NULL,
  momento_visto TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  aparelho VARCHAR(45) NOT NULL,
  PRIMARY KEY (id_usuario, id_post),
  FOREIGN KEY (id_usuario)
    REFERENCES usuarios (id_usuario),
  FOREIGN KEY (id_post)
    REFERENCES posts (id_post)
);


DROP TABLE IF EXISTS post_menciona_usuario ;

CREATE TABLE post_menciona_usuario (
  id_post INT NOT NULL,
  id_usuario INT NOT NULL,
  mencao TINYINT NOT NULL,
  PRIMARY KEY (id_post, id_usuario),
  FOREIGN KEY (id_post)
    REFERENCES posts (id_post),
  FOREIGN KEY (id_usuario)
    REFERENCES usuarios (id_usuario)
);


DROP TABLE IF EXISTS post_menciona_passaro;

CREATE TABLE post_menciona_passaro (
  especie_passaro VARCHAR(32) NOT NULL,
  id_post INT NOT NULL,
  mencao TINYINT NOT NULL,
  PRIMARY KEY (especie_passaro, id_post),
  FOREIGN KEY (especie_passaro)
    REFERENCES passaros (especie),
  FOREIGN KEY (id_post)
    REFERENCES posts (id_post)
);

