/* 
Make sure that following tables are empty before importing this file:
-company
-project
-session
-action
-file
-fileaction
-event
*/

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

INSERT INTO `company` (`name`) VALUES (`Aalto`);

SET @projectid = 1;
SET @sessionid = 4;

INSERT INTO `project` (`id`,`name`, `company_id`, `dir`, `password`) VALUES
(@projectid,'Sample Project', 1, '\\\\WOS-STORAGE\\Projects\\Sample', '');

INSERT INTO `session` (`id`,`name`, `project_id`, `starttime`, `endtime`, `previous_session_id`) VALUES
(1,'', @projectid, '2012-12-03 12:30:00', '2012-12-03 13:42:00', NULL),
(2,'', @projectid, '2012-12-05 11:20:00', '2012-12-05 12:10:00', NULL),
(3,'', @projectid, '2012-12-11 14:15:00', '2012-12-11 16:00:00', NULL),
(4,'', @projectid, '2012-12-17 08:06:00', '2012-12-17 10:23:00', NULL);


INSERT INTO `action` (`id`, `name`) VALUES
(1, 'Created'),
(2, 'Deleted'),
(3, 'Updated'),
(4, 'Renamed from'),
(5, 'Renamed to'),
(6, 'Opened'),
(7, 'Closed');

INSERT INTO `file` (`id`, `path`, `project_id`) VALUES
(1, '\\\\WOS-STORAGE\\Projects\\Sample\\notes.doc', @projectid),
(2, '\\\\WOS-STORAGE\\Projects\\Sample\\communication_slides.pdf', @projectid),
(3, '\\\\WOS-STORAGE\\Projects\\Sample\\query_results.xslx', @projectid),
(4, '\\\\WOS-STORAGE\\Projects\\Sample\\evaluation.pdf', @projectid),
(5, '\\\\WOS-STORAGE\\Projects\\Sample\\project_introduction.pdf', @projectid),
(6, '\\\\WOS-STORAGE\\Projects\\Sample\\model1.jpg', @projectid),
(7, '\\\\WOS-STORAGE\\Projects\\Sample\\model2.jpg', @projectid),
(8, '\\\\WOS-STORAGE\\Projects\\Sample\\model3.jpg', @projectid),
(9, '\\\\WOS-STORAGE\\Projects\\Sample\\model4.jpg', @projectid),
(10, '\\\\WOS-STORAGE\\Projects\\Sample\\model5.jpg', @projectid),
(11, '\\\\WOS-STORAGE\\Projects\\Sample\\sketch1.png', @projectid),
(12, '\\\\WOS-STORAGE\\Projects\\Sample\\sketch2.png', @projectid),
(13, '\\\\WOS-STORAGE\\Projects\\Sample\\sketch3.png', @projectid),
(14, '\\\\WOS-STORAGE\\Projects\\Sample\\logo.png', @projectid),
(15, '\\\\WOS-STORAGE\\Projects\\Sample\\status_051212.pdf', @projectid);

