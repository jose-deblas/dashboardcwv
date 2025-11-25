-- Create database and tables for Core Web Vitals
-- This file is executed by MySQL container initialization when the database is empty

CREATE DATABASE IF NOT EXISTS `core_web_vitals` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `core_web_vitals`;

-- Table to store URLs
CREATE TABLE IF NOT EXISTS `urls` (
  `url_id` INT AUTO_INCREMENT PRIMARY KEY,
  `url` VARCHAR(2048) NOT NULL,
  `device` VARCHAR(10) NOT NULL,
  `page_type` VARCHAR(50) NOT NULL,
  `brand` VARCHAR(50) NOT NULL,
  `category` VARCHAR(10) NOT NULL,
  `country_id` VARCHAR(10) NOT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  INDEX `idx_url` (`url`(191)),
  INDEX (`brand`),
  INDEX (`category`),
  INDEX (`country_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table to store Core Web Vitals measurements
CREATE TABLE IF NOT EXISTS `url_core_web_vitals` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `url_id` INT NOT NULL,
  `execution_date` DATE NOT NULL,
  `performance_score` DOUBLE DEFAULT NULL,
  `first_contentful_paint` DOUBLE DEFAULT NULL,
  `largest_contentful_paint` DOUBLE DEFAULT NULL,
  `total_blocking_time` DOUBLE DEFAULT NULL,
  `cumulative_layout_shift` DOUBLE DEFAULT NULL,
  `speed_index` DOUBLE DEFAULT NULL,
  `time_to_first_byte` DOUBLE DEFAULT NULL,
  `time_to_interactive` DOUBLE DEFAULT NULL,
  `crux_largest_contentful_paint` DOUBLE DEFAULT NULL,
  `crux_interaction_to_next_paint` DOUBLE DEFAULT NULL,
  `crux_cumulative_layout_shift` DOUBLE DEFAULT NULL,
  `crux_first_contentful_paint` DOUBLE DEFAULT NULL,
  `crux_time_to_first_byte` DOUBLE DEFAULT NULL,
  FOREIGN KEY (`url_id`) REFERENCES `urls`(`url_id`) ON DELETE CASCADE,
  INDEX (`execution_date`),
  UNIQUE KEY `unique_url_execution` (`url_id`, `execution_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table to store milestone dates for tracking progress
CREATE TABLE IF NOT EXISTS `milestones` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `milestone_date` DATE NOT NULL,
  `milestone_name` VARCHAR(100) NOT NULL,
  `description` VARCHAR(255) NOT NULL,
  `team_id` INT NOT NULL,
  `country_id` VARCHAR(10) NOT NULL,
  INDEX (`milestone_date`),
  INDEX (`team_id`),
  INDEX (`country_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table to store teams
CREATE TABLE IF NOT EXISTS `teams` (
  `team_id` INT AUTO_INCREMENT PRIMARY KEY,
  `team_name` VARCHAR(100) NOT NULL,
  `description` VARCHAR(255) DEFAULT NULL,
  UNIQUE KEY `unique_team_name` (`team_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table to store countries
CREATE TABLE IF NOT EXISTS `countries` (
  `country_id` VARCHAR(10) PRIMARY KEY,
  `country_name` VARCHAR(100) NOT NULL,
  UNIQUE KEY `unique_country_name` (`country_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table to store url_page_types
CREATE TABLE IF NOT EXISTS `url_page_types` (
  `page_type_id` INT AUTO_INCREMENT PRIMARY KEY,
  `page_type` VARCHAR(50) NOT NULL,
  UNIQUE KEY `unique_page_type` (`page_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table to store url_brands
CREATE TABLE IF NOT EXISTS `url_brands` (
  `brand_id` INT AUTO_INCREMENT PRIMARY KEY,
  `brand` VARCHAR(50) NOT NULL,
  `target_brand` BOOLEAN NOT NULL DEFAULT TRUE,
  UNIQUE KEY `unique_brand` (`brand`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table to store url_categories
CREATE TABLE IF NOT EXISTS `url_categories` (
  `category_id` INT AUTO_INCREMENT PRIMARY KEY,
  `category` VARCHAR(10) NOT NULL,
  UNIQUE KEY `unique_category` (`category`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

