import pandas as pd
import mysql.connector

# MySQL database connection details
host = 'localhost'
user = 'your_username'
password = 'your_password'
database = 'SupplyChainDB'

# Path to your CSV file on desktop
csv_file_path = '/path/to/your/desktop/SupplyChain_data.csv'

try:
    # Connect to the MySQL database
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    if connection.is_connected():
        cursor = connection.cursor()

        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file_path)

        # Remove ProductID from DataFrame
        df = df.drop(columns=['ProductID'])

        # Insert DataFrame records into MySQL database
        for i, row in df.iterrows():
            sql = "INSERT INTO Products (Date, SalesVolume, Price, Promotion, Category, Brand, SeasonalityFactor, CompetitorPresence, WeatherCondition, InventoryLevel, LeadTime_days, DemandForecast_units, EOQ_units, UnitCost, SupplierID, OrderDate, DeliveryDate, OrderQuantity_units, TransportationMode, SupplierLocation, OrderUrgency, OrderType, GeopoliticalRisk, NaturalDisasterRisk, MarketVolatilityRisk, SupplierReliability) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, tuple(row))

        # Commit changes and close connection
        connection.commit()
        cursor.close()
        print("Data uploaded successfully to MySQL database.")

except mysql.connector.Error as e:
    print("Error while connecting to MySQL", e)

finally:
    if connection.is_connected():
        connection.close()
