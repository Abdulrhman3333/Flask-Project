-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 25, 2024 at 07:50 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `aramco`
--

-- --------------------------------------------------------

--
-- Table structure for table `rdc`
--

CREATE TABLE `rdc` (
  `id` int(11) NOT NULL,
  `date` varchar(50) NOT NULL,
  `division` varchar(15) DEFAULT NULL,
  `tech` varchar(70) DEFAULT NULL,
  `dep` varchar(10) NOT NULL,
  `site` varchar(10) NOT NULL,
  `month` varchar(10) NOT NULL,
  `year` varchar(10) NOT NULL,
  `is_checked` varchar(10) NOT NULL,
  `value` int(11) NOT NULL,
  `tpv` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `rdc`
--

INSERT INTO `rdc` (`id`, `date`, `division`, `tech`, `dep`, `site`, `month`, `year`, `is_checked`, `value`, `tpv`) VALUES
(4, '2024-07-24 13:39:45', 'KAUST', 'SAIR (Tanks)', '2', 'Jazan', 'Aug', '2023', 'yes', 300000, 600000),
(5, '2024-07-24 13:39:45', 'KAUST', 'AR Guage Sensor', '3', 'Riyadh', 'Aug', '2023', 'yes', 100000, 300000),
(6, '2024-07-24 13:39:45', 'KAUST', 'RTC', '4', 'RTR-Alahsa', 'Aug', '2023', 'yes', 100000, 400000),
(7, '2024-07-24 13:48:17', 'OGNI', 'HSICM (km)', '4', 'Jeddah-RTR', 'Sep', '2024', 'yes', 200000, 800000),
(8, '2024-07-24 13:48:17', 'OGNI', 'FFS', '2', 'Jazan', 'Sep', '2024', 'yes', 100000, 200000),
(9, '2024-07-24 13:48:34', 'OGT', 'SEEDS', '4', 'Jeddah-RTR', 'Sep', '2024', 'yes', 250000, 1000000),
(10, '2024-07-24 13:48:34', 'OGT', 'Abu Safah Demulsifier', '2', 'Jazan', 'Sep', '2024', 'yes', 150000, 300000),
(11, '2024-07-24 13:49:21', 'F&C', 'HSFCC', '3', 'Jeddah-RTR', 'Oct', '2024', 'yes', 300000, 900000),
(12, '2024-07-24 13:49:21', 'F&C', 'Thermal Crude to Chemicals (TCTC)', '1', 'RTR-Alahsa', 'Oct', '2024', 'yes', 100000, 100000),
(13, '2024-07-24 14:39:52', 'CM', 'ArKaTAC', '3', 'Jeddah-RTR', 'Nov', '2024', 'yes', 100000, 300000),
(14, '2024-07-24 14:39:53', 'CM', 'Aspen Adsorption Process Model for CO2 DAC', '1', 'RTR-Alahsa', 'Nov', '2024', 'no', 0, 0),
(15, '2024-07-24 14:39:53', 'CM', 'Molten borate sorbent for CO2 capture', '2', 'Jazan', 'Nov', '2024', 'no', 0, 0),
(16, '2024-07-24 14:39:53', 'CM', 'Flow Battery', '3', 'Riyadh', 'Nov', '2024', 'no', 0, 0),
(17, '2024-07-24 14:40:13', 'F&C', 'HSFCC', '3', 'Jeddah-RTR', 'Nov', '2024', 'no', 0, 0),
(18, '2024-07-24 14:40:13', 'F&C', 'Thermal Crude to Chemicals (TCTC)', '1', 'RTR-Alahsa', 'Nov', '2024', 'no', 0, 0),
(19, '2024-07-24 14:42:42', 'KAUST', 'AFA', '3', 'Jeddah-RTR', 'Nov', '2024', 'no', 0, 0),
(20, '2024-07-24 14:42:42', 'KAUST', 'DPCUI', '1', 'RTR-Alahsa', 'Nov', '2024', 'no', 0, 0),
(21, '2024-07-24 14:42:42', 'KAUST', 'AR Guage Sensor', '3', 'Riyadh', 'Nov', '2024', 'no', 0, 0),
(22, '2024-07-24 14:42:42', 'KAUST', 'RTC', '2', 'RTR-Alahsa', 'Nov', '2024', 'no', 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `rejected`
--

CREATE TABLE `rejected` (
  `id` int(11) NOT NULL DEFAULT 0,
  `date` varchar(50) NOT NULL,
  `division` varchar(15) DEFAULT NULL,
  `tech` varchar(70) DEFAULT NULL,
  `dep` varchar(10) NOT NULL,
  `site` varchar(10) NOT NULL,
  `month` varchar(10) NOT NULL,
  `year` varchar(10) NOT NULL,
  `is_checked` varchar(10) NOT NULL,
  `value` int(11) NOT NULL,
  `tpv` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `rdc`
--
ALTER TABLE `rdc`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `rdc`
--
ALTER TABLE `rdc`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;



CREATE TABLE rdc8 (
  id int IDENTITY(1, 1) PRIMARY KEY,
  date varchar(50) ,
  division varchar(15) DEFAULT NULL,
  tech varchar(70) DEFAULT NULL,
  dep varchar(10) ,
  site varchar(10) ,
  month varchar(10) ,
  year varchar(10) ,
  is_checked varchar(10) ,
  value int ,
  tpv int 
)