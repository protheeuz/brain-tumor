-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Feb 15, 2025 at 01:24 PM
-- Server version: 8.0.30
-- PHP Version: 7.4.32

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_ikhsan`
--

-- --------------------------------------------------------

--
-- Table structure for table `riwayat_deteksi`
--

CREATE TABLE `riwayat_deteksi` (
  `id_deteksi` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `hasil_label` varchar(255) DEFAULT NULL,
  `confidence` decimal(5,4) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `riwayat_deteksi`
--

INSERT INTO `riwayat_deteksi` (`id_deteksi`, `user_id`, `hasil_label`, `confidence`, `created_at`) VALUES
(1, 4, 'pituitary', '1.0000', '2025-02-10 22:45:24'),
(2, 4, 'glioma', '0.9886', '2025-02-10 23:02:27'),
(3, 7, 'glioma', '1.0000', '2025-02-11 15:55:09'),
(4, 4, 'meningioma', '1.0000', '2025-02-11 16:03:54'),
(5, 4, 'meningioma', '1.0000', '2025-02-11 16:04:38'),
(6, 4, 'meningioma', '1.0000', '2025-02-11 16:05:46'),
(7, 4, 'meningioma', '1.0000', '2025-02-11 16:06:15'),
(8, 4, 'Tidak Tumor', '1.0000', '2025-02-15 13:18:25'),
(9, 4, 'pituitary', '1.0000', '2025-02-15 13:18:41'),
(10, 4, 'meningioma', '1.0000', '2025-02-15 13:19:39');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id_user` int NOT NULL,
  `nama` varchar(100) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('admin','pengunjung') NOT NULL DEFAULT 'pengunjung',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `otp_secret` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id_user`, `nama`, `username`, `password`, `role`, `created_at`, `otp_secret`) VALUES
(4, 'Yanto Suryanto', 'yanto', 'scrypt:32768:8:1$EPxbOPDXIEZDUZaE$3a8d308869b3181ef9391c60cf5bd052bc2a4c02bb149b2fb445dbe08a6d3a1e65b959cff0f1f4cb2ca31cfd979604dc3b43c1a6a0fa6287178a81cac44c3dca', 'pengunjung', '2025-02-10 20:55:14', 'FFRRVEQPS6RMMIV652BV5EQJ47MIEG56'),
(5, 'Mathtech Studio', 'mathtechstudio', 'scrypt:32768:8:1$tvbkf2wlq1OTmjH4$65dd13ea409df310152a450a8218fe4622de0e6dbd6ba8df95b68629ccaf9e90304387aaa9381523e4709ea8b3968a7af04679f601c6779fa1d073c28badf9d7', 'admin', '2025-02-10 21:22:47', 'O2DZDFQYZY6PX7KJF5W4QDKLFSCP46HI'),
(6, 'Iqbal F', 'iqbalfauzien', 'scrypt:32768:8:1$R5atWvqkwooBC5cc$28609eb515ed177f542e0aa928e59efccdeacd9e7b2fe60621f06a5eb87005ba0d27468761f382b545f2568037048401c00cb1a97389f724264ad66be8a7417b', 'admin', '2025-02-10 21:37:17', 'AZZWFJ3AQBID5QY4QW3IN6NIHTQ5EDAB'),
(7, 'muhammad ikhsan surahman', 'ikhsansrhman_', 'scrypt:32768:8:1$6MVZxPtB8yiPJeJP$a4f425c3ff3dc04f029ee19824c250da91d2c4ef7a93480a0ee7055d2de81b625a671daefc4c95c20a8aac873b816e9e5cfa2aa11cb9312f1ef415815cbfb7e3', 'pengunjung', '2025-02-11 15:07:31', 'W4KUTUTY7OHOXTQHX7BPR22CKUDXCQ3D');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `riwayat_deteksi`
--
ALTER TABLE `riwayat_deteksi`
  ADD PRIMARY KEY (`id_deteksi`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id_user`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `riwayat_deteksi`
--
ALTER TABLE `riwayat_deteksi`
  MODIFY `id_deteksi` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id_user` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `riwayat_deteksi`
--
ALTER TABLE `riwayat_deteksi`
  ADD CONSTRAINT `riwayat_deteksi_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id_user`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
