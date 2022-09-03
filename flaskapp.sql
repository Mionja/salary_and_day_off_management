-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : sam. 03 sep. 2022 à 05:57
-- Version du serveur : 10.4.24-MariaDB
-- Version de PHP : 8.1.6

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

CREATE TABLE `day_off` (
  `id` int(11) NOT NULL,
  `start` date NOT NULL,
  `end` date NOT NULL,
  `reason` text NOT NULL,
  `id_employee` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `day_off`
--

INSERT INTO `day_off` (`id`, `start`, `end`, `reason`, `id_employee`) VALUES
(1, '2022-09-04', '2022-09-06', 'casual', 1);

-- --------------------------------------------------------

--
-- Structure de la table `employee`
--

CREATE TABLE `employee` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `address` varchar(150) NOT NULL,
  `phone` varchar(30) NOT NULL,
  `hiring_day` timestamp NOT NULL DEFAULT current_timestamp(),
  `password` varchar(200) NOT NULL,
  `h_sup` int(11) NOT NULL,
  `leave_without_sold` int(11) NOT NULL,
  `advance` int(11) NOT NULL,
  `id_status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `employee`
--

INSERT INTO `employee` (`id`, `name`, `email`, `address`, `phone`, `hiring_day`, `password`, `h_sup`, `leave_without_sold`, `advance`, `id_status`) VALUES
(1, 'Mionja', 'mionjaranaivoarison@gmail.com', 'My address', '+261 34 07 373 40', '2022-09-02 03:59:38', '$5$rounds=535000$KlEMoGcgQDs3tGEL$wCUfou4fg8AXbOILa.0y1ux9/JgPlnFfhBAJ2BGwHq6', 0, 0, 0, 1),
(2, 'Mpiasa', 'employe@gmail.com', 'Address of employee ', '123456789089', '2022-09-02 04:08:11', '$5$rounds=535000$8aQqfBj8ur0guxif$CLqus7jSx7FYYoEYYoGjUfs/uLEURtZtuXbeO3XuAl0', 0, 0, 0, 2),
(3, 'Mario', 'lovamanitramario@gmail.com', 'Lot IVH 132a Ambohimanandray', '0340731748', '2022-09-02 15:14:18', '$5$rounds=535000$ijl.il1rACneJY9i$6Er6nMKYIX1ZmjQ3QxhANTDrvvRcVBpwEWj/bf9AdC1', 0, 0, 0, 2);

-- --------------------------------------------------------

--
-- Structure de la table `notifications`
--

CREATE TABLE `notifications` (
  `id` int(11) NOT NULL,
  `name` varchar(200) NOT NULL,
  `email` varchar(100) NOT NULL,
  `subject` varchar(200) NOT NULL,
  `message` text NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `notifications`
--

INSERT INTO `notifications` (`id`, `name`, `email`, `subject`, `message`) VALUES
(1, 'Mionja', 'mionjaranaivoarison@gmail.com', 'Noana ', 'NOANA LOATRA AHO E'),
(2, 'test', 'test@gmail.com', 'test', 'This is a teeeest'),
(3, 'Mario', 'lovamanitramario@gmail.com', 'TEST', 'It\'s for the test');

-- --------------------------------------------------------

--
-- Structure de la table `status`
--

CREATE TABLE `status` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `salary` int(11) NOT NULL,
  `day_off` int(11) NOT NULL,
  `cnaps` int(11) NOT NULL,
  `osti` int(11) NOT NULL,
  `irsa` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `status`
--

INSERT INTO `status` (`id`, `name`, `salary`, `day_off`, `cnaps`, `osti`, `irsa`) VALUES
(1, 'CEO', 456, 5, 30, 15, 15),
(2, 'DG', 123, 2, 20, 10, 10),
(3, 'Accounting', 400, 4, 30, 10, 10),
(4, 'Normal Employee', 350, 3, 25, 12, 12),
(5, 'Guardian', 100, 1, 15, 15, 15);

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `day_off`
--
ALTER TABLE `day_off`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_day_off_id_employee` (`id_employee`);

--
-- Index pour la table `employee`
--
ALTER TABLE `employee`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_employee_id_status` (`id_status`);

--
-- Index pour la table `notifications`
--
ALTER TABLE `notifications`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `status`
--
ALTER TABLE `status`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `day_off`
--
ALTER TABLE `day_off`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT pour la table `employee`
--
ALTER TABLE `employee`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT pour la table `notifications`
--
ALTER TABLE `notifications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT pour la table `status`
--
ALTER TABLE `status`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

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
