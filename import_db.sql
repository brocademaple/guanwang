CREATE DATABASE IF NOT EXISTS pipedb DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE pipedb;
SOURCE pipedb.sql;
-- MySQL 8.0语法
GRANT ALL PRIVILEGES ON pipedb.* TO 'root'@'localhost';
FLUSH PRIVILEGES;