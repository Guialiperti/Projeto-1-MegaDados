-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`usuario`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`usuario` ;

CREATE TABLE IF NOT EXISTS `mydb`.`usuario` (
  `id_usuario` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(32) NOT NULL,
  `email` VARCHAR(32) NOT NULL,
  `cidade` VARCHAR(32) NOT NULL,
  PRIMARY KEY (`id_usuario`),
  UNIQUE INDEX `id_UNIQUE` (`id_usuario` ASC) VISIBLE);


-- -----------------------------------------------------
-- Table `mydb`.`post`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`post` ;

CREATE TABLE IF NOT EXISTS `mydb`.`post` (
  `id_post` INT NOT NULL AUTO_INCREMENT,
  `titulo` VARCHAR(32) NOT NULL,
  `texto` VARCHAR(32) NULL,
  `url` VARCHAR(32) NULL,
  `visivel` TINYINT NOT NULL,
  `id_usuario_post` INT NULL,
  PRIMARY KEY (`id_post`),
  UNIQUE INDEX `id_UNIQUE` (`id_post` ASC) VISIBLE,
  CONSTRAINT `id_usuario_post`
    FOREIGN KEY ()
    REFERENCES `mydb`.`usuario` ()
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `mydb`.`passaro`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`passaro` ;

CREATE TABLE IF NOT EXISTS `mydb`.`passaro` (
  `especie` VARCHAR(32) NOT NULL,
  PRIMARY KEY (`especie`),
  UNIQUE INDEX `id_UNIQUE` (`especie` ASC) VISIBLE);


-- -----------------------------------------------------
-- Table `mydb`.`usuario_prefere_passaro`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`usuario_prefere_passaro` ;

CREATE TABLE IF NOT EXISTS `mydb`.`usuario_prefere_passaro` (
  `especie_passaro` VARCHAR(32) NOT NULL,
  `id_usuario` INT NOT NULL,
  PRIMARY KEY (`especie_passaro`, `id_usuario`),
  INDEX `id_usuario_idx` (`id_usuario` ASC) VISIBLE,
  CONSTRAINT `id_usuario`
    FOREIGN KEY (`id_usuario`)
    REFERENCES `mydb`.`usuario` (`id_usuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `especie_passaro`
    FOREIGN KEY (`especie_passaro`)
    REFERENCES `mydb`.`passaro` (`especie`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `mydb`.`usuario_ve_post`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`usuario_ve_post` ;

CREATE TABLE IF NOT EXISTS `mydb`.`usuario_ve_post` (
  `id_usuario` INT NOT NULL,
  `id_post` INT NOT NULL,
  `browser` VARCHAR(32) NOT NULL,
  `momento_visto` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `aparelho` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id_usuario`, `id_post`),
  CONSTRAINT `id_usuario`
    FOREIGN KEY ()
    REFERENCES `mydb`.`usuario` ()
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `id_post`
    FOREIGN KEY ()
    REFERENCES `mydb`.`post` ()
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `mydb`.`post_menciona_usuario`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`post_menciona_usuario` ;

CREATE TABLE IF NOT EXISTS `mydb`.`post_menciona_usuario` (
  `id_post` INT NOT NULL,
  `id_usuario` INT NOT NULL,
  `mencao` TINYINT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_post`, `id_usuario`),
  CONSTRAINT `id_post`
    FOREIGN KEY ()
    REFERENCES `mydb`.`post` ()
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `id_usuario`
    FOREIGN KEY ()
    REFERENCES `mydb`.`usuario` ()
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `mydb`.`post_menciona_passaro`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`post_menciona_passaro` ;

CREATE TABLE IF NOT EXISTS `mydb`.`post_menciona_passaro` (
  `especie_passaro` VARCHAR(32) NOT NULL,
  `id_post` INT NOT NULL,
  `mencao` TINYINT NOT NULL,
  PRIMARY KEY (`especie_passaro`, `id_post`),
  CONSTRAINT `especie_passaro`
    FOREIGN KEY ()
    REFERENCES `mydb`.`passaro` ()
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `id_post`
    FOREIGN KEY ()
    REFERENCES `mydb`.`post` ()
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

USE `mydb`;

DELIMITER $$

USE `mydb`$$
DROP TRIGGER IF EXISTS `mydb`.`post_BEFORE_UPDATE` $$
USE `mydb`$$
CREATE DEFINER = CURRENT_USER TRIGGER `mydb`.`post_BEFORE_UPDATE` BEFORE UPDATE ON `post` FOR EACH ROW
BEGIN

	IF NEW.visivel = 0 THEN
		UPDATE post_menciona_usuario
			SET mencao = 0 WHERE id_post = NEW.id_post;
        
		UPDATE post_menciona_passaro
			SET mencao = 0 WHERE id_post = NEW.id_post;
		END IF;
        
END$$


DELIMITER ;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
