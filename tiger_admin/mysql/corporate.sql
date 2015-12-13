-- MySQL dump 10.13  Distrib 5.5.45, for Linux (x86_64)
--
-- Host: localhost    Database: corporate
-- ------------------------------------------------------
-- Server version	5.5.45

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `account_tab`
--

DROP TABLE IF EXISTS `account_tab`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `account_tab` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(32) NOT NULL,
  `email` varchar(32) NOT NULL,
  `password` varchar(64) NOT NULL,
  `salt` varchar(32) NOT NULL,
  `status` smallint(6) NOT NULL,
  `create_time` datetime NOT NULL,
  `account_type` smallint(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `company_tab`
--

DROP TABLE IF EXISTS `company_tab`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `company_tab` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `slogan` varchar(128) NOT NULL,
  `url` varchar(64) NOT NULL,
  `description` varchar(256) NOT NULL,
  `create_time` datetime NOT NULL,
  `valid_from` datetime DEFAULT '1900-01-01 00:00:00',
  `valid_to` datetime DEFAULT '9999-01-01 00:00:00',
  `status` smallint(6) NOT NULL,
  `account_id` int(11) NOT NULL,
  `pdf_url` varchar(64) NOT NULL DEFAULT '',
  `is_index` tinyint(1) DEFAULT '0',
  `address` varchar(128) NOT NULL DEFAULT '',
  `email` varchar(64) NOT NULL DEFAULT '',
  `tel` varchar(20) NOT NULL DEFAULT '',
  `fax` varchar(20) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `url` (`url`),
  KEY `company_tab_93025c2f` (`account_id`),
  CONSTRAINT `account_id_refs_id_002207d9` FOREIGN KEY (`account_id`) REFERENCES `account_tab` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `company_tag_tab`
--

DROP TABLE IF EXISTS `company_tag_tab`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `company_tag_tab` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `company_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `company_id` (`company_id`,`tag_id`),
  KEY `company_tag_tab_0316dde1` (`company_id`),
  KEY `company_tag_tab_5659cca2` (`tag_id`),
  CONSTRAINT `company_id_refs_id_799e30ea` FOREIGN KEY (`company_id`) REFERENCES `company_tab` (`id`),
  CONSTRAINT `tag_id_refs_id_88fd8dfe` FOREIGN KEY (`tag_id`) REFERENCES `tag_tab` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `contact_tab`
--

DROP TABLE IF EXISTS `contact_tab`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contact_tab` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sender` varchar(32) NOT NULL,
  `mobile` varchar(20) NOT NULL,
  `email` varchar(64) NOT NULL,
  `title` varchar(64) NOT NULL,
  `content` varchar(512) NOT NULL,
  `create_date` datetime NOT NULL,
  `company_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `contact_tab_0316dde1` (`company_id`),
  CONSTRAINT `company_id_refs_id_71463fd0` FOREIGN KEY (`company_id`) REFERENCES `company_tab` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `customer_tab`
--

DROP TABLE IF EXISTS `customer_tab`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer_tab` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `slogan` varchar(128) NOT NULL,
  `url` varchar(64) NOT NULL,
  `description` varchar(256) NOT NULL,
  `create_time` datetime NOT NULL,
  `valid_from` datetime NOT NULL,
  `valid_to` datetime NOT NULL,
  `status` smallint(6) NOT NULL,
  `account_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `url` (`url`),
  KEY `customer_tab_93025c2f` (`account_id`),
  CONSTRAINT `account_id_refs_id_17f03907` FOREIGN KEY (`account_id`) REFERENCES `account_tab` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `gallery_tab`
--

DROP TABLE IF EXISTS `gallery_tab`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gallery_tab` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `image_url` varchar(64) NOT NULL,
  `is_cover` tinyint(1) NOT NULL,
  `product_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`,`product_id`),
  KEY `gallery_tab_7f1b40ad` (`product_id`),
  CONSTRAINT `product_id_refs_id_c112db26` FOREIGN KEY (`product_id`) REFERENCES `product_tab` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `product_tab`
--

DROP TABLE IF EXISTS `product_tab`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_tab` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `company_id` int(11) NOT NULL,
  `name` varchar(64) NOT NULL,
  `description` varchar(512) NOT NULL,
  `create_date` datetime NOT NULL,
  `status` smallint(6) NOT NULL,
  `pdf_url` varchar(64) DEFAULT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `company_id` (`company_id`,`name`),
  KEY `product_tab_0316dde1` (`company_id`),
  CONSTRAINT `company_id_refs_id_f5094944` FOREIGN KEY (`company_id`) REFERENCES `company_tab` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tag_tab`
--

DROP TABLE IF EXISTS `tag_tab`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tag_tab` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `status` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `video_tab`
--

DROP TABLE IF EXISTS `video_tab`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `video_tab` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `description` varchar(128) NOT NULL,
  `video_url` varchar(256) NOT NULL,
  `host_url` varchar(128) NOT NULL,
  `company_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `video_tab_0316dde1` (`company_id`),
  CONSTRAINT `company_id_refs_id_8a4e4a68` FOREIGN KEY (`company_id`) REFERENCES `company_tab` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-12-13 22:45:31