INSERT INTO `fileaction` (`id`,`file_id`, `action_id`, `action_time`, `user_id`, `computer_id`, `session_id`) VALUES
(1,5, 1, '2012-12-03 12:31:00', NULL, 7, @sessionid-3),
(2,5, 3, '2012-12-03 12:31:00', NULL, 7, @sessionid-3),
(3,1, 1, '2012-12-03 12:33:00', NULL, 1, @sessionid-3),
(4,1, 6, '2012-12-03 12:34:00', NULL, 1, @sessionid-3),
(5,5, 6, '2012-12-03 12:37:00', NULL, 7, @sessionid-3),
(6,6, 1, '2012-12-03 12:38:00', NULL, 3, @sessionid-3),
(7,7, 1, '2012-12-03 12:38:00', NULL, 3, @sessionid-3),
(8,8, 1, '2012-12-03 12:38:00', NULL, 3, @sessionid-3),
(9,9, 1, '2012-12-03 12:38:00', NULL, 3, @sessionid-3),
(10,10, 1, '2012-12-03 12:38:00', NULL, 3, @sessionid-3),
(11,6, 3, '2012-12-03 12:39:00', NULL, 3, @sessionid-3),
(12,7, 3, '2012-12-03 12:39:00', NULL, 3, @sessionid-3),
(13,8, 3, '2012-12-03 12:39:00', NULL, 3, @sessionid-3),
(14,9, 3, '2012-12-03 12:39:00', NULL, 3, @sessionid-3),
(15,10, 3, '2012-12-03 12:39:00', NULL, 3, @sessionid-3),
(16,6, 6, '2012-12-03 12:42:00', NULL, 3, @sessionid-3),
(17,7, 6, '2012-12-03 12:42:00', NULL, 3, @sessionid-3),
(18,8, 6, '2012-12-03 12:42:00', NULL, 3, @sessionid-3),
(19,9, 6, '2012-12-03 12:42:00', NULL, 3, @sessionid-3),
(20,10, 6, '2012-12-03 12:42:00', NULL, 3, @sessionid-3),
(21,1, 3, '2012-12-03 12:49:00', NULL, 3, @sessionid-3),
(22,1, 3, '2012-12-03 13:11:00', NULL, 3, @sessionid-3),
(23,4, 1, '2012-12-03 13:23:00', NULL, 3, @sessionid-3),
(24,4, 3, '2012-12-03 13:23:00', NULL, 3, @sessionid-3),
(25,4, 6, '2012-12-03 13:24:00', NULL, 3, @sessionid-3),
(26,1, 3, '2012-12-03 13:29:00', NULL, 3, @sessionid-3),
(27,1, 3, '2012-12-03 13:37:00', NULL, 3, @sessionid-3),
(28,1, 3, '2012-12-03 13:41:00', NULL, 3, @sessionid-3),
(29,.1, 6, '2012-12-05 11:22:00', NULL, 3, @sessionid-2),
(30,5, 1, '2012-12-05 11:23:00', NULL, 3, @sessionid-2),
(31,5, 3, '2012-12-05 11:23:00', NULL, 3, @sessionid-2),
(32,5, 6, '2012-12-05 11:24:00', NULL, 3, @sessionid-2),
(33,1, 3, '2012-12-05 11:42:00', NULL, 3, @sessionid-2),
(34,1, 3, '2012-12-05 12:05:00', NULL, 3, @sessionid-2),
(35,1, 6, '2012-12-11 14:17:00', NULL, 3, @sessionid-1),
(36,2, 1, '2012-12-11 14:18:00', NULL, 3, @sessionid-1),
(37,2, 3, '2012-12-11 14:18:00', NULL, 3, @sessionid-1),
(38,2, 6, '2012-12-11 14:20:00', NULL, 3, @sessionid-1),
(39,1, 3, '2012-12-11 14:43:00', NULL, 3, @sessionid-1),
(40,11, 1, '2012-12-11 14:49:00', NULL, 3, @sessionid-1),
(41,11, 3, '2012-12-11 14:49:00', NULL, 3, @sessionid-1),
(42,12, 1, '2012-12-11 14:49:00', NULL, 3, @sessionid-1),
(43,12, 3, '2012-12-11 14:49:00', NULL, 3, @sessionid-1),
(44,13, 1, '2012-12-11 14:49:00', NULL, 3, @sessionid-1),
(45,13, 3, '2012-12-11 14:49:00', NULL, 3, @sessionid-1),
(46,11, 6, '2012-12-11 14:52:00', NULL, 3, @sessionid-1),
(47,12, 6, '2012-12-11 14:52:00', NULL, 3, @sessionid-1),
(48,13, 6, '2012-12-11 14:52:00', NULL, 3, @sessionid-1),
(49,1, 3, '2012-12-11 15:31:00', NULL, 3, @sessionid-1),
(50,1, 3, '2012-12-11 15:47:00', NULL, 3, @sessionid-1),
(51,3, 1, '2012-12-17 08:09:00', NULL, 3, @sessionid),
(52,3, 3, '2012-12-17 08:09:00', NULL, 3, @sessionid),
(53,4, 1, '2012-12-17 08:09:00', NULL, 3, @sessionid),
(54,4, 3, '2012-12-17 08:09:00', NULL, 3, @sessionid),
(55,3, 6, '2012-12-17 08:10:00', NULL, 3, @sessionid),
(56,4, 6, '2012-12-17 08:10:00', NULL, 3, @sessionid),
(57,1, 6, '2012-12-17 08:15:00', NULL, 3, @sessionid),
(58,1, 3, '2012-12-17 08:45:00', NULL, 3, @sessionid),
(59,1, 3, '2012-12-17 09:12:00', NULL, 3, @sessionid),
(60,3, 3, '2012-12-17 09:34:00', NULL, 3, @sessionid),
(61,3, 3, '2012-12-17 10:06:00', NULL, 3, @sessionid),
(62,3, 3, '2012-12-17 10:20:00', NULL, 3, @sessionid);

INSERT INTO `event` (`time`, `title`, `desc`) VALUES
('2012-12-03 12:31:00', 'Important', ''),
('2012-12-03 12:41:00', 'Action Point', ''),
('2012-12-03 13:01:00', 'Important', ''),
('2012-12-03 13:14:00', 'Marko does UI sketching', ''),
('2012-12-05 11:23:00', 'Default Event', ''),
('2012-12-05 11:41:00', 'Important', ''),
('2012-12-05 11:58:00', 'Action Point', ''),
('2012-12-05 12:16:00', 'Action Point', ''),
('2012-12-11 14:29:00', 'Default Event', ''),
('2012-12-11 14:50:00', 'Default Event', ''),
('2012-12-11 15:12:00', 'Default Event', ''),
('2012-12-11 15:17:00', 'Action Point', ''),
('2012-12-11 15:29:00', 'Action Point', ''),
('2012-12-11 15:32:00', 'Important', ''),
('2012-12-11 15:56:00', 'Default Event', ''),
('2012-12-11 15:57:00', 'Action Point', ''),
('2012-12-17 08:15:00', 'Default Event', ''),
('2012-12-17 08:23:00', 'Default Event', ''),
('2012-12-17 08:45:00', 'Action Point', ''),
('2012-12-17 08:51:00', 'Important', ''),
('2012-12-17 09:11:00', 'Action Point', ''),
('2012-12-17 09:25:00', 'Default Event', ''),
('2012-12-17 09:29:00', 'A new product idea from Mike', ''),
('2012-12-17 09:42:00', 'Action Point', ''),
('2012-12-17 09:56:00', 'Action Point', ''),
('2012-12-17 10:18:00', 'Default Event', ''),
('2012-12-17 10:24:00', 'Action Point', '');



