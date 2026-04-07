-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema db_rotinas
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `db_rotinas` DEFAULT CHARACTER SET utf8 ;
USE `db_rotinas` ;

-- -----------------------------------------------------
-- Table `db_rotinas`.`usuario`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `db_rotinas`.`usuario` ;

CREATE TABLE IF NOT EXISTS `db_rotinas`.`usuario` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(150) NOT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `is_active` BOOLEAN NOT NULL DEFAULT TRUE,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `db_rotinas`.`rotina`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `db_rotinas`.`rotina` ;

CREATE TABLE IF NOT EXISTS `db_rotinas`.`rotina` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(60) NOT NULL,
  `startTime` DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
  `deadLine` DATETIME NOT NULL,
  `description` VARCHAR(255) NULL,
  `is_active` TINYINT(1) NOT NULL DEFAULT 1,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_rotina_usuario_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_rotina_usuario`
    FOREIGN KEY (`user_id`)
    REFERENCES `db_rotinas`.`usuario` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `db_rotinas`.`execucoes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `db_rotinas`.`execucoes` ;

CREATE TABLE IF NOT EXISTS `db_rotinas`.`execucoes` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `date` DATE NOT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  `rotina_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `uk_rotina_date_idx` (`rotina_id` ASC, `date` ASC) VISIBLE,
  INDEX `fk_execucoes_rotina1_idx` (`rotina_id` ASC) VISIBLE,
  CONSTRAINT `fk_execucoes_rotina1`
    FOREIGN KEY (`rotina_id`)
    REFERENCES `db_rotinas`.`rotina` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `db_rotinas`.`historico_acoes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `db_rotinas`.`historico_acoes` ;

CREATE TABLE IF NOT EXISTS `db_rotinas`.`historico_acoes` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `actionsType` ENUM('CREATE', 'UPDATE', 'DELETE') NOT NULL,
  `description` VARCHAR(255) NOT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  `user_id` INT NOT NULL,
  `rotina_id` INT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_historico_acoes_usuario1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_historico_acoes_rotina1_idx` (`rotina_id` ASC) VISIBLE,
  CONSTRAINT `fk_historico_acoes_usuario1`
    FOREIGN KEY (`user_id`)
    REFERENCES `db_rotinas`.`usuario` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_historico_acoes_rotina1`
    FOREIGN KEY (`rotina_id`)
    REFERENCES `db_rotinas`.`rotina` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

-- ADMIN
insert into db_rotinas.usuario(`name`)
value('admin');