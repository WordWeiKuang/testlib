-- phpMyAdmin SQL Dump
-- version 4.6.4
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: May 11, 2017 at 03:31 PM
-- Server version: 5.7.13-log
-- PHP Version: 7.0.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `testlib`
--

-- --------------------------------------------------------

--
-- Table structure for table `item`
--

CREATE TABLE `item` (
  `id` varchar(50) NOT NULL,
  `index` int(11) NOT NULL,
  `content` text NOT NULL,
  `answer` text NOT NULL,
  `answer_list` text,
  `answer_A` text,
  `answer_B` text,
  `answer_C` text,
  `answer_D` text,
  `answer_type` varchar(255) NOT NULL,
  `score` int(11) NOT NULL,
  `paper` varchar(50) NOT NULL,
  `ctime` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `paper`
--

CREATE TABLE `paper` (
  `id` varchar(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `tag` varchar(50) DEFAULT NULL,
  `cover` text,
  `brief` text,
  `munber` int(11) DEFAULT NULL,
  `total` float DEFAULT NULL,
  `ctime` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `paper`
--

INSERT INTO `paper` (`id`, `name`, `tag`, `cover`, `brief`, `munber`, `total`, `ctime`) VALUES
('001494512606707b4cb69e1fdc848438c12b233c8abdb83000', '高等数学', '00149451250535151272845f89543549aac821db19ec0a1000', NULL, '11111111', 0, 0, 1494512606.70773),
('00149451264856824521020ae1a4c2a98c79f74903f8de5000', '英语四级', '0014945125119132f1e68c537364e2c8e91c7def3d4ce4a000', NULL, 'test paper', 0, 0, 1494512648.56897),
('001494512663630785da161df4840cc8b1a2acc0c0b4307000', '微积分', '00149451250535151272845f89543549aac821db19ec0a1000', NULL, '12312312', 0, 0, 1494512663.63066);

-- --------------------------------------------------------

--
-- Table structure for table `tag`
--

CREATE TABLE `tag` (
  `id` varchar(50) NOT NULL,
  `pid` varchar(50) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `brief` text,
  `cover` text,
  `ctime` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `tag`
--

INSERT INTO `tag` (`id`, `pid`, `name`, `brief`, `cover`, `ctime`) VALUES
('00149451250535151272845f89543549aac821db19ec0a1000', NULL, 'this is a simp tag', 'bilibili Acfun', NULL, 1494512505.35161),
('0014945125119132f1e68c537364e2c8e91c7def3d4ce4a000', NULL, '1', '1', NULL, 1494512511.91367),
('001494512514614929726a619414d48af1c8b3de33b5c99000', NULL, '2', '3', NULL, 1494512514.61489);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` varchar(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `passwd` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `cover` text,
  `code_key` text,
  `code_sha` text,
  `admin` tinyint(4) NOT NULL,
  `tag` text,
  `ctime` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `name`, `passwd`, `email`, `cover`, `code_key`, `code_sha`, `admin`, `tag`, `ctime`) VALUES
('001494512353034f690f731644f4186ad084d62b109f1f1000', 'admin', 'dd0d1ab024e5e94f3a4edf55eed728e8467bfcf0', 'admin@test.com', NULL, NULL, NULL, 1, NULL, 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `item`
--
ALTER TABLE `item`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `paper`
--
ALTER TABLE `paper`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tag`
--
ALTER TABLE `tag`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
