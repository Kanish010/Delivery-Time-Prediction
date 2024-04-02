-- Create the database
CREATE DATABASE IF NOT EXISTS SupplyChainDB;

-- Switch to the newly created database
USE SupplyChainDB;

CREATE TABLE DemandForecasting (
    ProductID VARCHAR(50) PRIMARY KEY,
    Date DATE,
    SalesVolume INT,
    Price DECIMAL(8, 2),
    Promotion TINYINT,
    Category VARCHAR(20),
    Brand VARCHAR(20),
    SeasonalityFactor TINYINT,
    CompetitorPresence TINYINT,
    WeatherCondition VARCHAR(10)
);

CREATE TABLE InventoryOptimization (
    InventoryLevel INT,
    LeadTime_days INT,
    DemandForecast_units INT,
    EOQ_units INT,
    UnitCost DECIMAL(8, 2),
    ReorderPoint_units INT,
    ReorderQuantity_units INT
);

CREATE TABLE LeadTimePrediction (
    ProductID VARCHAR(50),
    SupplierID VARCHAR(50),
    OrderDate DATE,
    DeliveryDate DATE,
    OrderQuantity_units INT,
    TransportationMode VARCHAR(10),
    SupplierLocation VARCHAR(50),
    OrderUrgency INT,
    OrderType VARCHAR(10),
    PRIMARY KEY (ProductID),
    FOREIGN KEY (ProductID) REFERENCES DemandForecasting(ProductID)
    PRIMARY KEY (SupplierID),
    FOREIGN KEY (SupplierID) REFERENCES Supplier(SupplierID)
);

CREATE TABLE RiskManagement (
    SupplierID VARCHAR(50),
    GeopoliticalRisk VARCHAR(10),
    NaturalDisasterRisk VARCHAR(10),
    MarketVolatilityRisk VARCHAR(10),
    SupplierReliability VARCHAR(10),
    OrderLeadTime_days INT,
    InventoryLevel INT,
    PRIMARY KEY (SupplierID),
    FOREIGN KEY (SupplierID) REFERENCES Supplier(SupplierID)
);
