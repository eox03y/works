-- MySQL dump 10.13  Distrib 5.1.66, for debian-linux-gnu (x86_64)
--
-- Host: 10.0.6.62    Database: enwiktionary
-- ------------------------------------------------------
-- Server version	5.5.29-MariaDB-mariadb1~precise-log

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
-- Table structure for table `image`
--

DROP TABLE IF EXISTS `image`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `image` (
  `img_name` varbinary(255) NOT NULL DEFAULT '',
  `img_size` int(8) unsigned NOT NULL DEFAULT '0',
  `img_width` int(5) NOT NULL DEFAULT '0',
  `img_height` int(5) NOT NULL DEFAULT '0',
  `img_metadata` mediumblob NOT NULL,
  `img_bits` int(3) NOT NULL DEFAULT '0',
  `img_media_type` enum('UNKNOWN','BITMAP','DRAWING','AUDIO','VIDEO','MULTIMEDIA','OFFICE','TEXT','EXECUTABLE','ARCHIVE') DEFAULT NULL,
  `img_major_mime` enum('unknown','application','audio','image','text','video','message','model','multipart') NOT NULL DEFAULT 'unknown',
  `img_minor_mime` varbinary(32) NOT NULL DEFAULT 'unknown',
  `img_description` tinyblob NOT NULL,
  `img_user` int(5) unsigned NOT NULL DEFAULT '0',
  `img_user_text` varbinary(255) NOT NULL DEFAULT '',
  `img_timestamp` varbinary(14) NOT NULL DEFAULT '',
  `img_sha1` varbinary(32) NOT NULL DEFAULT '',
  PRIMARY KEY (`img_name`),
  KEY `img_size` (`img_size`),
  KEY `img_timestamp` (`img_timestamp`),
  KEY `img_usertext_timestamp` (`img_user_text`,`img_timestamp`),
  KEY `img_sha1` (`img_sha1`)
) ENGINE=InnoDB DEFAULT CHARSET=binary;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `image`
--

