-- MySQL dump 10.13  Distrib 5.7.30, for Linux (x86_64)
--
-- Host: localhost    Database: App_Covid
-- ------------------------------------------------------
-- Server version	5.7.30-0ubuntu0.18.04.1

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
-- Table structure for table `consul_med`
--

DROP TABLE IF EXISTS `consul_med`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `consul_med` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nif` int(11) NOT NULL,
  `medico_nome` varchar(45) DEFAULT NULL,
  `especialidade` varchar(20) DEFAULT NULL,
  `obser` varchar(30) DEFAULT NULL,
  `data` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`,`nif`),
  KEY `nif` (`nif`),
  CONSTRAINT `consul_med_ibfk_1` FOREIGN KEY (`nif`) REFERENCES `infpes` (`nif`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `consul_med`
--

LOCK TABLES `consul_med` WRITE;
/*!40000 ALTER TABLE `consul_med` DISABLE KEYS */;
INSERT INTO `consul_med` VALUES (1,209432143,'Miguel Oliveira','Medicina Geral',NULL,'01-03-2020'),(2,209432143,'Miguel Fereira','Medicina Geral',NULL,'12-03-2020'),(3,215654970,'Yuri Ferreira','Medicina Interna',NULL,'15-04-2020'),(4,322548962,'Yuri Ferreira','Pneumologia','diabéticos','23-02-2020'),(5,239456876,'Ana Pereira','Medecina Geral',NULL,'09-03-2020'),(6,245965453,'David Duarte','Cardiologia','insuficiência cardíaca','12-05-2020'),(7,356986149,'Luís Guerreiro','Pneumologia',NULL,'22-05-2020');
/*!40000 ALTER TABLE `consul_med` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `examcompl`
--

DROP TABLE IF EXISTS `examcompl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `examcompl` (
  `exam_id` int(11) NOT NULL AUTO_INCREMENT,
  `id` int(11) NOT NULL,
  `nome` varchar(30) NOT NULL,
  `data` varchar(10) NOT NULL,
  `obser` varchar(20) DEFAULT NULL,
  `resultado` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`exam_id`,`id`),
  KEY `id` (`id`),
  CONSTRAINT `examcompl_ibfk_1` FOREIGN KEY (`id`) REFERENCES `consul_med` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `examcompl`
--

LOCK TABLES `examcompl` WRITE;
/*!40000 ALTER TABLE `examcompl` DISABLE KEYS */;
INSERT INTO `examcompl` VALUES (1,1,'Exame Covid-19','01-03-2020','Negativo','01-03-2020'),(2,2,'Exame Covid-19','12-03-2020','Positivo','12-03-2020'),(3,4,'Exame Covid-19','23-02-2020','Positivo','23-02-2020'),(4,5,'Exame Covid-19','09-03-2020','Negativo','09-03-2020'),(5,6,'Exame Covid-19','12-05-2020','Positivo','12-05-2020');
/*!40000 ALTER TABLE `examcompl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `infpes`
--

DROP TABLE IF EXISTS `infpes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `infpes` (
  `nif` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(45) NOT NULL,
  `data_de_nascimento` varchar(10) NOT NULL,
  `email` varchar(60) NOT NULL,
  `telefone` int(11) NOT NULL,
  `codigo_postal` varchar(8) NOT NULL,
  `localidade` varchar(50) NOT NULL,
  PRIMARY KEY (`nif`)
) ENGINE=InnoDB AUTO_INCREMENT=356986150 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `infpes`
--

LOCK TABLES `infpes` WRITE;
/*!40000 ALTER TABLE `infpes` DISABLE KEYS */;
INSERT INTO `infpes` VALUES (209432143,'Alvaro Chines','10-10-1990','alvarones@gmail.com',954684596,'2840-433','Pinhal de Frades'),(215654970,'Claudio Mardinez','25-04-1995','mardinezo@gmail.com',934564786,'2865-678','Quinta das Laranjeiras'),(239456876,'Daniel Nunes','04-03-1998','dnunes@gmail.com',965322766,'2965-261','Lagamecas'),(245965453,'Isabel Andrade','05-07-1999','isadrade@gmail.com',914567845,'2670-377','Loures'),(322548962,'Ana Rodrigues','06-09-2000','anarodr@gmail.com',963243877,'2840-732','Casal do Marco'),(356986149,'Sara Manuela','12-02-2001','samanu@gmail.com',934586943,'2520/267','Peniche');
/*!40000 ALTER TABLE `infpes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `medicacao`
--

DROP TABLE IF EXISTS `medicacao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `medicacao` (
  `med_id` int(11) NOT NULL AUTO_INCREMENT,
  `id` int(11) NOT NULL,
  `nome` varchar(30) NOT NULL,
  `dose` varchar(20) DEFAULT NULL,
  `tratamento` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`med_id`,`id`),
  KEY `id` (`id`),
  CONSTRAINT `medicacao_ibfk_1` FOREIGN KEY (`id`) REFERENCES `consul_med` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medicacao`
--

LOCK TABLES `medicacao` WRITE;
/*!40000 ALTER TABLE `medicacao` DISABLE KEYS */;
INSERT INTO `medicacao` VALUES (1,4,'paracetamol','1000mg','3 vez ao dia'),(2,5,'ibuprofeno','200mg','2 vez ao dia'),(3,6,'paracetamol','1000mg','3 vez ao dia');
/*!40000 ALTER TABLE `medicacao` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sintomas`
--

DROP TABLE IF EXISTS `sintomas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sintomas` (
  `id` int(11) NOT NULL,
  `sintoma` varchar(30) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `sintomas_ibfk_1` FOREIGN KEY (`id`) REFERENCES `consul_med` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sintomas`
--

LOCK TABLES `sintomas` WRITE;
/*!40000 ALTER TABLE `sintomas` DISABLE KEYS */;
INSERT INTO `sintomas` VALUES (4,'febre'),(5,'dores musculares'),(6,'falta de ar');
/*!40000 ALTER TABLE `sintomas` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-07-05 18:54:03
