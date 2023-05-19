create database opsw;
show databases;
use opsw;

create table user(
`user_id` int NOT NULL auto_increment,
`pwd` varchar(20) NOT NULL,
`name` varchar(20) NOT NULL,
`email` varchar(50) NOT NULL,
`birthday` int NOT NULL,
`period` int NOT NULL,
PRIMARY KEY (`user_id`)
);

create table mail(
`user_id` int NOT NULL,
`created_at` varchar(100) NOT NULL,
`content` varchar(500) NOT NULL,
`weather` int NOT NULL,
`email` varchar(50) NOT NULL,
PRIMARY KEY (`user_id`)
);

