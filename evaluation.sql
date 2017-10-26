-- MySQL dump 10.16  Distrib 10.1.13-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: STODaP
-- ------------------------------------------------------
-- Server version	10.1.13-MariaDB-1~trusty

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
-- Table structure for table `evaluation_datasetanswer`
--

DROP TABLE IF EXISTS `evaluation_datasetanswer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `evaluation_datasetanswer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `urls` varchar(1000) NOT NULL,
  `start_time` datetime NOT NULL,
  `end_time` datetime NOT NULL,
  `search_method_id` int(11) NOT NULL,
  `subject_id` int(11) NOT NULL,
  `task_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `evaluation_datasetanswer_539d0c8c` (`search_method_id`),
  KEY `evaluation_datasetanswer_ffaba1d1` (`subject_id`),
  KEY `evaluation_datasetanswer_57746cc8` (`task_id`),
  CONSTRAINT `evaluation__subject_id_6d2d3f7200cd10f4_fk_evaluation_subject_id` FOREIGN KEY (`subject_id`) REFERENCES `evaluation_subject` (`id`),
  CONSTRAINT `evaluation_datase_task_id_53e1e4ded3ee85c0_fk_evaluation_task_id` FOREIGN KEY (`task_id`) REFERENCES `evaluation_task` (`id`),
  CONSTRAINT `search_method_id_1bdb97189bfad096_fk_evaluation_searchmethod_id` FOREIGN KEY (`search_method_id`) REFERENCES `evaluation_searchmethod` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=91 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `evaluation_datasetanswer`
--

LOCK TABLES `evaluation_datasetanswer` WRITE;
/*!40000 ALTER TABLE `evaluation_datasetanswer` DISABLE KEYS */;
INSERT INTO `evaluation_datasetanswer` VALUES (55,'#water stod#####','2016-05-09 00:58:24','2016-05-09 00:58:31',2,37,1),(56,'free proc##','2016-05-09 00:58:31','2016-05-09 00:58:41',3,37,3),(57,'budget exversion####','2016-05-09 00:58:41','2016-05-09 00:58:47',1,37,2),(58,'free budget####','2016-05-09 00:59:32','2016-05-09 00:59:38',3,38,2),(59,'water ex######','2016-05-09 00:59:38','2016-05-09 00:59:44',1,38,1),(60,'stdo proc##','2016-05-09 00:59:44','2016-05-09 00:59:49',2,38,3),(61,'water ex######','2016-05-09 01:00:19','2016-05-09 01:00:26',1,39,1),(62,'#proc stodap#','2016-05-09 01:00:26','2016-05-09 01:00:32',2,39,3),(63,'#budget free###','2016-05-09 01:00:32','2016-05-09 01:00:38',3,39,2),(64,'dd#dd#dd','2016-05-11 17:54:33','2016-05-11 18:28:32',2,40,3),(65,'http://dados.gov.br/dataset/compras-publicas-do-governo-federal#free budget#http://data.vic.gov.au/data/dataset/expenditure-on-consultancies-by-the-department-of-education-and-early-childhood-development#proc stodap#','2016-05-11 18:28:32','2016-05-11 18:28:39',3,40,2),(66,'free budget#http://data.vic.gov.au/data/dataset/expenditure-on-consultancies-by-the-department-of-education-and-early-childhood-development#free budget#http://data.vic.gov.au/data/dataset/expenditure-on-consultancies-by-the-department-of-education-and-early-childhood-development#free budget#budget ex#dd','2016-05-11 18:28:39','2016-05-11 18:28:55',1,40,1),(67,'https://africaopendata.org//dataset/open-budget-survey-2015#http://www.civicdata.io/dataset/school-district-of-philadelphia-budget#https://africaopendata.org//dataset/kenya-open-budget-program-based-budget-2015#https://datahub.io/dataset/2015-budget-portsmouth#https://offenedaten.de//dataset/haushaltsplan-2015-landkreis-ludwigslust-parchim','2016-05-12 17:57:58','2016-05-12 18:04:35',2,44,2),(68,'http://datahub.io//dataset/cauvery#http://datahub.io//dataset/brahmaputra#http://datahub.io//dataset/ganga#http://search.geothermaldata.org/dataset/preliminary-study-of-the-quality-of-water-in-the-drainage-area-of-the-jemez-river-and-rio-guada#http://search.geothermaldata.org/dataset/effect-of-tree-leaves-on-water-quality-in-the-cacapon-river-west-virginia#http://search.geothermaldata.org/dataset/raft-river-monitor-well-potentiometric-head-responses-and-water-quality-as-related-to-the-conce#http://search.geothermaldata.org/dataset/water-quality-control-plan-east-colorado-river-basin-7b','2016-05-12 17:57:24','2016-05-12 18:04:39',2,41,1),(69,'http://africaopendata.org/ (Rivers)#http://catalog.data.gov (SRR - Lower Columbia River)#http://data.gov.uk (Rivers Agency (NI) Designated Watercourses (Metadata))#http://datahub.io/ (Water quality of river Cauvery)#http://catalog.data.gov (Water Quality Bacteria Standards 2016)#http://search.geothermaldata.org (Water Quality Analyses Tule Valley, Utah)#http://search.geothermaldata.org (Water Quality Analyses Big Sand Springs Valley, Nevada)','2016-05-12 17:57:59','2016-05-12 18:06:12',2,45,1),(70,'https://data.gov.uk/dataset/procurement-information-contracts-register#http://japan.census.okfn.org/dataset/contracts#http://dados.gov.br/lv/dataset/paa-programa-de-aquisicao-de-alimentos-da-agricultura-familiar','2016-05-12 17:59:53','2016-05-12 18:06:34',3,47,3),(71,'http://open.canada.ca/data/en/dataset/8826e456-6bb2-4183-8072-f6747ae9db71#http://datahub.io/dataset/2015-budget-portsmouth#http://africaopendata.org/dataset/2015-budget#http://catalog.data.gov/dataset/fy-2015-budget-submission-volume-i#http://dados.gov.br/dataset/orcamento-federal','2016-05-12 18:04:39','2016-05-12 18:08:34',1,41,2),(72,'http://budgetresponsibility.org.uk/download/public-finances-databank/#http://www.ecb.europa.eu/stats/monetary/rates/html/index.en.html#http://www.ecb.europa.eu/press/pdf/md/md1512.pdf#https://data.oecd.org/chart/4xrA#http://dfat.gov.au/about-us/corporate/portfolio-budget-statements/Documents/2014-15_DFAT_PBS_Complete.pdf','2016-05-12 17:57:49','2016-05-12 18:09:31',3,43,2),(73,'https://data.gov.uk/dataset/chemical-river-water-quality-1990to2009#https://datahub.io/dataset/wqis#http://open.canada.ca/data/en/dataset/9ec91c92-22f8-4520-8b2c-0f1cce663e18#http://catalog.data.gov/dataset/lba-eco-cd-06-water-balance-of-the-ji-parana-river-basin-brazil-1995-1996-a0b17#https://data.wa.gov/Goal-3-Sustainable-Energy-and-a-Clean-Environment/G3-3-2-Freshwater-Water-Quality/2yty-mbvh#http://catalog.data.gov/dataset/water-sample-locations-for-fanno-creek-oregon#http://data.sa.gov.au/data/dataset/south-east-ground-water-levels','2016-05-12 17:57:29','2016-05-12 18:09:32',1,42,1),(74,'http://catalog.data.gov/dataset/nyc-budget-revenue#https://datahub.io/dataset/nigeria-2009-budget#https://datahub.io/dataset/kikuyo-budget#https://datahub.io/dataset/southafrican-national-budget#https://datahub.io/dataset/budgets-praha','2016-05-12 18:06:34','2016-05-12 18:09:38',2,47,2),(75,'http://compras.dados.gov.br/docs/home.html#https://buyandsell.gc.ca/procurement-data/#https://www.data.gouv.fr/fr/datasets/citoyennete-liste-des-marches-publics-pour-grand-poitiers/','2016-05-12 18:08:35','2016-05-12 18:12:12',3,41,3),(76,'https://data.gov.uk/dataset/new-liabilities-nndr-2014-20151#https://africaopendata.org/dataset/2015-budget#http://catalog.data.gov/dataset/bills-signed-by-governor-kitzhaber-2015#https://datahub.io/dataset/2015-budget-portsmouth#https://data.sfgov.org/City-Management-and-Ethics/Campaign-Finance-Individual-Expenditure-Ceilings-I/cgah-zci4','2016-05-12 18:06:13','2016-05-12 18:12:35',1,45,2),(77,'https://data.gov.uk/dataset/procurement-information-for-hambleton-district-council#http://dados.gov.br/dataset/compras-publicas-do-governo-federal#','2016-05-12 18:04:35','2016-05-12 18:13:53',1,44,3),(78,'https://datahub.io/dataset/water-quality-river-damodar-rupnarayan-barakar-konar-jumar-bokaro-and-mahananda-2008#http://catalog.data.gov/dataset/hudson-river-valley-greenway-water-trail-designated-sites#https://gisdata.mn.gov/dataset/us-mn-state-metc-water-lakes-rivers#http://catalog.data.gov/dataset/missouri-river-water-trail-access-points-e5bd8#https://data.nasa.gov/Earth-Science/LBA-ECO-CD-06-Water-Balance-of-the-Ji-Parana-River/y88x-gmgd#http://catalog.data.gov/dataset/cahaba-river-national-wildlife-refuge-water-resource-inventory-and-assessment#https://datahub.io/dataset/water-quality','2016-05-12 17:59:09','2016-05-12 18:13:53',1,46,1),(79,'https://data.yorkopendata.org/dataset/procurement-information#http://dados.prefeitura.sp.gov.br/it/dataset/contratos-convenios-e-parcerias#http://catalogo.datos.gob.mx/sv/dataset/montos-maximos-de-adquisiciones','2016-05-12 18:13:53','2016-05-12 18:16:53',3,46,3),(80,'https://datahub.io/dataset/budgets-praha#http://catalog.data.gov/dataset/cahaba-river-national-wildlife-refuge-water-resource-inventory-and-assessment#http://catalog.data.gov/dataset/hydrogeology-mo-1998-natural-ground-water-quality-shp#https://datahub.io/dataset/water-quality#http://catalog.data.gov/dataset/oregon-ag-water-quality-management-areas-map#http://catalog.data.gov/dataset/storage-and-retrieval-for-water-quality-data-storet#http://opendata.arcgis.com/datasets/423b4eae73b74027bd8827f5cdcbb6f5_5','2016-05-12 18:09:39','2016-05-12 18:17:27',1,47,1),(81,'https://data.gov.uk/dataset/procurement-information-contracts-register##','2016-05-12 18:09:31','2016-05-12 18:18:09',1,43,3),(82,'https://datahub.io/dataset/2015-budget-city-of-virginia-beach-va#http://data.nsw.gov.au/data/dataset/56f0b52a-1354-4910-b681-509ecd92888e#https://africaopendata.org//dataset/2015-budget#https://www.data.gv.at/katalog/dataset/voranschlag-2015#http://donnees.ville.montreal.qc.ca//dataset/budget-rosemont-la-petite-patrie','2016-05-12 18:16:53','2016-05-12 18:25:30',2,46,2),(83,'http://catalog.data.gov/dataset/lba-eco-lc-07-water-quality-co2-chlorophyll-lago-curuai-para-brazil-2003-2004-b057d#https://data.sa.gov.au/data/dataset/4666f1a7-cde4-40d0-85ef-f7ec2aec7ca9#http://130.179.67.140/dataset/environment-canada-water-quality-monitoring-stations-east-side-rivers-and-lake-outlet-water-quality#http://search.geothermaldata.org/dataset/reservoir-simulation-study-of-the-onikobe-geothermal-field-japan#http://search.geothermaldata.org/dataset/quality-of-surface-waters-of-the-united-states-1969-part-11-pacific-slope-basins-in-california##','2016-05-12 18:18:09','2016-05-12 18:25:49',2,43,1),(84,'https://datahub.io/dataset/pt-budget#https://data.gov.uk/dataset/engagedx-dataset1-sirc-performance-data-of-social-investment-released-for-first-time#https://data.gov.uk/dataset/finance-expenditure-august-2015#https://data.qld.gov.au/dataset/2015-16-budget-bp3#http://datamx.io/dataset/presupuesto-de-egresos-de-la-ciudad-de-monterrey-2015','2016-05-12 18:09:33','2016-05-12 18:27:01',2,42,2),(85,'http://sos.noaa.gov/Datasets/list.php#http://www.zeus.iag.usp.br/ftp/#','2016-05-12 18:12:36','2016-05-12 18:29:17',3,45,3),(86,'http://dados.gov.br/dataset/compras-publicas-do-governo-federal#https://data.cityofchicago.org/Administration-Finance/Contracts/rsxa-ify5#https://open-data.europa.eu/pt/data/dataset/ted-csv','2016-05-12 18:27:01','2016-05-12 18:39:10',3,42,3),(87,'https://catalog.data.gov/dataset/drainage-areas-for-selected-stream-sampling-stations-missouri-river-basin#https://data.nal.usda.gov/dataset/data-long-term-agroecosystem-research-central-mississippi-river-basin-goodwater-creek-1#http://waterdata.usgs.gov/nwis/uv/?site_no=02469100&PARAmeter_cd=00095,00010,00300,00400#https://catalog.data.gov/dataset/yellowstone-river-basin-study-unit-boundary-national-water-quality-assessment-program-scale-1-1###','2016-05-12 18:13:53','2016-05-12 18:40:13',3,44,1),(88,'##','2016-05-12 19:20:04','2016-05-12 19:20:06',2,48,3),(89,'####','2016-05-12 19:20:07','2016-05-12 19:20:08',1,48,2),(90,'######','2016-05-12 19:20:08','2016-05-12 19:20:09',3,48,1);
/*!40000 ALTER TABLE `evaluation_datasetanswer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `evaluation_subject`
--

