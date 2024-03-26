-- Create the database
CREATE DATABASE SupplyChainDB;

-- Switch to the newly created database
USE SupplyChainDB;

-- Create the Products table
CREATE TABLE SupplyChainData (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    ProductID INT,
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
    SupplierLocation VARCHAR(50),
    OrderUrgency INT,
    OrderType VARCHAR(20),
    GeopoliticalRisk VARCHAR(10),
    NaturalDisasterRisk VARCHAR(10),
    MarketVolatilityRisk VARCHAR(10),
    SupplierReliability VARCHAR(10)
);
