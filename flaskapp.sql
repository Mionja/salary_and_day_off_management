-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Sep 04, 2022 at 02:56 AM
-- Server version: 5.7.36
-- PHP Version: 7.4.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `flaskapp`
--

-- --------------------------------------------------------

--
-- Table structure for table `day_off`
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
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `day_off`
--

INSERT INTO `day_off` (`id`, `start`, `end`, `reason`, `id_employee`) VALUES
(1, '2022-09-01', '2022-09-02', 'casual', 1),
(2, '2022-09-03', '2022-09-05', 'casual', 1),
(4, '2022-09-13', '2022-09-15', 'sick', 2),
(5, '2022-09-22', '2022-09-23', 'casual', 8),
(6, '2022-09-01', '2022-09-02', 'casual', 8),
(7, '2022-11-03', '2022-11-05', 'casual', 1);

-- --------------------------------------------------------

--
-- Table structure for table `employee`
--

DROP TABLE IF EXISTS `employee`;
CREATE TABLE IF NOT EXISTS `employee` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `address` varchar(150) NOT NULL,
  `phone` varchar(30) NOT NULL,
  `photo` varchar(50) NOT NULL DEFAULT 'default.jpg',
  `hiring_day` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `password` varchar(200) NOT NULL,
  `h_sup` int(11) DEFAULT NULL,
  `advance` int(11) DEFAULT NULL,
  `id_status` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_employee_id_status` (`id_status`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `employee`
--

INSERT INTO `employee` (`id`, `name`, `email`, `address`, `phone`, `photo`, `hiring_day`, `password`, `h_sup`, `advance`, `id_status`) VALUES
(1, 'RANAIVOARISON MIONJA', 'mionjaranaivoarison@gmail.com', 'Earth of the solar system', '+261 34 07 373 40', 'Mionja.jpg', '2022-09-02 03:59:38', '$5$rounds=535000$KlEMoGcgQDs3tGEL$wCUfou4fg8AXbOILa.0y1ux9/JgPlnFfhBAJ2BGwHq6', 0, 62, 1),
(2, 'Mpiasa', 'employe@gmail.com', 'Address of employee ', '123456789089', 'grinning_squinting_face_48px.png', '2022-09-02 04:08:11', '$5$rounds=535000$8aQqfBj8ur0guxif$CLqus7jSx7FYYoEYYoGjUfs/uLEURtZtuXbeO3XuAl0', 0, 55, 2),
(3, 'Mario', 'lovamanitramario@gmail.com', 'Lot IVH 132a Ambohimanandray', '0340731748', 'Mario.jpg', '2022-09-02 15:14:18', '$5$rounds=535000$ijl.il1rACneJY9i$6Er6nMKYIX1ZmjQ3QxhANTDrvvRcVBpwEWj/bf9AdC1', 0, 100, 2),
(8, 'gardian', 'gardian@gmail.com', 'Address of a gardian', '+261 34 07 373 40', 'anya.jpg', '2022-09-04 00:46:53', '$5$rounds=535000$VKhtOiThi/qE.IPl$CGh.7YEIPE1RxLwmY5fznebTGuh..ZbDBVZpT..S2E5', NULL, NULL, 5);

-- --------------------------------------------------------

--
-- Table structure for table `links`
--

DROP TABLE IF EXISTS `links`;
CREATE TABLE IF NOT EXISTS `links` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `website` varchar(200) NOT NULL,
  `github` varchar(200) NOT NULL,
  `twitter` varchar(200) NOT NULL,
  `facebook` varchar(200) NOT NULL,
  `id_employee` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_linkd_id_employee` (`id_employee`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `links`
--

INSERT INTO `links` (`id`, `website`, `github`, `twitter`, `facebook`, `id_employee`) VALUES
(1, 'www.website', 'Mionja', 'Mio_something', 'Mionja Ranaivoarison', 1);

-- --------------------------------------------------------

--
-- Table structure for table `notifications`
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
-- Dumping data for table `notifications`
--

INSERT INTO `notifications` (`id`, `name`, `email`, `subject`, `message`) VALUES
(1, 'Mionja', 'mionjaranaivoarison@gmail.com', 'Noana ', 'NOANA LOATRA AHO E'),
(2, 'test', 'test@gmail.com', 'test', 'This is a teeeest'),
(3, 'Mario', 'lovamanitramario@gmail.com', 'TEST', 'It\'s for the test');

-- --------------------------------------------------------

--
-- Table structure for table `status`
--

DROP TABLE IF EXISTS `status`;
CREATE TABLE IF NOT EXISTS `status` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `salary` int(11) NOT NULL,
  `day_off` int(11) NOT NULL,
  `cnaps` int(11) NOT NULL,
  `osti` int(11) NOT NULL,
  `irsa` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `status`
--

INSERT INTO `status` (`id`, `name`, `salary`, `day_off`, `cnaps`, `osti`, `irsa`) VALUES
(1, 'CEO', 4560, 5, 13, 13, 20),
(2, 'Developer', 1230, 2, 1, 1, 20),
(3, 'Sys Admin', 4000, 4, 1, 1, 20),
(4, 'Normal Employee', 3500, 3, 1, 1, 20),
(5, 'Guardian', 1000, 1, 1, 1, 20);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `day_off`
--
ALTER TABLE `day_off`
  ADD CONSTRAINT `fk_day_off_id_employee` FOREIGN KEY (`id_employee`) REFERENCES `employee` (`id`);

--
-- Constraints for table `employee`
--
ALTER TABLE `employee`
  ADD CONSTRAINT `fk_employee_id_status` FOREIGN KEY (`id_status`) REFERENCES `status` (`id`);

--
-- Constraints for table `links`
--
ALTER TABLE `links`
  ADD CONSTRAINT `fk_linkd_id_employee` FOREIGN KEY (`id_employee`) REFERENCES `employee` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
