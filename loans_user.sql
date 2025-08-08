-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 05, 2025 at 12:35 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `loaning_system`
--

-- --------------------------------------------------------

--
-- Table structure for table `loans_user`
--

CREATE TABLE `loans_user` (
  `id` bigint(20) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `email` varchar(254) DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  `age` varchar(10) DEFAULT NULL,
  `username` varchar(150) NOT NULL,
  `is_enduser` tinyint(1) NOT NULL,
  `profile` varchar(100) DEFAULT NULL,
  `address` longtext DEFAULT NULL,
  `gender` varchar(10) NOT NULL,
  `profession` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `loans_user`
--

INSERT INTO `loans_user` (`id`, `password`, `last_login`, `is_superuser`, `first_name`, `last_name`, `is_staff`, `is_active`, `date_joined`, `email`, `name`, `phone_number`, `age`, `username`, `is_enduser`, `profile`, `address`, `gender`, `profession`) VALUES
(1, 'pbkdf2_sha256$600000$CvupiPVFkGFJ3FtWTJMZhY$qJIXfF9BQgP714OtoUGwVFSqTRatIhor2rj2T7XLlLw=', '2025-08-05 10:20:33.985226', 1, 'Felix', 'Odhiambo', 1, 1, '2025-07-27 14:22:21.616509', 'fellomarley7@gmail.com', 'Fello Marley7', '0794735993', NULL, 'StoryTeller7', 0, 'profiles/IMG_20250731_104429_1.jpg', '71, Maseno', 'male', 'full stack developer'),
(2, 'pbkdf2_sha256$600000$UVXBIF2B8qeGXtT2o6yBuL$+bVOLLYX197AGmjuyGsBzMSQcQuwKmKefaaZ2b1ofO4=', '2025-08-03 19:22:38.155613', 0, '', '', 0, 1, '2025-07-27 17:12:03.408444', 'felixngwono@gmail.com', 'Felix Odhiambo', '0700369300', '2025', 'Salima', 1, 'profiles/IMG-20250724-WA0007.jpg', '00100, Nairobi', 'male', 'software developer'),
(3, 'pbkdf2_sha256$600000$mskzgLGqYmQjDLPG60qvCY$YMgJvBe2QDZtmk/HQwkcA6KvN+wheLPmr84dL6zg4hE=', '2025-07-29 18:27:01.026301', 0, '', '', 0, 1, '2025-07-28 20:17:00.225685', 'egan@gmail.com', 'Tommy Egan', '0778951547', '1995', 'Egan', 1, 'profiles/IMG-20250724-WA0008.jpg', '80, Mombasa', 'male', 'drug dealer'),
(4, 'pbkdf2_sha256$600000$POSOWWcVye9y9MK3YCSsf6$XFoXVFIlt0gIjYqoclsXzEK0hQxKvAokcySSOf7Thdg=', '2025-08-04 11:27:56.027261', 0, '', '', 0, 1, '2025-07-29 06:38:31.466246', 'jamie@gmail.com', 'Jamie Ghost', '0789562314', '2023-09-11', 'Jamie', 1, 'profiles/IMG_20231006_085543_1.jpg', '67, Eldoret', 'male', 'club owner'),
(5, 'pbkdf2_sha256$600000$cjGHJToDZPKV7f8Yp1DEt1$+foatzUDQoVk2tpuIpgutblg4nbSPtxso2P/m2BoN/I=', '2025-08-04 11:25:13.251886', 0, '', '', 0, 1, '2025-07-29 07:01:44.110440', 'stpatrick@gmail.com', 'Jamie St. Patrick', '0712345678', NULL, 'JamieStPatrick', 0, 'profiles/IMG_20231003_124900.jpg', '20, Nakuru', 'male', 'engineer'),
(6, 'pbkdf2_sha256$600000$2Jd25IR09WKDSX1COBlhDT$+iGvLF4DUHZZ/wnksH2h0cmD5sAsbZ0zhMyg/EO83Hw=', '2025-08-04 08:13:15.609135', 0, '', '', 0, 1, '2025-07-29 18:10:13.599053', 'odhiambo@gmail.com', 'Odhiambo Felix', '0756987456', '1997-06-10', 'Odhis', 1, 'profiles/IMG-20250724-WA0011.jpg', '01000, Moi Avenue Nairobi', 'male', 'developer'),
(7, 'pbkdf2_sha256$600000$y5Tp66RRzjvbweaHs62vRn$mL8fnuwdjMC/M4lVHoQS/Dma2pWYXYEZk/6Hn6PKxJU=', '2025-08-03 08:40:13.381347', 0, '', '', 0, 1, '2025-08-03 08:39:40.043307', 'sandeval@gmail.com', 'Mike Sandeval', '0789562312', '1981-05-03', 'Sandeval', 1, 'profiles/bc4f9597d5a345fb919debbd4bbecced.jpg', '80 Nyalenda, Kisumu, Kenya', 'male', 'Lawyer'),
(8, 'pbkdf2_sha256$600000$exN20pIMYk4j3zTe1bR57P$V4urWRQx9DWnm5NMQB5oS1jHYQ4xZrDOrU2ku1akTqU=', '2025-08-03 08:46:23.132369', 0, '', '', 0, 1, '2025-08-03 08:46:03.008089', 'mercy@gmail.com', 'Mercy Wanjiru', '0745789215', '1992-06-09', 'Mercy77', 1, 'profiles/7a475dcab8ce47a28381381da4572739.jpg', '20 Ukunda, Mombasa,Kenya', 'female', 'Teacher'),
(9, 'pbkdf2_sha256$600000$vdiwYNC3pHvRmWGTeku9yb$JEyGfnBPHQW+S1Djsh2rOErbtsEXhziBcYRb/1h5wvQ=', '2025-08-03 17:29:34.415672', 0, '', '', 0, 1, '2025-08-03 09:40:29.212996', 'shanty@gmail.com', 'Shanti Page', '0725874136', NULL, 'ShantPage7', 0, 'profiles/2be4a60d35a044cf8ff2505d191275ff.jpg', '14, Chicago', 'female', 'Mogul');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `loans_user`
--
ALTER TABLE `loans_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `loans_user_username_67875221_uniq` (`username`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `phone_number` (`phone_number`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `loans_user`
--
ALTER TABLE `loans_user`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
