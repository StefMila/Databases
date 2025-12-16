-- ==========================================
-- SQL DDL Statements
-- Painters & Paintings Database
-- ==========================================

-- ==========================================
-- RESET (Drop tables in reverse order of dependency)
-- ==========================================
DROP TABLE IF EXISTS visitable;
DROP TABLE IF EXISTS painted;
DROP TABLE IF EXISTS painting;
DROP TABLE IF EXISTS artist;
DROP TABLE IF EXISTS city;
DROP TABLE IF EXISTS country;

-- ==========================================
-- CREATE Tables (in order of dependency)
-- ==========================================

-- Country entity
CREATE TABLE country (
    iso CHAR(2) PRIMARY KEY,  
    country_name VARCHAR(100) NOT NULL,
    CONSTRAINT check_iso_uppercase CHECK (iso = UPPER(iso))
);

-- City entity (dependent on Country) - ID-dependency
CREATE TABLE city (
    country_iso CHAR(2) NOT NULL,
    zipcode VARCHAR(10) NOT NULL,
    name VARCHAR(100) NOT NULL,
    PRIMARY KEY (country_iso, zipcode),
    CONSTRAINT fk_city_country FOREIGN KEY (country_iso) REFERENCES country(iso) ON DELETE RESTRICT,
    CONSTRAINT check_zipcode_format CHECK (LENGTH(zipcode) > 0)
);

-- Artist (Painter) entity
CREATE TABLE artist (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    birth_year INTEGER,
    death_year INTEGER,
    CONSTRAINT check_artist_name CHECK (LENGTH(first_name) > 0 AND LENGTH(last_name) > 0),
    CONSTRAINT check_years CHECK (death_year IS NULL OR death_year >= birth_year)
);

-- Painting entity (independent)
CREATE TABLE painting (
    serial_number SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    style_type VARCHAR(50) NOT NULL,
    year_created INTEGER,
    wikipedia_url VARCHAR(500),
    CONSTRAINT check_title CHECK (LENGTH(title) > 0),
    CONSTRAINT check_style CHECK (LENGTH(style_type) > 0),
    CONSTRAINT check_year_created CHECK (year_created IS NULL OR (year_created > 1000 AND year_created <= EXTRACT(YEAR FROM CURRENT_DATE)))
);

-- Painted relationship (Artist 1:M Painting)
CREATE TABLE painted (
    artist_id INTEGER NOT NULL,
    painting_serial_number INTEGER NOT NULL,
    PRIMARY KEY (artist_id, painting_serial_number),
    CONSTRAINT fk_painted_artist FOREIGN KEY (artist_id) REFERENCES artist(id) ON DELETE RESTRICT,
    CONSTRAINT fk_painted_painting FOREIGN KEY (painting_serial_number) REFERENCES painting(serial_number) ON DELETE CASCADE
);

-- Visitable relationship (City 1:M Painting)
CREATE TABLE visitable (
    city_country_iso CHAR(2) NOT NULL,
    city_zipcode VARCHAR(10) NOT NULL,
    painting_serial_number INTEGER NOT NULL,
    PRIMARY KEY (city_country_iso, city_zipcode, painting_serial_number),
    CONSTRAINT fk_visitable_city FOREIGN KEY (city_country_iso, city_zipcode) REFERENCES city(country_iso, zipcode) ON DELETE RESTRICT,
    CONSTRAINT fk_visitable_painting FOREIGN KEY (painting_serial_number) REFERENCES painting(serial_number) ON DELETE CASCADE
);
