-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : sam. 03 sep. 2022 à 20:49
-- Version du serveur : 5.7.36
-- Version de PHP : 7.4.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `flaskapp`
--

-- --------------------------------------------------------

--
-- Structure de la table `day_off`
--

DROP TABLE IF EXISTS `day_off`;
CREATE TABLE IF NOT EXISTS `day_off` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `start` date NOT NULL,
  `end` date NOT NULL,
  `reason` text NOT NULL,
  `id_employee` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_day_off_id_employee` (`id_employee`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `day_off`
--

INSERT INTO `day_off` (`id`, `start`, `end`, `reason`, `id_employee`) VALUES
(1, '2022-09-01', '2022-09-10', 'Mandende', 1),
(2, '2022-09-11', '2022-09-13', 'Mcaca any anaty ala', 2);

-- --------------------------------------------------------

--
-- Structure de la table `employee`
--

DROP TABLE IF EXISTS `employee`;
CREATE TABLE IF NOT EXISTS `employee` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `address` varchar(150) NOT NULL,
  `phone` varchar(30) NOT NULL,
  `hiring_day` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `password` varchar(200) NOT NULL,
  `id_status` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_employee_id_status` (`id_status`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `employee`
--

INSERT INTO `employee` (`id`, `name`, `email`, `address`, `phone`, `hiring_day`, `password`, `id_status`) VALUES
(1, 'Mionja', 'mionjaranaivoarison@gmail.com', 'Earth of the solar system', '+261 34 07 373 40', '2022-09-02 03:59:38', '$5$rounds=535000$KlEMoGcgQDs3tGEL$wCUfou4fg8AXbOILa.0y1ux9/JgPlnFfhBAJ2BGwHq6', 1),
(2, 'Mpiasa', 'employe@gmail.com', 'Address of employee ', '123456789089', '2022-09-02 04:08:11', '$5$rounds=535000$8aQqfBj8ur0guxif$CLqus7jSx7FYYoEYYoGjUfs/uLEURtZtuXbeO3XuAl0', 2);

-- --------------------------------------------------------

--
-- Structure de la table `notifications`
--

DROP TABLE IF EXISTS `notifications`;
CREATE TABLE IF NOT EXISTS `notifications` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `email` varchar(100) NOT NULL,
  `subject` varchar(200) NOT NULL,
  `message` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `notifications`
--

INSERT INTO `notifications` (`id`, `name`, `email`, `subject`, `message`) VALUES
(1, 'Mionja', 'mionjaranaivoarison@gmail.com', 'Noana ', 'NOANA LOATRA AHO E'),
(2, 'test', 'test@gmail.com', 'test', 'This is a teeeest'),
(3, 'Python', 'python@gmail.com', 'Start', 'print(\"hello world\")');

-- --------------------------------------------------------

--
-- Structure de la table `status`
--

DROP TABLE IF EXISTS `status`;
CREATE TABLE IF NOT EXISTS `status` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `salary` int(11) NOT NULL,
  `day_off` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `status`
--

INSERT INTO `status` (`id`, `name`, `salary`, `day_off`) VALUES
(1, 'CEO', 456, 5),
(2, 'Normal employee', 123, 2);

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `day_off`
--
ALTER TABLE `day_off`
  ADD CONSTRAINT `fk_day_off_id_employee` FOREIGN KEY (`id_employee`) REFERENCES `employee` (`id`);

--
-- Contraintes pour la table `employee`
--
ALTER TABLE `employee`
  ADD CONSTRAINT `fk_employee_id_status` FOREIGN KEY (`id_status`) REFERENCES `status` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
