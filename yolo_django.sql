SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- Create the user_data table
DROP TABLE IF EXISTS `user_data`;
CREATE TABLE `user_data` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `email` varchar(100) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `account` varchar(100) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `password` varchar(256) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `phone` varchar(11) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `avatar` varchar(100) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `add_time` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `gender` varchar(6) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `account` (`account`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ROW_FORMAT=Dynamic;

-- Insert the data for demonstration
INSERT INTO `user_data` VALUES (1, 'test', 'test@gmail.com', 'test', '123456', '12345678901', 'img.png', '2025-7-11 11:38:32.000000', '2025-07-13 08:42:55.000000', '0', 22);


-- Create the django_session table
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session` (
  `session_key` varchar(40) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `session_data` longtext CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ROW_FORMAT=Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
