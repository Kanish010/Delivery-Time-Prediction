import pandas as pd
import mysql.connector

# MySQL database connection details
host = 'your_host'
user = 'your_username'
password = 'password'
database = 'SupplyChainDB'

# Path to your CSV file
csv_file_path = 'your/file/path'

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

        # Insert DataFrame records into MySQL database
        for i, row in df.iterrows():
            # Construct the SQL INSERT query
            sql = "INSERT INTO SupplyChainData (ProductID, Date, SalesVolume, Price, Promotion, Category, Brand, SeasonalityFactor, CompetitorPresence, WeatherCondition, InventoryLevel, LeadTime_days, DemandForecast_units, EOQ_units, UnitCost, SupplierID, OrderDate, DeliveryDate, OrderQuantity_units, TransportationMode, SupplierLocation, OrderUrgency, OrderType, GeopoliticalRisk, NaturalDisasterRisk, MarketVolatilityRisk, SupplierReliability) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            # Extract the values from the row
            values = (row['ProductID'], row['Date'], row['SalesVolume'], row['Price'], row['Promotion'], 
                      row['Category'], row['Brand'], row['SeasonalityFactor'], row['CompetitorPresence'], 
                      row['WeatherCondition'], row['InventoryLevel'], row['LeadTime_days'], row['DemandForecast_units'], 
                      row['EOQ_units'], row['UnitCost'], row['SupplierID'], row['OrderDate'], row['DeliveryDate'], row['OrderQuantity_units'], 
                      row['TransportationMode'], row['SupplierLocation'], row['OrderUrgency'], row['OrderType'], row['GeopoliticalRisk'], 
                      row['NaturalDisasterRisk'], row['MarketVolatilityRisk'], row['SupplierReliability'])
            # Execute the SQL query
            cursor.execute(sql, values)

        # Commit changes and close connection
        connection.commit()
        cursor.close()
        print("Data uploaded successfully to MySQL database.")

except mysql.connector.Error as e:
    print("Error while connecting to MySQL", e)

finally:
    if connection.is_connected():
        connection.close()
