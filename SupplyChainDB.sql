-- Create the database
CREATE DATABASE IF NOT EXISTS SupplyChainDB;

-- Switch to the newly created database
USE SupplyChainDB;

-- Create the Products table
CREATE TABLE IF NOT EXISTS SupplyChainData (
    EntryID INT AUTO_INCREMENT PRIMARY KEY,
    ProductID VARCHAR(36),
    Date DATE,
    SalesVolume INT,
    Price DECIMAL(8, 2),
    Promotion BOOLEAN,
    Category VARCHAR(50),
    Brand VARCHAR(50),
    SeasonalityFactor BOOLEAN,
    CompetitorPresence BOOLEAN,
    WeatherCondition VARCHAR(50),
    InventoryLevel INT,
    LeadTime_days INT,
    DemandForecast_units INT,
    EOQ_units INT,
    UnitCost DECIMAL(8, 2),
    SupplierID INT,
    OrderDate DATE,
    DeliveryDate DATE,
    OrderQuantity_units INT,
    TransportationMode VARCHAR(20),
    SupplierLocation VARCHAR(250),
    OrderUrgency INT,
    OrderType VARCHAR(20),
    GeopoliticalRisk VARCHAR(250),
    NaturalDisasterRisk VARCHAR(250),
    MarketVolatilityRisk VARCHAR(250),
    SupplierReliability VARCHAR(100)
);
