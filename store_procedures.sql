
DROP PROCEDURE IF EXISTS marca_passaro;
DROP PROCEDURE IF EXISTS marca_usuario;

DELIMITER //
CREATE PROCEDURE marca_usuario(IN nome_usuario VARCHAR(32), IN post INT)
BEGIN
	IF EXISTS (SELECT id_usuario FROM usuarios WHERE nome = nome_usuario) THEN
		INSERT INTO post_menciona_usuario (id_post, id_usuario) VALUES (id_post, id_usuario);
    END IF;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE marca_passaro(IN especie_passaro VARCHAR(32), IN post INT)
BEGIN
	IF EXISTS (SELECT especie FROM passaros WHERE especie = especie_passaro) THEN
		INSERT INTO post_menciona_passaro (especie_passaro, id_post) VALUES (especie_passaro, id_post);
    END IF;
END//
DELIMITER ;