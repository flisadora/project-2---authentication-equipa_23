-- -------------------------------------------------------------
-- TablePlus 4.5.0(396)
--
-- https://tableplus.com/
--
-- Database: sio
-- Generation Time: 2021-11-03 19:30:38.4310
-- -------------------------------------------------------------


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

CREATE DATABASE IF NOT EXISTS HPWiki;

USE HPWiki;

CREATE TABLE `characters` (
  `name` varchar(100) NOT NULL,
  `photo` blob NOT NULL,
  `born` date NOT NULL,
  `blood_status` varchar(20) NOT NULL,
  `marital_status` varchar(20) NOT NULL,
  `nationality` varchar(20) NOT NULL,
  `species` varchar(20) NOT NULL,
  `gender` varchar(20) NOT NULL,
  `height` varchar(10) NOT NULL,
  `weight` varchar(10) NOT NULL,
  `boggart` varchar(20) DEFAULT NULL,
  `wand` varchar(100) DEFAULT NULL,
  `patronus` varchar(50) DEFAULT NULL,
  `occupation` varchar(200) NOT NULL,
  `house` varchar(20) DEFAULT NULL,
  `biography` varchar(12000) NOT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura da tabela `users`
--

CREATE TABLE `users` (
  `name` varchar(100) NOT NULL,
  `nickname` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `role` tinyint(1) NOT NULL,
  PRIMARY KEY (`nickname`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura da tabela `comments`
--

CREATE TABLE `comments` (
  `nickname` varchar(50) NOT NULL,
  `comm_date` datetime NOT NULL,
  `text` varchar(1000) NOT NULL,
  `charactere` varchar(100) NOT NULL,
  PRIMARY KEY (`nickname`,`comm_date`),
  KEY `charactere` (`charactere`),
  CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`charactere`) REFERENCES `characters` (`name`),
  CONSTRAINT `comments_ibfk_2` FOREIGN KEY (`nickname`) REFERENCES `users` (`nickname`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


--
-- Índices para tabelas despejadas
--


--
-- Restrições para despejos de tabelas
--


--
-- Inserção de dados nas tabelas
--

INSERT INTO `characters` (`name`, `photo`, `born`, `blood_status`, `marital_status`, `nationality`, `species`, `gender`, `height`, `weight`, `boggart`, `wand`, `patronus`, `occupation`, `house`, `biography`) VALUES
('Harry James Potter', 'https://static.wikia.nocookie.net/harrypotter/images/9/97/Harry_Potter.jpg', '1980-07-31', 'Half-Blood', 'Married', 'English', 'Human', 'Male', '164 cm', '65', 'Dementor', '11\", Holly, Phoenix Feather', 'Stag', 'Head of the Department of Magical Law Enforcement', 'Gryffindor', 'Harry James Potter was born on 31 July 1980, at Godric\'s Hollow in the West Country, England, only hours after his classmate-to-be Neville Longbottom. Around this time, a prophecy regarding a boy born at the end of July with the power to defeat Voldemort was stated to wizards. Harry\'s christening was quiet and quick, with only mother, father, and Sirius Black in attendance. Harry spent his infancy in hiding with his parents in the Potter cottage.\nFor Harry\'s first birthday, Sirius bought him a toy broomstick. In Lily\'s letter to Sirius, it mentioned that this broomstick had been Harry\'s favourite present and that he had smashed a horrible vase that had been a gift from Petunia and nearly killed their cat. In the letter, Lily also included a picture of Harry flying around on the broom and James chasing after him. Lily also stated in the letter that Harry looked pleased with himself while flying around on the toy broom. Lily and James also hosted a very quiet birthday tea. The only ones in attendance were them, Harry, and Bathilda Bagshot also used to dote on infant Harry. The Potters owned a cat, but it is unknown what happened to it after Voldemort\'s attack.\nWhen it became clear that Voldemort marked the Potters for death in regards to the prophecy, Albus Dumbledore suggested they use the Fidelius Charm to keep them safe. He even offered to be the Potter\'s Secret Keeper, but the Potters had planned to make Sirius their Secret Keeper instead. On Sirius\' advice, they changed this designation to Peter Pettigrew, who they thought would be less suspicious. In a terrible turn of fate, Pettigrew was a Death Eater spy, and barely a week later betrayed the Potter\'s whereabouts.'),
('Hermione Jean Granger', 'https://static.wikia.nocookie.net/harrypotter/images/3/34/Hermione_Granger.jpg', '1979-09-19', 'Muggle-Born', 'Married', 'English', 'Human', 'Female', '152 cm', '118', 'Failure', '10\", vine wood, dragon heartstring', 'Otter', 'Minister of Magic', 'Gryffindor', 'Hermione was born to Mr. and Mrs Granger on 19 September 1979. She was their only child and, although they were \"a bit bemused\" by the oddities displayed by their daughter, they were known to be proud of her.\nUpon turning eleven, Hermione was happily surprised to learn that she was a witch and was therefore invited to attend Hogwarts. She eagerly accepted and took to studying magic even before she began her first year at Hogwarts in the September of 1991, learning all the set spellbooks by heart and even managing to perform \"a few spells\" successfully. In addition to the texts set by the school, Hermione brought with her several other books for reference and to further her understanding of the wizarding world, to the point that she had looked at books and had more knowledge of the wizarding world than some of her pure-blood/half-blood classmates.'),
('Ronald Bilius Weasley', 'https://static.wikia.nocookie.net/harrypotter/images/8/85/Ron_Weasley.jpg', '1980-03-01', 'Pure-Blood', 'Married', 'English', 'Human', 'Male', '171 cm', '75', 'Aragog', '12\", Ash, unicorn tail hair', 'Jack Russel Terrier', 'Auror', 'Gryffindor', 'Ronald Bilius Weasley was born 1 March, 1980, to Arthur and Molly Weasley (née Prewett), at the height of the First Wizarding War. During this war his maternal uncles Fabian and Gideon Prewett, both members of the Order of the Phoenix, were murdered while fighting a group of four Death Eaters led by Antonin Dolohov. While he was still a toddler, the war ended for a time after Lord Voldemort\'s first defeat at the hands of Ron\'s classmate-to-be Harry Potter on 31 October, 1981.\n\nRon and his five older brothers — Bill, Charlie, Percy, Fred and George — as well as his younger sister, Ginny, grew up in The Burrow on the outskirts of Ottery St Catchpole in Devon, England. Like all his siblings, he was home educated in reading, writing and simple mathematics by his mother. The Weasley family was not wealthy at all, compared to other wizarding families. Many other pure-blood families, particularly the Malfoys, disdained them for their \"blood traitor\" beliefs and lack of wealth. They tried their best to make up for this with their love.\n\nThe Weasley siblings, especially Fred and George, were fond of teasing and playing pranks on each other, and Ron was a particular target for Fred and George. They once transfigured Ron\'s teddy bear into a giant spider, sparking his arachnophobia. On another occasion, the twins nearly got him to make an Unbreakable Vow, which finally made their father truly furious (and Fred would later state that his left buttock has \"never been the same since\" after the row that ensued). They also once got him to eat an Acid Pop which burnt a hole through his tongue.\n\nWhen Ron was younger, he had a pet rat named Scabbers, whom he had inherited from Percy. This rat was actually Peter Pettigrew, a traitor to all wizardkind. Ron was very fond of Scabbers, but wasn\'t sad to let him go when he found out the truth about his old rat. Ron had a fairly happy childhood, which Harry, who had been brought up by his spiteful relatives the Dursleys, envied. To compensate for their impoverishment, Ron\'s mother indulged him in three delicious meals daily. This became so habitual that missing a meal in later life would irritate Ron.');

INSERT INTO `users` (`name`, `nickname`, `email`, `password`, `role`) VALUES
('isabel', 'bella.4', 'isabella@hotmail.com', 'a4a2d4153f5bf93107c23e2750f11336', 0),
('joao', 'johny_03', 'john@gmail.com', '5788a97c728c710956e3d1f87c8429d4 	', 0),
('Liliana', 'lilimarta74', 'lili_martinha@gmail.com', 'e5862159d8c557f89a580e072b096f45', 1);

INSERT INTO `comments` (`nickname`, `comm_date`, `text`, `charactere`) VALUES
('bella.4', '2012-09-22 12:03:15', 'I didn\'t know she had become Minister of Magic :O', 'Hermione Jean Granger'),
('johny_03', '2013-01-14 22:53:25', 'Do you remember when Ron had to vomit all those slugs LMAO', 'Ronald Bilius Weasley'),
('lilimarta74', '2012-09-15 01:05:19', 'Hermione really was the best of her age <3', 'Hermione Jean Granger');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;