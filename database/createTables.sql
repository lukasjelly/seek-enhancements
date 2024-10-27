use seek;

-- Table: Advertisers
CREATE TABLE `Advertiser` (
    `advertiser_Id` INT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    `is_verified` TINYINT(1) NULL,
    `registration_date` DATETIME NULL,
    `date_added` DATETIME NULL
);

-- Table: Classification
CREATE TABLE `Classification` (
    `classification_Id` INT PRIMARY KEY,
    `label` VARCHAR(255) NOT NULL
);

-- Table: SubClassification
CREATE TABLE `SubClassification` (
    `subClassification_Id` INT PRIMARY KEY,
    `classification_id` INT NOT NULL,
    `label` VARCHAR(255) NOT NULL,
    FOREIGN KEY (`classification_id`) REFERENCES `Classification`(`classification_Id`)
);

-- Table: Location
CREATE TABLE `Location` (
    `location_Id` INT PRIMARY KEY,
    `area` VARCHAR(255) NULL,
    `location` VARCHAR(255) NULL
);

-- Table: WorkType
CREATE TABLE `WorkType` (
    `work_type_id` INT PRIMARY KEY,
    `label` VARCHAR(255) NOT NULL
);

-- Table: Job
CREATE TABLE `Job` (
    `job_Id` INT PRIMARY KEY NOT NULL,
    `advertiser_Id` INT NOT NULL,
    `classification_Id` INT NOT NULL,
    `subClassification_Id` INT NOT NULL,
    `work_type_id` INT NOT NULL,
    `title` VARCHAR(255) NULL,
    `phone_number` VARCHAR(20) NULL,
    `is_expired` TINYINT(1) NULL,
    `expires_at` DATETIME NULL,
    `is_link_out` TINYINT(1) NULL,
    `is_verified` TINYINT(1) NULL,
    `abstract` TEXT NULL,
    `content` TEXT NULL,
    `status` VARCHAR(50) NULL,
    `listed_at` DATETIME NULL,
    `salary` VARCHAR(255) NULL,
    `share_link` VARCHAR(255) NULL,
    `date_added` DATETIME NULL,
    `bullets` TEXT NULL,
    `questions` TEXT NULL,
    FOREIGN KEY (`advertiser_Id`) REFERENCES `Advertiser`(`advertiser_Id`)
);

-- Table: JobLocation
CREATE TABLE `JobLocation` (
    `job_location_id` INT PRIMARY KEY,
    `job_id` INT NOT NULL,
    `location_id` INT NOT NULL,
    FOREIGN KEY (`job_id`) REFERENCES `Job`(`job_Id`),
    FOREIGN KEY (`location_id`) REFERENCES `Location`(`location_Id`)
);