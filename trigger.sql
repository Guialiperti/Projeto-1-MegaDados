DELIMITER $$

USE REDE $$
DROP TRIGGER IF EXISTS REDE .`post_BEFORE_UPDATE` $$
USE REDE $$
CREATE DEFINER = CURRENT_USER TRIGGER REDE.`post_BEFORE_UPDATE` BEFORE UPDATE ON posts FOR EACH ROW
BEGIN

	IF NEW.visivel = 0 THEN
		UPDATE post_menciona_usuario
			SET mencao = 0 WHERE id_post = NEW.id_post;
        
		UPDATE post_menciona_passaro
			SET mencao = 0 WHERE id_post = NEW.id_post;
		END IF;
        
END$$


DELIMITER ;