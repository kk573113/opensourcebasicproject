CREATE TABLE `user_table` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `pwd` varchar(45) NOT NULL,
  `birthday` varchar(45) NOT NULL,
  `period` varchar(45) NOT NULL,
  PRIMARY KEY (`user_id`)
);

CREATE TABLE `mail_table` (
  `mail_id` int NOT NULL AUTO_INCREMENT,
  `content` varchar(45) NOT NULL,
  `created_at` varchar(45) NOT NULL,
  `weather` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `send` bool DEFAULT False,
  PRIMARY KEY (`mail_id`)
  )