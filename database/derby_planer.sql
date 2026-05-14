-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 13-05-2026 a las 01:59:03
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `derby_planer`
--
CREATE DATABASE IF NOT EXISTS `derby_planer` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `derby_planer`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `carreras`
--

CREATE TABLE IF NOT EXISTS `carreras` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`dist` int(11) DEFAULT NULL,
`terreno` varchar(20) DEFAULT NULL,
PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- RELACIONES PARA LA TABLA `carreras`:
--

--
-- Truncar tablas antes de insertar `carreras`
--

TRUNCATE TABLE `carreras`;
-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `habilidades`
--

CREATE TABLE IF NOT EXISTS `habilidades` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`nombre` varchar(50) DEFAULT NULL,
PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- RELACIONES PARA LA TABLA `habilidades`:
--

--
-- Truncar tablas antes de insertar `habilidades`
--

TRUNCATE TABLE `habilidades`;
--
-- Volcado de datos para la tabla `habilidades`
--

INSERT INTO `habilidades` (`id`, `nombre`) VALUES
(1, 'Sprint Final'),
(2, 'Recuperación Stamina'),
(3, 'Arranque Explosivo'),
(4, 'Visión de Campo'),
(5, 'Maestro de Curvas'),
(6, 'Resistencia Tierra'),
(7, 'Cierre Veloz'),
(8, 'Ritmo Constante'),
(9, 'Impulso Inicial'),
(10, 'Corazón de Acero'),
(11, 'Zancada Larga'),
(12, 'Análisis de Rival');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `resultados`
--

CREATE TABLE IF NOT EXISTS `resultados` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`user_id` int(11) DEFAULT NULL,
`race_id` int(11) DEFAULT NULL,
`uma_id` int(11) DEFAULT NULL,
`posicion` int(11) DEFAULT NULL,
PRIMARY KEY (`id`),
KEY `user_id` (`user_id`),
KEY `race_id` (`race_id`),
KEY `uma_id` (`uma_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- RELACIONES PARA LA TABLA `resultados`:
--   `user_id`
--       `usuarios` -> `id`
--   `race_id`
--       `carreras` -> `id`
--   `uma_id`
--       `umas` -> `id`
--

--
-- Truncar tablas antes de insertar `resultados`
--

TRUNCATE TABLE `resultados`;
-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `stats`
--

CREATE TABLE IF NOT EXISTS `stats` (
`uma_id` int(11) NOT NULL,
`vel` int(11) DEFAULT NULL,
`sta` int(11) DEFAULT NULL,
`pwr` int(11) DEFAULT NULL,
`intel` int(11) DEFAULT NULL,
PRIMARY KEY (`uma_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- RELACIONES PARA LA TABLA `stats`:
--   `uma_id`
--       `umas` -> `id`
--

--
-- Truncar tablas antes de insertar `stats`
--

TRUNCATE TABLE `stats`;
-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `umas`
--

CREATE TABLE IF NOT EXISTS `umas` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`user_id` int(11) DEFAULT NULL,
`nombre` varchar(50) DEFAULT NULL,
`estilo` varchar(20) DEFAULT NULL,
`suelo_fav` varchar(20) DEFAULT NULL,
PRIMARY KEY (`id`),
KEY `user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- RELACIONES PARA LA TABLA `umas`:
--   `user_id`
--       `usuarios` -> `id`
--

--
-- Truncar tablas antes de insertar `umas`
--

TRUNCATE TABLE `umas`;
-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `uma_habs`
--

CREATE TABLE IF NOT EXISTS `uma_habs` (
`uma_id` int(11) NOT NULL,
`hab_id` int(11) NOT NULL,
PRIMARY KEY (`uma_id`,`hab_id`),
KEY `hab_id` (`hab_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- RELACIONES PARA LA TABLA `uma_habs`:
--   `uma_id`
--       `umas` -> `id`
--   `hab_id`
--       `habilidades` -> `id`
--

--
-- Truncar tablas antes de insertar `uma_habs`
--

TRUNCATE TABLE `uma_habs`;
-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE IF NOT EXISTS `usuarios` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`nombre` varchar(100) NOT NULL,
`email` varchar(100) NOT NULL,
`password` varchar(255) NOT NULL,
PRIMARY KEY (`id`),
UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- RELACIONES PARA LA TABLA `usuarios`:
--

--
-- Truncar tablas antes de insertar `usuarios`
--

TRUNCATE TABLE `usuarios`;
--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `resultados`
--
ALTER TABLE `resultados`
ADD CONSTRAINT `resultados_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `usuarios` (`id`),
ADD CONSTRAINT `resultados_ibfk_2` FOREIGN KEY (`race_id`) REFERENCES `carreras` (`id`),
ADD CONSTRAINT `resultados_ibfk_3` FOREIGN KEY (`uma_id`) REFERENCES `umas` (`id`);

--
-- Filtros para la tabla `stats`
--
ALTER TABLE `stats`
ADD CONSTRAINT `stats_ibfk_1` FOREIGN KEY (`uma_id`) REFERENCES `umas` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `umas`
--
ALTER TABLE `umas`
ADD CONSTRAINT `umas_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `usuarios` (`id`);

--
-- Filtros para la tabla `uma_habs`
--
ALTER TABLE `uma_habs`
ADD CONSTRAINT `uma_habs_ibfk_1` FOREIGN KEY (`uma_id`) REFERENCES `umas` (`id`),
ADD CONSTRAINT `uma_habs_ibfk_2` FOREIGN KEY (`hab_id`) REFERENCES `habilidades` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
