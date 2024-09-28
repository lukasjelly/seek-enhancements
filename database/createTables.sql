-- Table: Advertisers
CREATE TABLE Advertisers (
    id INT PRIMARY KEY IDENTITY(1,1),
    name VARCHAR(255) NOT NULL,
    is_verified BIT NOT NULL,
    registration_date DATETIME NOT NULL
);

-- Table: Classifications
CREATE TABLE Classifications (
    classification_id INT PRIMARY KEY IDENTITY(1,1),
    label VARCHAR(255) NOT NULL
);

-- Table: SubClassifications
CREATE TABLE SubClassifications (
    subClassification_Id INT PRIMARY KEY IDENTITY(1,1),
    classification_id INT NOT NULL,
    label VARCHAR(255) NOT NULL,
    FOREIGN KEY (classification_id) REFERENCES Classifications(id)
);

-- Table: Jobs
CREATE TABLE Jobs (
    id INT PRIMARY KEY IDENTITY(1,1),
    title VARCHAR(255) NOT NULL,
    abstract TEXT NULL,
    content TEXT NULL,
    phone_number VARCHAR(20) NULL,
    is_expired BIT NOT NULL,
    expires_at DATETIME NULL,
    is_link_out BIT NOT NULL,
    is_verified BIT NOT NULL,
    status VARCHAR(50) NOT NULL,
    listed_at DATETIME NOT NULL,
    salary VARCHAR(255) NULL,
    share_link VARCHAR(255) NULL,
    advertiser_id INT,
    classification_id INT, -- FK to Classifications
    subclassification_id INT, -- FK to SubClassifications
    FOREIGN KEY (advertiser_id) REFERENCES Advertisers(id),
    FOREIGN KEY (classification_id) REFERENCES Classifications(id),
    FOREIGN KEY (subclassification_id) REFERENCES SubClassifications(id)
);

-- Table: JobLocations
CREATE TABLE JobLocations (
    id INT PRIMARY KEY IDENTITY(1,1),
    job_id INT NOT NULL,
    location_id INT NOT NULL,
    FOREIGN KEY (job_id) REFERENCES Jobs(id),
    FOREIGN KEY (location_id) REFERENCES Locations(id)
);

-- Table: JobTracking
CREATE TABLE JobTracking (
    id INT PRIMARY KEY IDENTITY(1,1),
    job_id INT NOT NULL,
    source_zone VARCHAR(50) NULL,
    ad_product_type VARCHAR(50) NULL,
    has_role_requirements BIT NULL,
    is_private_advertiser BIT NULL,
    work_type_ids VARCHAR(50) NULL,
    posted_time VARCHAR(50) NULL,
    FOREIGN KEY (job_id) REFERENCES Jobs(id)
);

-- Table: JobProducts
CREATE TABLE JobProducts (
    id INT PRIMARY KEY IDENTITY(1,1),
    job_id INT NOT NULL,
    branding_id INT NULL,
    video_url VARCHAR(255) NULL,
    FOREIGN KEY (job_id) REFERENCES Jobs(id),
    FOREIGN KEY (branding_id) REFERENCES ProductBranding(id)
);

-- Table: ProductBranding
CREATE TABLE ProductBranding (
    id INT PRIMARY KEY IDENTITY(1,1),
    cover_url VARCHAR(255) NULL,
    thumbnail_url VARCHAR(255) NULL,
    logo_url VARCHAR(255) NULL
);

-- Table: ProductBullets
CREATE TABLE ProductBullets (
    id INT PRIMARY KEY IDENTITY(1,1),
    product_id INT NOT NULL,
    bullet_point TEXT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES JobProducts(id)
);

-- Table: ProductQuestionnaire
CREATE TABLE ProductQuestionnaire (
    id INT PRIMARY KEY IDENTITY(1,1),
    product_id INT NOT NULL,
    question TEXT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES JobProducts(id)
);
