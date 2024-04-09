import pandas as pd
import mysql.connector

# MySQL database connection details
host = 'localhost'
user = 'root'
password = 'password'
database = 'SupplyChainDB'

# File paths for CSV files
demand_forecasting_csv = '/path/to/DemandForecasting_data.csv'
inventory_optimization_csv = '/path/to/InventoryOptimization_data.csv'

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

        # Iterate through CSV files
        for csv_file, table_name in [(demand_forecasting_csv, 'DemandForecasting'), (inventory_optimization_csv, 'InventoryOptimization')]:
            # Read the CSV file into a DataFrame
            df = pd.read_csv(csv_file)

            # Insert DataFrame records into MySQL database
            for i, row in df.iterrows():
                # Construct the SQL INSERT query
                sql = f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES ({', '.join(['%s' for _ in range(len(df.columns))])})"
                # Extract the values from the row
                values = tuple(row)
                # Execute the SQL query
                cursor.execute(sql, values)

            # Commit changes after processing each CSV file
            connection.commit()

        cursor.close()
        print("Data uploaded successfully to MySQL database.")

except mysql.connector.Error as e:
    print("Error while connecting to MySQL", e)

finally:
    if connection.is_connected():
        connection.close()
