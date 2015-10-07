-- --------------------------------------------------------
-- Host:                         192.168.236.133
-- Server version:               5.5.31-0ubuntu0.12.04.2-log - (Ubuntu)
-- Server OS:                    debian-linux-gnu
-- HeidiSQL Version:             8.0.0.4484
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- Dumping structure for table tiger.contactus_tab
CREATE TABLE IF NOT EXISTS `contactus_tab` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sender` varchar(64) NOT NULL,
  `mobile` varchar(20) NOT NULL,
  `email` varchar(64) NOT NULL,
  `title` varchar(64) NOT NULL,
  `content` varchar(1024) NOT NULL,
  `create_date` datetime NOT NULL,
  `corporate_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_contactus_tab_corporate_tab` (`corporate_id`),
  CONSTRAINT `FK_contactus_tab_corporate_tab` FOREIGN KEY (`corporate_id`) REFERENCES `corporate_tab` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table tiger.contactus_tab: ~0 rows (approximately)
/*!40000 ALTER TABLE `contactus_tab` DISABLE KEYS */;
/*!40000 ALTER TABLE `contactus_tab` ENABLE KEYS */;


-- Dumping structure for table tiger.corporate_tab
CREATE TABLE IF NOT EXISTS `corporate_tab` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(64) NOT NULL,
  `email` varchar(128) NOT NULL,
  `name` varchar(64) NOT NULL,
  `homepage` varchar(128) NOT NULL DEFAULT '',
  `introduction` varchar(1024) NOT NULL DEFAULT '',
  `tel` varchar(20) NOT NULL DEFAULT '',
  `address` varchar(128) NOT NULL DEFAULT '',
  `logo` varchar(64) NOT NULL DEFAULT '',
  `create_date` datetime NOT NULL,
  `last_update_date` datetime NOT NULL,
  `valid_since` datetime NOT NULL DEFAULT '1900-01-01 00:00:00',
  `valid_until` datetime NOT NULL DEFAULT '9999-01-01 00:00:00',
  `status` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table tiger.corporate_tab: ~0 rows (approximately)
/*!40000 ALTER TABLE `corporate_tab` DISABLE KEYS */;
/*!40000 ALTER TABLE `corporate_tab` ENABLE KEYS */;


-- Dumping structure for table tiger.corporate_tag_tab
CREATE TABLE IF NOT EXISTS `corporate_tag_tab` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `corporate_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `corporate_id_tag_id` (`corporate_id`,`tag_id`),
  KEY `FK_corporate_tag_tab_tag_tab` (`tag_id`),
  CONSTRAINT `FK_corporate_tag_tab_contactus_tab` FOREIGN KEY (`corporate_id`) REFERENCES `contactus_tab` (`id`),
  CONSTRAINT `FK_corporate_tag_tab_tag_tab` FOREIGN KEY (`tag_id`) REFERENCES `tag_tab` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table tiger.corporate_tag_tab: ~0 rows (approximately)
/*!40000 ALTER TABLE `corporate_tag_tab` DISABLE KEYS */;
/*!40000 ALTER TABLE `corporate_tag_tab` ENABLE KEYS */;


-- Dumping structure for table tiger.corporate_video_tab
CREATE TABLE IF NOT EXISTS `corporate_video_tab` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `corporate_id` int(11) NOT NULL,
  `video_id` int(11) NOT NULL,
  `create_date` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `corporate_id_video_id` (`corporate_id`,`video_id`),
  KEY `FK_corporate_video_tab_video_tab` (`video_id`),
  CONSTRAINT `FK_corporate_video_tab_corporate_tab` FOREIGN KEY (`corporate_id`) REFERENCES `corporate_tab` (`id`),
  CONSTRAINT `FK_corporate_video_tab_video_tab` FOREIGN KEY (`video_id`) REFERENCES `video_tab` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table tiger.corporate_video_tab: ~0 rows (approximately)
/*!40000 ALTER TABLE `corporate_video_tab` DISABLE KEYS */;
/*!40000 ALTER TABLE `corporate_video_tab` ENABLE KEYS */;


-- Dumping structure for table tiger.gallery_tab
CREATE TABLE IF NOT EXISTS `gallery_tab` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `corporate_id` int(11) NOT NULL,
  `name` varchar(64) NOT NULL,
  `image_url` varchar(64) NOT NULL,
  `description` varchar(256) NOT NULL,
  `create_date` datetime NOT NULL,
  `status` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `image_url` (`image_url`),
  KEY `FK_gallery_tab_corporate_tab` (`corporate_id`),
  CONSTRAINT `FK_gallery_tab_corporate_tab` FOREIGN KEY (`corporate_id`) REFERENCES `corporate_tab` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table tiger.gallery_tab: ~0 rows (approximately)
/*!40000 ALTER TABLE `gallery_tab` DISABLE KEYS */;
/*!40000 ALTER TABLE `gallery_tab` ENABLE KEYS */;


-- Dumping structure for table tiger.tag_tab
CREATE TABLE IF NOT EXISTS `tag_tab` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table tiger.tag_tab: ~0 rows (approximately)
/*!40000 ALTER TABLE `tag_tab` DISABLE KEYS */;
/*!40000 ALTER TABLE `tag_tab` ENABLE KEYS */;


-- Dumping structure for table tiger.video_tab
CREATE TABLE IF NOT EXISTS `video_tab` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `video_url` varchar(128) NOT NULL,
  `name` varchar(64) NOT NULL,
  `description` varchar(256) NOT NULL,
  `create_date` datetime NOT NULL,
  `status` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `video_url` (`video_url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table tiger.video_tab: ~0 rows (approximately)
/*!40000 ALTER TABLE `video_tab` DISABLE KEYS */;
/*!40000 ALTER TABLE `video_tab` ENABLE KEYS */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
