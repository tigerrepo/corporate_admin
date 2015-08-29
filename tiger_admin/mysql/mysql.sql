BEGIN;
CREATE TABLE `account_tab` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `username` varchar(32) NOT NULL,
    `email` varchar(32) NOT NULL UNIQUE,
    `password` varchar(64) NOT NULL,
    `salt` varchar(32) NOT NULL,
    `status` smallint NOT NULL,
    `create_time` datetime NOT NULL,
    `account_type` smallint NOT NULL
)
;
CREATE TABLE `customer_tab` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(32) NOT NULL,
    `slogan` varchar(128) NOT NULL,
    `url` varchar(64) NOT NULL UNIQUE,
    `description` varchar(256) NOT NULL,
    `create_time` datetime NOT NULL,
    `valid_from` datetime NOT NULL,
    `valid_to` datetime NOT NULL,
    `status` smallint NOT NULL,
    `account_id` integer NOT NULL
)
;
ALTER TABLE `customer_tab` ADD CONSTRAINT `account_id_refs_id_17f03907` FOREIGN KEY (`account_id`) REFERENCES `account_tab` (`id`);
CREATE TABLE `video_tab` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(32) NOT NULL,
    `description` varchar(128) NOT NULL,
    `video_url` varchar(256) NOT NULL,
    `host_url` varchar(128) NOT NULL,
    `company_id` integer NOT NULL
)
;
ALTER TABLE `video_tab` ADD CONSTRAINT `company_id_refs_id_bfdc7238` FOREIGN KEY (`company_id`) REFERENCES `customer_tab` (`id`);
CREATE INDEX `customer_tab_93025c2f` ON `customer_tab` (`account_id`);
CREATE INDEX `video_tab_0316dde1` ON `video_tab` (`company_id`);

COMMIT;
