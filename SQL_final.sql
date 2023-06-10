CREATE DATABASE `opensource` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
CREATE TABLE `mail_table` (
  `mail_id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(45) NOT NULL,
  `content` varchar(1024) NOT NULL,
  `created_at` varchar(45) NOT NULL,
  `weather` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `send` tinyint(1) DEFAULT '0',
  `ok` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`mail_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `user_table` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `pwd` varchar(45) NOT NULL,
  `birth` varchar(45) NOT NULL,
  `period` varchar(45) NOT NULL,
  `surprise` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