/*!40000 ALTER TABLE `image` DISABLE KEYS */;
INSERT INTO `image` VALUES ('Books-aj.svg_aj_ashton_01e.svg',10563,309,274,'a:3:{s:5:\"width\";i:309;s:6:\"height\";i:274;s:7:\"version\";i:2;}',0,'DRAWING','image','svg+xml','Copy of [[commons:File:Books-aj.svg aj ashton 01e.svg]], duplicated here to prevent Main Page vandalism.',224635,'Yair rand','20100611050645','4a71r1wv9pvjhn4rr5n115v16gsad85'),('Far_Side_1982-05-28_-_Thagomizer.png',25581,199,260,'a:6:{s:10:\"frameCount\";i:0;s:9:\"loopCount\";i:1;s:8:\"duration\";d:0;s:8:\"bitDepth\";i:8;s:9:\"colorType\";s:9:\"greyscale\";s:8:\"metadata\";a:4:{s:11:\"XResolution\";s:8:\"3937/100\";s:11:\"YResolution\";s:8:\"3937/100\";s:14:\"ResolutionUnit\";i:3;s:15:\"_MW_PNG_VERSION\";i:1;}}',8,'BITMAP','image','png','Low-resolution scan of a single-panel \'\'The Far Side\'\' comic by Gary Larson, published 1982-05-02, in which {{term|thagomizer}} was first coined.\n\n===Fair use rationale===\nI have a good faith belief that [[Wiktionary:Copyrights|fair use]] applies to this ',33343,'Robin Lionheart','20120216235625','ccz2vm1f7a8j11k7ry9vhnyiawvhz5v'),('Google_Books_screenshot.png',96951,537,706,'a:6:{s:10:\"frameCount\";i:0;s:9:\"loopCount\";i:1;s:8:\"duration\";d:0;s:8:\"bitDepth\";i:8;s:9:\"colorType\";s:10:\"truecolour\";s:8:\"metadata\";a:4:{s:11:\"XResolution\";s:8:\"2835/100\";s:11:\"YResolution\";s:8:\"2835/100\";s:14:\"ResolutionUnit\";i:3;s:15:\"_MW_PNG_VERSION\";i:1;}}',8,'BITMAP','image','png','http://books.google.com/books?id=4_0vAAAAYAAJ&pg=PA27&dq=%22he%27s%22',8006,'Msh210','20120213180710','jhr5yaharhk8fxam9n4kvuhqn3g6wsh'),('HebrewFontComparison.png',46051,639,474,'a:6:{s:10:\"frameCount\";i:0;s:9:\"loopCount\";i:1;s:8:\"duration\";d:0;s:8:\"bitDepth\";i:8;s:9:\"colorType\";s:16:\"truecolour-alpha\";s:8:\"metadata\";a:4:{s:11:\"XResolution\";s:8:\"3780/100\";s:11:\"YResolution\";s:8:\"3780/100\";s:14:\"ResolutionUnit\";i:3;s:15:\"_MW_PNG_VERSION\";i:1;}}',8,'BITMAP','image','png','Forgot to save the typo fix before uploading...',93335,'Wikitiki89','20130123204503','izbwr6qxhe7m73pbr9qnh3b5d3k0voy'),('Hippietrail_dictionaries.JPG',1780880,2304,3072,'a:32:{s:16:\"ImageDescription\";s:31:\"OLYMPUS DIGITAL CAMERA         \";s:4:\"Make\";s:23:\"OLYMPUS IMAGING CORP.  \";s:5:\"Model\";s:10:\"FE210,X775\";s:11:\"XResolution\";s:5:\"314/1\";s:11:\"YResolution\";s:5:\"314/1\";s:14:\"ResolutionUnit\";i:2;s:8:\"Software\";s:31:\"1.0                            \";s:8:\"DateTime\";s:19:\"2009:08:11 13:28:36\";s:16:\"YCbCrPositioning\";i:2;s:14:\"CustomRendered\";i:0;s:12:\"ExposureMode\";i:0;s:12:\"WhiteBalance\";i:0;s:16:\"DigitalZoomRatio\";s:7:\"100/100\";s:16:\"SceneCaptureType\";i:1;s:8:\"Contrast\";i:0;s:10:\"Saturation\";i:0;s:9:\"Sharpness\";i:0;s:12:\"ExposureTime\";s:3:\"1/4\";s:7:\"FNumber\";s:5:\"31/10\";s:15:\"ExposureProgram\";i:5;s:15:\"ISOSpeedRatings\";i:125;s:11:\"ExifVersion\";s:4:\"0221\";s:16:\"DateTimeOriginal\";s:19:\"2009:08:11 13:28:36\";s:17:\"DateTimeDigitized\";s:19:\"2009:08:11 13:28:36\";s:17:\"ExposureBiasValue\";s:4:\"0/10\";s:16:\"MaxApertureValue\";s:7:\"326/100\";s:12:\"MeteringMode\";i:2;s:11:\"LightSource\";i:0;s:5:\"Flash\";i:16;s:11:\"FocalLength\";s:7:\"630/100\";s:10:\"ColorSpace\";i:1;s:22:\"MEDIAWIKI_EXIF_VERSION\";i:1;}',8,'BITMAP','image','jpeg','Some of my dictionaries, grammars, and language books.',671,'Hippietrail','20090811081351','nhfni7swvcklm8t0jl6dfzyj8gsz58e'),('Hólǫ́_screenshot.png',4007,443,70,'a:6:{s:10:\"frameCount\";i:0;s:9:\"loopCount\";i:1;s:8:\"duration\";d:0;s:8:\"bitDepth\";i:8;s:9:\"colorType\";s:10:\"truecolour\";s:8:\"metadata\";a:4:{s:11:\"XResolution\";s:8:\"3778/100\";s:11:\"YResolution\";s:8:\"3778/100\";s:14:\"ResolutionUnit\";i:3;s:15:\"_MW_PNG_VERSION\";i:1;}}',8,'BITMAP','image','png','Screenshot showing font oddities, displayed in Firefox 18.0 on fully patched Win 7.',12340,'Eirikr','20130126004933','7e62zsaoembikl1qy6af4321ilwz4oa'),('Japanese_writing.pdf',115744,1240,1754,'a:13:{s:7:\"Creator\";s:28:\"Microsoft® Office Word 2007\";s:8:\"Producer\";s:28:\"Microsoft® Office Word 2007\";s:12:\"CreationDate\";s:24:\"Sun Jan 13 14:20:26 2013\";s:7:\"ModDate\";s:24:\"Sun Jan 13 14:20:26 2013\";s:6:\"Tagged\";s:3:\"yes\";s:5:\"Pages\";s:1:\"3\";s:9:\"Encrypted\";s:2:\"no\";s:5:\"pages\";a:3:{i:1;a:1:{s:9:\"Page size\";s:23:\"595.2 x 841.92 pts (A4)\";}i:2;a:1:{s:9:\"Page size\";s:23:\"841.92 x 595.2 pts (A4)\";}i:3;a:1:{s:9:\"Page size\";s:23:\"595.2 x 841.92 pts (A4)\";}}s:9:\"File size\";s:12:\"115744 bytes\";s:9:\"Optimized\";s:2:\"no\";s:11:\"PDF version\";s:3:\"1.5\";s:14:\"mergedMetadata\";a:5:{s:8:\"Software\";s:28:\"Microsoft® Office Word 2007\";s:12:\"pdf-Producer\";s:28:\"Microsoft® Office Word 2007\";s:13:\"pdf-Encrypted\";s:2:\"no\";s:12:\"pdf-PageSize\";a:2:{i:0;s:23:\"595.2 x 841.92 pts (A4)\";i:1;s:23:\"841.92 x 595.2 pts (A4)\";}s:11:\"pdf-Version\";s:3:\"1.5\";}s:4:\"text\";a:4:{i:0;s:84:\"スーパーマリオ USA\nスーパーマリオ USA\nスーパーマリオＵＳＡ\n\n\";i:1;s:108:\"ス\nー\nパ\nー\nマ\nリ\nオ\n\nス\nー\nパ\nー\nマ\nリ\nオ\nUSA\n\nUSA\n\nス\nー\nパ\nー\nマ\nリ\nオ\nＵ\nＳ\nＡ\n\n\";i:2;s:0:\"\";i:3;s:0:\"\";}}',0,'OFFICE','application','pdf','for [[WT:RFM#ＣＤ]]',55840,'Liliana-60','20130113132200','22etih978pw9org3hjwjr2m7f63r4a7'),('Logo_book2.png',7180,74,52,'a:3:{s:10:\"frameCount\";i:0;s:9:\"loopCount\";i:1;s:8:\"duration\";d:0;}',8,'BITMAP','image','png','Copy of [[commons:Logo_book2.png]], duplicated here to prevent Main Page vandalism.',224635,'Yair rand','20100611050436','aax8c8hcwcp3707m9n7xkq1449wa2oy'),('Notepad_icon.png',6962,71,59,'a:3:{s:10:\"frameCount\";i:0;s:9:\"loopCount\";i:1;s:8:\"duration\";d:0;}',8,'BITMAP','image','png','Copy of [[commons:Notepad_icon.png]], duplicated here to prevent Main Page vandalism.',224635,'Yair rand','20100611050222','35p46fl1wtgnfknv9kyne6hzgrqhjk8'),('Screenshot_demonstrating_translation_table_rendering_bug.png',41611,552,362,'a:6:{s:10:\"frameCount\";i:0;s:9:\"loopCount\";i:1;s:8:\"duration\";d:0;s:8:\"bitDepth\";i:8;s:9:\"colorType\";s:16:\"truecolour-alpha\";s:8:\"metadata\";a:4:{s:11:\"XResolution\";s:8:\"3779/100\";s:11:\"YResolution\";s:8:\"3779/100\";s:14:\"ResolutionUnit\";i:3;s:15:\"_MW_PNG_VERSION\";i:1;}}',8,'BITMAP','image','png','Screenshot demonstrating translation table rendering bug',283,'Timwi','20130121201827','menn26l9zpb6oztwbqemxkobv2gflmz'),('Test_silliness.png',31956,345,343,'a:6:{s:10:\"frameCount\";i:0;s:9:\"loopCount\";i:1;s:8:\"duration\";d:0;s:8:\"bitDepth\";i:8;s:9:\"colorType\";s:10:\"truecolour\";s:8:\"metadata\";a:4:{s:11:\"XResolution\";s:8:\"3779/100\";s:11:\"YResolution\";s:8:\"3779/100\";s:14:\"ResolutionUnit\";i:3;s:15:\"_MW_PNG_VERSION\";i:1;}}',8,'BITMAP','image','png','Test PNG upload.',12340,'Eirikr','20120523203527','becgs9f8wymj0eufc1nsiizylp0ndhu'),('Wiki.png',8897,135,135,'a:6:{s:10:\"frameCount\";i:0;s:9:\"loopCount\";i:1;s:8:\"duration\";d:0;s:8:\"bitDepth\";i:8;s:9:\"colorType\";s:15:\"greyscale-alpha\";s:8:\"metadata\";a:1:{s:15:\"_MW_PNG_VERSION\";i:1;}}',8,'BITMAP','image','png','optimized, should reduce server traffic and client download time',55840,'Liliana-60','20120523190359','le0i8qt2pncpc93w5jt965mvgxe97mr'),('Wikipedia-logo-en.png',45283,200,200,'a:3:{s:10:\"frameCount\";i:0;s:9:\"loopCount\";i:1;s:8:\"duration\";d:0;}',8,'BITMAP','image','png','',224635,'Yair rand','20100604212250','ttqnfq8yw1cmcbdxzzdy5zgwbzyktx6'),('Wiktionary-favicon-en-colored.png',13552,150,86,'a:3:{s:10:\"frameCount\";i:0;s:9:\"loopCount\";i:1;s:8:\"duration\";d:0;}',8,'BITMAP','image','png','',4369,'Dominic','20071019083045','hgcpdo0jlz31zdvex7ri20gwkkwavg7'),('Wiktionary-favicon-en.png',7320,150,47,'a:3:{s:10:\"frameCount\";i:0;s:9:\"loopCount\";i:1;s:8:\"duration\";d:0;}',8,'BITMAP','image','png','',4369,'Dominic','20071019073924','4j0q56740u21ckgtw1kw3vs58an3j8e'),('Writing_star.svg',161448,580,470,'a:4:{s:5:\"width\";i:580;s:6:\"height\";i:470;s:8:\"metadata\";s:335:\"\n    <rdf:RDF xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\" xmlns:cc=\"http://web.resource.org/cc/\" xmlns:dc=\"http://purl.org/dc/elements/1.1/\">\n      <cc:Work rdf:about=\"\">\n        <dc:format>image/svg+xml</dc:format>\n        <dc:type rdf:resource=\"http://purl.org/dc/dcmitype/StillImage\"/>\n      </cc:Work>\n    </rdf:RDF>\n  \";s:7:\"version\";i:2;}',0,'DRAWING','image','svg+xml','Copy of [[commons:File:Writing star.svg]], duplicated here to prevent against Main Page vandalism.',224635,'Yair rand','20100611045855','tw0ljvqdhp05l4sg2ftw00q1u4nn4n5'),('YR\'s_scripts.PNG',390051,1263,898,'a:3:{s:10:\"frameCount\";i:0;s:9:\"loopCount\";i:1;s:8:\"duration\";d:0;}',8,'BITMAP','image','png','',224635,'Yair rand','20110106165955','751zjb3exm2vdifg1z6v4nhldagfk3i'),('cyrillic_fonts_demonstration.png',136327,1720,808,'a:6:{s:10:\"frameCount\";i:0;s:9:\"loopCount\";i:1;s:8:\"duration\";d:0;s:8:\"bitDepth\";i:8;s:9:\"colorType\";s:10:\"truecolour\";s:8:\"metadata\";a:6:{s:11:\"XResolution\";s:8:\"2835/100\";s:11:\"YResolution\";s:8:\"2835/100\";s:14:\"ResolutionUnit\";i:3;s:8:\"DateTime\";s:19:\"2013:02:13 01:13:01\";s:14:\"PNGFileComment\";a:2:{s:9:\"x-default\";s:17:\"Created with GIMP\";s:5:\"_type\";s:4:\"lang\";}s:15:\"_MW_PNG_VERSION\";i:1;}}',8,'BITMAP','image','png','For [[WT:Beer parlour/2013/February#Old Cyrillic script in headwords]]',21371,'CodeCat','20130213011709','9ptlroycll4f086ccrjyy0zanlcwflz'),('ezrasil-taameyfrank-arial.PNG',10594,407,333,'a:6:{s:10:\"frameCount\";i:0;s:9:\"loopCount\";i:1;s:8:\"duration\";d:0;s:8:\"bitDepth\";i:8;s:9:\"colorType\";s:10:\"truecolour\";s:8:\"metadata\";a:1:{s:15:\"_MW_PNG_VERSION\";i:1;}}',8,'BITMAP','image','png','Temporary upload to show how the fonts Ezra SIL (top of each triplet), Taamey Frank CLM (middle) and, for reference, Arial (bottom) behave at size 14 (top triplet), 12, 10 and 8 (bottom).',444485,'-sche','20130123171652','fwv7z9b3t09vokdmcxw7afuvd5r7obr'),('favicon.png',4248,32,32,'a:6:{s:10:\"frameCount\";i:0;s:9:\"loopCount\";i:1;s:8:\"duration\";d:0;s:8:\"bitDepth\";i:8;s:9:\"colorType\";s:16:\"truecolour-alpha\";s:8:\"metadata\";a:6:{s:15:\"PixelXDimension\";s:2:\"40\";s:15:\"PixelYDimension\";s:2:\"30\";s:11:\"XResolution\";s:8:\"5669/100\";s:11:\"YResolution\";s:8:\"5669/100\";s:14:\"ResolutionUnit\";i:3;s:15:\"_MW_PNG_VERSION\";i:1;}}',8,'BITMAP','image','png','Testing higher resolution (made by myself).',5174,'Krun','20130215121736','3ts0dyjdt318swsyopvn1ezi0jaw1xa'),('ipa-rendering-ff.png',5924,285,100,'a:6:{s:10:\"frameCount\";i:0;s:9:\"loopCount\";i:1;s:8:\"duration\";d:0;s:8:\"bitDepth\";i:8;s:9:\"colorType\";s:10:\"truecolour\";s:8:\"metadata\";a:4:{s:11:\"XResolution\";s:8:\"3779/100\";s:11:\"YResolution\";s:8:\"3779/100\";s:14:\"ResolutionUnit\";i:3;s:15:\"_MW_PNG_VERSION\";i:1;}}',8,'BITMAP','image','png','Screenshot of IPA rendering, showing problems with tie bars and letters being raised/lowered. Taken in Firefox. File can be deleted after problem is resolved.',444485,'-sche','20120312204022','k8xw3iw48061dv9af1s3kgm0dzyird6'),('ipa-rendering.png',5545,225,100,'a:6:{s:10:\"frameCount\";i:0;s:9:\"loopCount\";i:1;s:8:\"duration\";d:0;s:8:\"bitDepth\";i:8;s:9:\"colorType\";s:10:\"truecolour\";s:8:\"metadata\";a:4:{s:11:\"XResolution\";s:8:\"3779/100\";s:11:\"YResolution\";s:8:\"3779/100\";s:14:\"ResolutionUnit\";i:3;s:15:\"_MW_PNG_VERSION\";i:1;}}',8,'BITMAP','image','png','Screenshot of IPA rendering, showing problems with tie bars and letters being raised/lowered. File can be deleted after problem is resolved.',444485,'-sche','20120312203359','jtb43bvxce1p3qx0rxxic7zz4ce1wti'),('khw-superscript.jpg',24412,555,115,'a:1:{s:22:\"MEDIAWIKI_EXIF_VERSION\";i:2;}',8,'BITMAP','image','jpeg','page 20 of \'\'Modern Cantonese phonology\'\' by Robert S. Bauer and Paul K. Benedict (1997): \"The labialized-velar initials kw- [kʷ] and khw- [kʰʷ] have been\" (to be used to illustrate modifier letters, in a vote) (fair use of a small, likely unrecognizab',444485,'-sche','20120219224006','o6ezmc7nv97t9etc77hezawad1y6efy'),('wiktprob.png',9920,819,591,'a:3:{s:10:\"frameCount\";i:0;s:9:\"loopCount\";i:1;s:8:\"duration\";d:0;}',8,'BITMAP','image','png','',55840,'Liliana-60','20110407125545','10mo18onawhk84ndg5ll7jv01yjqccr');
/*!40000 ALTER TABLE `image` ENABLE KEYS */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2013-03-13  1:45:09