DROP TABLE IF EXISTS `evaluation_subject`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `evaluation_subject` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `age` int(11) NOT NULL,
  `internet_ability` int(11) DEFAULT NULL,
  `opendata_ability` int(11) DEFAULT NULL,
  `insert_date` datetime NOT NULL,
  `usefulness` int(11) DEFAULT NULL,
  `usability` int(11) DEFAULT NULL,
  `comments` varchar(1000) DEFAULT NULL,
  `task_order` varchar(50) DEFAULT NULL,
  `search_method_order` varchar(50) DEFAULT NULL,
  `data_ability` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `evaluation_subject`
--

LOCK TABLES `evaluation_subject` WRITE;
/*!40000 ALTER TABLE `evaluation_subject` DISABLE KEYS */;
INSERT INTO `evaluation_subject` VALUES (37,0,4,5,'2016-05-09 00:58:24',3,3,'lkjlkj','1#3#2','2#3#1',2),(38,11,1,4,'2016-05-09 00:59:32',3,3,'','2#1#3','3#1#2',5),(39,9,5,5,'2016-05-09 01:00:18',3,3,'','1#3#2','1#2#3',1),(40,32,1,2,'2016-05-11 17:54:32',4,1,'','3#2#1','2#3#1',5),(41,27,5,1,'2016-05-12 17:57:23',2,4,'','1#2#3','2#1#3',3),(42,23,5,3,'2016-05-12 17:57:29',1,3,'A busca no STDOaP é bem interessante e a navegação foi mais rápida, porém seria interessante explicar no sistema como essa busca facetada é feita, pois se não houvesse a explicação não seria tão intuitivo. ','1#2#3','1#2#3',4),(43,27,5,5,'2016-05-12 17:57:49',4,4,'','2#3#1','3#1#2',5),(44,23,5,3,'2016-05-12 17:57:55',1,2,'Acho que um ponto fundamental para aperfeiçoamento da plataforma é o mapeamento de novos filtros na busca facetada com pontos relevantes de classificação. Por exemplo, seria bom que existisse a possibilidade de classificar os datasets por ano, por país etc. O exemplo de tarefa usada durante o experimento pode ter favorecido a ferramenta em algum momento (algumas buscas são claramente mais eficientes na ferramenta), no entanto a falta de clareza pode também ter prejudicado de certo modo. No mais a ferramenta é relativamente fácil de utilizar e muito mais eficiente que métodos tradicionais, principalmente por agregar datasets que muitas vezes não são de conhecimento do usuário.','2#3#1','2#1#3',4),(45,26,5,2,'2016-05-12 17:57:59',1,1,'','1#2#3','2#1#3',3),(46,29,5,3,'2016-05-12 17:59:09',2,2,'Facilitar na interface retirar um filtro e/ou trocar de filtro.\r\nPoder mesclar filtro, como se fosse uma busca \"multi\" facetada.','1#3#2','1#3#2',5),(47,22,5,1,'2016-05-12 17:59:53',1,1,'','3#2#1','3#2#1',4),(48,22,3,3,'2016-05-12 19:20:02',NULL,NULL,NULL,'3#2#1','2#1#3',3);
/*!40000 ALTER TABLE `evaluation_subject` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-05-13 10:40:09
