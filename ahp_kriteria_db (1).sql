-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jul 10, 2025 at 03:49 PM
-- Server version: 8.0.30
-- PHP Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ahp_kriteria_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `alternatif`
--

CREATE TABLE `alternatif` (
  `id_alternatif` int NOT NULL,
  `nama_alternatif` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `alternatif`
--

INSERT INTO `alternatif` (`id_alternatif`, `nama_alternatif`) VALUES
(1, 'Motif Batik'),
(2, 'Motif Geometris'),
(3, 'Motif Floral');

-- --------------------------------------------------------

--
-- Table structure for table `bobot_kriteria`
--

CREATE TABLE `bobot_kriteria` (
  `id` int NOT NULL,
  `id_kriteria` int DEFAULT NULL,
  `bobot` decimal(10,4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `bobot_kriteria`
--

INSERT INTO `bobot_kriteria` (`id`, `id_kriteria`, `bobot`) VALUES
(209, 1, 0.5569),
(210, 2, 0.1655),
(211, 3, 0.1530),
(212, 4, 0.1246);

-- --------------------------------------------------------

--
-- Table structure for table `hasil_akhir`
--

CREATE TABLE `hasil_akhir` (
  `id` int NOT NULL,
  `id_alternatif` int DEFAULT NULL,
  `skor_total` decimal(10,4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `hasil_skoring`
--

CREATE TABLE `hasil_skoring` (
  `id` int NOT NULL,
  `upload_id` int DEFAULT NULL,
  `nama_motif` varchar(100) DEFAULT NULL,
  `kualitas_bahan` int DEFAULT NULL,
  `keunikan_motif` int DEFAULT NULL,
  `kombinasi_warna` int DEFAULT NULL,
  `tren_pasar` int DEFAULT NULL,
  `skor_total` decimal(10,4) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `hasil_skoring`
--

INSERT INTO `hasil_skoring` (`id`, `upload_id`, `nama_motif`, `kualitas_bahan`, `keunikan_motif`, `kombinasi_warna`, `tren_pasar`, `skor_total`, `created_at`) VALUES
(1, NULL, 'Jacquard Poly 03', 6, 6, 7, 4, 5.7557, '2025-06-16 11:07:01'),
(2, NULL, 'Maxmara Digital', 9, 6, 7, 6, 7.6197, '2025-06-16 11:07:01'),
(3, NULL, 'Rayon Silky', 8, 8, 7, 5, 7.3208, '2025-06-16 11:07:01'),
(4, NULL, 'Saten Jepang', 9, 6, 8, 3, 7.1907, '2025-06-16 11:07:01'),
(5, NULL, 'Jacquard Poly 03', 6, 6, 7, 4, 5.7557, '2025-06-16 11:08:39'),
(6, NULL, 'Maxmara Digital', 9, 6, 7, 6, 7.6197, '2025-06-16 11:08:39'),
(7, NULL, 'Rayon Silky', 8, 8, 7, 5, 7.3208, '2025-06-16 11:08:39'),
(8, NULL, 'Saten Jepang', 9, 6, 8, 3, 7.1907, '2025-06-16 11:08:39'),
(9, 2, 'Jacquard Poly 03', 6, 6, 7, 4, 5.7557, '2025-06-16 11:14:49'),
(10, 2, 'Maxmara Digital', 9, 6, 7, 6, 7.6197, '2025-06-16 11:14:49'),
(11, 2, 'Rayon Silky', 8, 8, 7, 5, 7.3208, '2025-06-16 11:14:49'),
(12, 2, 'Saten Jepang', 9, 6, 8, 3, 7.1907, '2025-06-16 11:14:49'),
(13, 3, 'Jacquard Poly 03', 6, 6, 7, 4, 5.7557, '2025-06-16 11:48:16'),
(14, 3, 'Maxmara Digital', 9, 6, 7, 6, 7.6197, '2025-06-16 11:48:16'),
(15, 3, 'Rayon Silky', 8, 8, 7, 5, 7.3208, '2025-06-16 11:48:16'),
(16, 3, 'Saten Jepang', 9, 6, 8, 3, 7.1907, '2025-06-16 11:48:16'),
(17, 4, 'Jacquard Poly 03', 6, 6, 7, 4, 5.7557, '2025-06-18 07:43:45'),
(18, 4, 'Maxmara Digital', 9, 6, 7, 6, 7.6197, '2025-06-18 07:43:45'),
(19, 4, 'Rayon Silky', 8, 8, 7, 5, 7.3208, '2025-06-18 07:43:45'),
(20, 4, 'Saten Jepang', 9, 6, 8, 3, 7.1907, '2025-06-18 07:43:45'),
(21, 5, 'Jacquard Poly 03', 6, 6, 7, 4, 5.7557, '2025-06-18 12:01:08'),
(22, 5, 'Maxmara Digital', 9, 6, 7, 6, 7.6197, '2025-06-18 12:01:08'),
(23, 5, 'Rayon Silky', 8, 8, 7, 5, 7.3208, '2025-06-18 12:01:08'),
(24, 5, 'Saten Jepang', 9, 6, 8, 3, 7.1907, '2025-06-18 12:01:08'),
(25, 6, 'Jacquard Poly 03', 6, 6, 7, 4, 5.7557, '2025-06-18 13:06:20'),
(26, 6, 'Maxmara Digital', 9, 6, 7, 6, 7.6197, '2025-06-18 13:06:20'),
(27, 6, 'Rayon Silky', 8, 8, 7, 5, 7.3208, '2025-06-18 13:06:20'),
(28, 6, 'Saten Jepang', 9, 6, 8, 3, 7.1907, '2025-06-18 13:06:20'),
(29, 7, 'Jacquard Poly 03', 6, 6, 7, 4, 5.7557, '2025-06-18 14:40:52'),
(30, 7, 'Maxmara Digital', 9, 6, 7, 6, 7.6197, '2025-06-18 14:40:52'),
(31, 7, 'Rayon Silky', 8, 8, 7, 5, 7.3208, '2025-06-18 14:40:52'),
(32, 7, 'Saten Jepang', 9, 6, 8, 3, 7.1907, '2025-06-18 14:40:52'),
(33, 8, 'Jacquard Poly 03', 6, 6, 7, 4, 5.7557, '2025-06-18 16:44:39'),
(34, 8, 'Maxmara Digital', 9, 6, 7, 6, 7.6197, '2025-06-18 16:44:39'),
(35, 8, 'Rayon Silky', 8, 8, 7, 5, 7.3208, '2025-06-18 16:44:39'),
(36, 8, 'Saten Jepang', 9, 6, 8, 3, 7.1907, '2025-06-18 16:44:39'),
(37, 9, 'Jacquard Poly 03', 6, 6, 7, 4, 5.7557, '2025-06-18 19:54:38'),
(38, 9, 'Maxmara Digital', 9, 6, 7, 6, 7.6197, '2025-06-18 19:54:38'),
(39, 9, 'Rayon Silky', 8, 8, 7, 5, 7.3208, '2025-06-18 19:54:38'),
(40, 9, 'Saten Jepang', 9, 6, 8, 3, 7.1907, '2025-06-18 19:54:38'),
(41, 10, 'Denim', 6, 6, 6, 9, 6.5541, '2025-06-26 12:17:34'),
(42, 10, 'Drill', 6, 6, 6, 7, 6.1847, '2025-06-26 12:17:34'),
(43, 10, 'Katun', 6, 6, 6, 9, 6.5541, '2025-06-26 12:17:34'),
(44, 10, 'Linen', 6, 6, 6, 6, 6.0000, '2025-06-26 12:17:34'),
(45, 10, 'Polyester', 6, 6, 6, 8, 6.3694, '2025-06-26 12:17:34'),
(46, 10, 'Rayon', 7, 6, 6, 9, 7.0523, '2025-06-26 12:17:34'),
(47, 10, 'Satin', 6, 6, 6, 4, 5.6306, '2025-06-26 12:17:34'),
(48, 10, 'Sifon', 6, 6, 6, 9, 6.5541, '2025-06-26 12:17:34'),
(49, 10, 'Spandek', 6, 6, 6, 6, 6.0000, '2025-06-26 12:17:34'),
(50, 10, 'Wol', 6, 6, 6, 5, 5.8153, '2025-06-26 12:17:34'),
(51, 11, 'Rayon Silky', 8, 6, 6, 2, 6.6154, '2025-06-26 12:41:36'),
(52, 11, 'Stretch', 6, 7, 7, 4, 6.0693, '2025-06-26 12:41:36'),
(53, 12, 'Rayon Silky', NULL, 6, 6, 2, 2.1602, '2025-06-28 10:39:55'),
(54, 12, 'Stretch', NULL, 7, 7, 4, 2.7279, '2025-06-28 10:39:55'),
(55, 17, 'Rayon Silky', NULL, 6, 6, 2, 2.1602, '2025-06-28 10:56:40'),
(56, 17, 'Stretch', NULL, 7, 7, 4, 2.7279, '2025-06-28 10:56:40'),
(57, 18, 'Rayon Silky', 8, 6, 6, 2, 6.6154, '2025-06-28 10:56:52'),
(58, 18, 'Stretch', 6, 7, 7, 4, 6.0693, '2025-06-28 10:56:52'),
(59, 19, 'Rayon Silky', 9, 6, 6, 2, 7.1723, '2025-06-28 10:59:20'),
(60, 19, 'Stretch', 9, 7, 7, 4, 7.7400, '2025-06-28 10:59:20');

-- --------------------------------------------------------

--
-- Table structure for table `hasil_upload`
--

CREATE TABLE `hasil_upload` (
  `id` int NOT NULL,
  `waktu_upload` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `hasil_upload`
--

INSERT INTO `hasil_upload` (`id`, `waktu_upload`) VALUES
(2, '2025-06-16 11:14:49'),
(3, '2025-06-16 11:48:16'),
(4, '2025-06-18 07:43:45'),
(5, '2025-06-18 12:01:08'),
(6, '2025-06-18 13:06:20'),
(7, '2025-06-18 14:40:52'),
(8, '2025-06-18 16:44:39'),
(9, '2025-06-18 19:54:38'),
(10, '2025-06-26 12:17:34'),
(11, '2025-06-26 12:41:36'),
(12, '2025-06-28 10:39:55'),
(17, '2025-06-28 10:56:40'),
(18, '2025-06-28 10:56:52'),
(19, '2025-06-28 10:59:20');

-- --------------------------------------------------------

--
-- Table structure for table `kriteria`
--

CREATE TABLE `kriteria` (
  `id_kriteria` int NOT NULL,
  `nama_kriteria` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `kriteria`
--

INSERT INTO `kriteria` (`id_kriteria`, `nama_kriteria`) VALUES
(1, 'Kualitas Bahan'),
(2, 'Keunikan Motif'),
(3, 'Kombinasi Warna'),
(4, 'Tren Pasar');

-- --------------------------------------------------------

--
-- Table structure for table `nilai_alternatif`
--

CREATE TABLE `nilai_alternatif` (
  `id` int NOT NULL,
  `id_alternatif` int DEFAULT NULL,
  `id_kriteria` int DEFAULT NULL,
  `nilai` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `perbandingan_kriteria`
--

CREATE TABLE `perbandingan_kriteria` (
  `id` int NOT NULL,
  `kriteria_1_id` int DEFAULT NULL,
  `kriteria_2_id` int DEFAULT NULL,
  `nilai_perbandingan` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `perbandingan_kriteria`
--

INSERT INTO `perbandingan_kriteria` (`id`, `kriteria_1_id`, `kriteria_2_id`, `nilai_perbandingan`) VALUES
(25, 1, 2, 5.00),
(26, 1, 3, 3.00),
(27, 1, 4, 4.00),
(28, 2, 3, 1.00),
(29, 2, 4, 2.00),
(30, 3, 4, 1.00);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `alternatif`
--
ALTER TABLE `alternatif`
  ADD PRIMARY KEY (`id_alternatif`);

--
-- Indexes for table `bobot_kriteria`
--
ALTER TABLE `bobot_kriteria`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_kriteria` (`id_kriteria`);

--
-- Indexes for table `hasil_akhir`
--
ALTER TABLE `hasil_akhir`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_alternatif` (`id_alternatif`);

--
-- Indexes for table `hasil_skoring`
--
ALTER TABLE `hasil_skoring`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_upload` (`upload_id`);

--
-- Indexes for table `hasil_upload`
--
ALTER TABLE `hasil_upload`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `kriteria`
--
ALTER TABLE `kriteria`
  ADD PRIMARY KEY (`id_kriteria`);

--
-- Indexes for table `nilai_alternatif`
--
ALTER TABLE `nilai_alternatif`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_alternatif` (`id_alternatif`),
  ADD KEY `id_kriteria` (`id_kriteria`);

--
-- Indexes for table `perbandingan_kriteria`
--
ALTER TABLE `perbandingan_kriteria`
  ADD PRIMARY KEY (`id`),
  ADD KEY `kriteria_1_id` (`kriteria_1_id`),
  ADD KEY `kriteria_2_id` (`kriteria_2_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `alternatif`
--
ALTER TABLE `alternatif`
  MODIFY `id_alternatif` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `bobot_kriteria`
--
ALTER TABLE `bobot_kriteria`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=213;

--
-- AUTO_INCREMENT for table `hasil_akhir`
--
ALTER TABLE `hasil_akhir`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `hasil_skoring`
--
ALTER TABLE `hasil_skoring`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=61;

--
-- AUTO_INCREMENT for table `hasil_upload`
--
ALTER TABLE `hasil_upload`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `kriteria`
--
ALTER TABLE `kriteria`
  MODIFY `id_kriteria` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `nilai_alternatif`
--
ALTER TABLE `nilai_alternatif`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `perbandingan_kriteria`
--
ALTER TABLE `perbandingan_kriteria`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `bobot_kriteria`
--
ALTER TABLE `bobot_kriteria`
  ADD CONSTRAINT `bobot_kriteria_ibfk_1` FOREIGN KEY (`id_kriteria`) REFERENCES `kriteria` (`id_kriteria`);

--
-- Constraints for table `hasil_akhir`
--
ALTER TABLE `hasil_akhir`
  ADD CONSTRAINT `hasil_akhir_ibfk_1` FOREIGN KEY (`id_alternatif`) REFERENCES `alternatif` (`id_alternatif`);

--
-- Constraints for table `hasil_skoring`
--
ALTER TABLE `hasil_skoring`
  ADD CONSTRAINT `fk_upload` FOREIGN KEY (`upload_id`) REFERENCES `hasil_upload` (`id`);

--
-- Constraints for table `nilai_alternatif`
--
ALTER TABLE `nilai_alternatif`
  ADD CONSTRAINT `nilai_alternatif_ibfk_1` FOREIGN KEY (`id_alternatif`) REFERENCES `alternatif` (`id_alternatif`),
  ADD CONSTRAINT `nilai_alternatif_ibfk_2` FOREIGN KEY (`id_kriteria`) REFERENCES `kriteria` (`id_kriteria`);

--
-- Constraints for table `perbandingan_kriteria`
--
ALTER TABLE `perbandingan_kriteria`
  ADD CONSTRAINT `perbandingan_kriteria_ibfk_1` FOREIGN KEY (`kriteria_1_id`) REFERENCES `kriteria` (`id_kriteria`),
  ADD CONSTRAINT `perbandingan_kriteria_ibfk_2` FOREIGN KEY (`kriteria_2_id`) REFERENCES `kriteria` (`id_kriteria`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
