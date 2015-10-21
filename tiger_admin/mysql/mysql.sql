BEGIN;
CREATE TABLE `account_tab` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `username` varchar(32) NOT NULL UNIQUE,
    `email` varchar(32) NOT NULL UNIQUE,
    `password` varchar(64) NOT NULL,
    `salt` varchar(32) NOT NULL,
    `status` smallint NOT NULL,
    `create_time` datetime NOT NULL,
    `account_type` smallint NOT NULL
)
;
CREATE TABLE `company_tab` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(32) NOT NULL UNIQUE,
    `slogan` varchar(128) NOT NULL,
    `url` varchar(64) NOT NULL UNIQUE,
    `description` varchar(256) NOT NULL,
    `create_time` datetime NOT NULL,
    `valid_from` datetime NOT NULL,
    `valid_to` datetime NOT NULL,
    `status` smallint NOT NULL,
    `account_id` integer NOT NULL,
    `pdf_url` varchar(64) NOT NULL DEFAULT ''
)
;
ALTER TABLE `company_tab` ADD CONSTRAINT `account_id_refs_id_002207d9` FOREIGN KEY (`account_id`) REFERENCES `account_tab` (`id`);
CREATE TABLE `video_tab` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(32) NOT NULL,
    `description` varchar(128) NOT NULL,
    `video_url` varchar(256) NOT NULL,
    `host_url` varchar(128) NOT NULL,
    `company_id` integer NOT NULL
)
;
ALTER TABLE `video_tab` ADD CONSTRAINT `company_id_refs_id_8a4e4a68` FOREIGN KEY (`company_id`) REFERENCES `company_tab` (`id`);
CREATE TABLE `contact_tab` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `sender` varchar(32) NOT NULL,
    `mobile` varchar(20) NOT NULL,
    `email` varchar(64) NOT NULL,
    `title` varchar(64) NOT NULL,
    `content` varchar(512) NOT NULL,
    `create_date` datetime NOT NULL,
    `company_id` integer NOT NULL
)
;
ALTER TABLE `contact_tab` ADD CONSTRAINT `company_id_refs_id_71463fd0` FOREIGN KEY (`company_id`) REFERENCES `company_tab` (`id`);
CREATE TABLE `tag_tab` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(32) NOT NULL UNIQUE,
    `status` smallint NOT NULL
)
;
CREATE TABLE `company_tag_tab` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `company_id` integer NOT NULL,
    `tag_id` integer NOT NULL,
    UNIQUE (`company_id`, `tag_id`)
)
;
ALTER TABLE `company_tag_tab` ADD CONSTRAINT `company_id_refs_id_799e30ea` FOREIGN KEY (`company_id`) REFERENCES `company_tab` (`id`);
ALTER TABLE `company_tag_tab` ADD CONSTRAINT `tag_id_refs_id_88fd8dfe` FOREIGN KEY (`tag_id`) REFERENCES `tag_tab` (`id`);
CREATE TABLE `product_tab` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `company_id` integer NOT NULL,
    `name` varchar(64) NOT NULL,
    `description` varchar(512) NOT NULL,
    `create_date` datetime NOT NULL,
    `status` smallint NOT NULL,
    UNIQUE (`company_id`, `name`)
)
;
ALTER TABLE `product_tab` ADD CONSTRAINT `company_id_refs_id_f5094944` FOREIGN KEY (`company_id`) REFERENCES `company_tab` (`id`);
CREATE TABLE `gallery_tab` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(64) NOT NULL,
    `image_url` varchar(64) NOT NULL,
    `is_cover` bool NOT NULL,
    `product_id` integer NOT NULL,
    UNIQUE (`name`, `product_id`)
)
;
ALTER TABLE `gallery_tab` ADD CONSTRAINT `product_id_refs_id_c112db26` FOREIGN KEY (`product_id`) REFERENCES `product_tab` (`id`);
CREATE INDEX `company_tab_93025c2f` ON `company_tab` (`account_id`);
CREATE INDEX `video_tab_0316dde1` ON `video_tab` (`company_id`);
CREATE INDEX `contact_tab_0316dde1` ON `contact_tab` (`company_id`);
CREATE INDEX `company_tag_tab_0316dde1` ON `company_tag_tab` (`company_id`);
CREATE INDEX `company_tag_tab_5659cca2` ON `company_tag_tab` (`tag_id`);
CREATE INDEX `product_tab_0316dde1` ON `product_tab` (`company_id`);
CREATE INDEX `gallery_tab_7f1b40ad` ON `gallery_tab` (`product_id`);

COMMIT;
