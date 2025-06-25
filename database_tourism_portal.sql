-- Create database
CREATE DATABASE IF NOT EXISTS tourism_portal_fi;
USE tourism_portal_fi;

-- Table: users
CREATE TABLE IF NOT EXISTS users (
    name VARCHAR(20) UNIQUE,
    password VARCHAR(20),
    type VARCHAR(10)
);

-- Table: locations
CREATE TABLE IF NOT EXISTS locations (
    location_id INT UNIQUE,
    location VARCHAR(20) PRIMARY KEY
);

-- Table: transport
CREATE TABLE IF NOT EXISTS transport (
    transport VARCHAR(10),
    cost_per_km INT
);

-- Table: hotels
CREATE TABLE IF NOT EXISTS hotels (
    location VARCHAR(10),
    hotel VARCHAR(20),
    Cost_per_night INT,
    FOREIGN KEY (location) REFERENCES locations(location)
);

-- Table: spots
CREATE TABLE IF NOT EXISTS spots (
    location VARCHAR(10),
    spots VARCHAR(100),
    FOREIGN KEY (location) REFERENCES locations(location)
);

-- Table: details
CREATE TABLE IF NOT EXISTS details (
    no INT,
    cr VARCHAR(15),
    des VARCHAR(15),
    tp VARCHAR(15),
    t_cost INT,
    hotel VARCHAR(15),
    h_cost INT,
    gcost INT,
    total_cost INT
);
