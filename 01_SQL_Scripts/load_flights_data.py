import pandas as pd
from sqlalchemy import create_engine, text
import mysql.connector
import time 
from contextlib import closing
from typing import List

# --- 1. CONFIGURATION ---
MYSQL_PASSWORD = "Password"
DB_NAME = "Airline_Performance_Analysis"
CSV_FILE_PATH = r"C:\Users\hp\OneDrive\Desktop\Labmentix\Project 2\Final_project_data_archive/flights.csv"
CHUNK_SIZE = 50000 


# --- Helper Function to manage Constraints ---

def get_foreign_key_names(connection, table_name: str, db_name: str) -> List[str]:
    """Retrieves the names of all foreign key constraints on the specified table."""
    query = f"""
    SELECT CONSTRAINT_NAME 
    FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
    WHERE TABLE_SCHEMA = '{db_name}' 
    AND TABLE_NAME = '{table_name}' 
    AND REFERENCED_TABLE_NAME IS NOT NULL;
    """
    result = connection.execute(text(query)).fetchall()
    return [row[0] for row in result]

def drop_foreign_keys(connection, table_name: str, db_name: str):
    """Drops all foreign key constraints from the specified table."""
    constraints = get_foreign_key_names(connection, table_name, db_name)
    if not constraints:
        print("    ➡️ No existing foreign key constraints found to drop.")
        return
    
    print(f"    ⚠️ Found and dropping {len(constraints)} foreign key constraints...")
    
    for name in constraints:
        drop_query = f"ALTER TABLE `{table_name}` DROP FOREIGN KEY `{name}`;"
        connection.execute(text(drop_query))
        print(f"    ✅ Dropped constraint: {name}")


def recreate_flights_table(connection):
    """Drops and recreates the flights table with corrected data types (VARCHAR(5) for airport/airline codes)."""
    
    print("\n--- Recreating 'flights' table with corrected column sizes ---")
    
    # 1. Drop existing table (to clear old data and constraints)
    drop_table_query = "DROP TABLE IF EXISTS `flights`;"
    connection.execute(text(drop_table_query))
    print("    ✅ Existing 'flights' table dropped.")

    # 2. Create the table with updated VARCHAR sizes (5 instead of 3)
    create_table_query = text("""
        CREATE TABLE flights (
            FLIGHT_ID 				INT AUTO_INCREMENT PRIMARY KEY,
            YEAR 					SMALLINT,
            MONTH 					TINYINT,
            DAY 					TINYINT,
            DAY_OF_WEEK 			TINYINT,
            AIRLINE 				VARCHAR(5),  -- CRITICAL CHANGE: Increased from 3 to 5
            FLIGHT_NUMBER 			VARCHAR(10),
            TAIL_NUMBER 			VARCHAR(10),
            ORIGIN_AIRPORT 			VARCHAR(5),  -- CRITICAL CHANGE: Increased from 3 to 5
            DESTINATION_AIRPORT 	VARCHAR(5),  -- CRITICAL CHANGE: Increased from 3 to 5
            SCHEDULED_DEPARTURE 	SMALLINT,
            DEPARTURE_TIME 			SMALLINT,
            DEPARTURE_DELAY 		SMALLINT,
            TAXI_OUT 				SMALLINT,
            WHEELS_OFF 				SMALLINT,
            SCHEDULED_TIME 			SMALLINT,
            ELAPSED_TIME 			SMALLINT,
            AIR_TIME 				SMALLINT,
            DISTANCE 				SMALLINT,
            WHEELS_ON 				SMALLINT,
            TAXI_IN 				SMALLINT,
            SCHEDULED_ARRIVAL 		SMALLINT,
            ARRIVAL_TIME 			SMALLINT,
            ARRIVAL_DELAY 			SMALLINT,
            DIVERTED 				BOOLEAN,
            CANCELLED 				BOOLEAN,
            CANCELLATION_REASON 	VARCHAR(1),
            AIR_SYSTEM_DELAY 		SMALLINT,
            SECURITY_DELAY 			SMALLINT,
            AIRLINE_DELAY 			SMALLINT,
            LATE_AIRCRAFT_DELAY 	SMALLINT,
            WEATHER_DELAY 			SMALLINT
            -- Note: Foreign Keys will NOT be added back to ensure smooth data loading.
        );
    """)
    connection.execute(create_table_query)
    print("    ✅ New 'flights' table created (VARCHAR(5) for codes).")


# --- 2. SQLALCHEMY ENGINE SETUP ---
DB_CONNECTION_STRING = f'mysql+mysqlconnector://root:{MYSQL_PASSWORD}@localhost:3306/{DB_NAME}'
try:
    engine = create_engine(DB_CONNECTION_STRING, echo=False, pool_pre_ping=True)
    print("✅ SQLAlchemy Engine created.")
except Exception as e:
    print(f"❌ SQLAlchemy Engine Error: {e}")
    exit()


# --- 3. CONNECTION TEST (No change needed) ---
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=MYSQL_PASSWORD,
        database=DB_NAME
    )
    print("✅ Connection Test: Successful!")
    conn.close()
except Exception as e:
    print(f"❌ Connection Error during test: {e}")
    exit()


# --- 4. CHUNKED DATA INGESTION (Modified to use a dedicated connection) ---
rows_processed = 0
start_time = time.time()
print(f"\n--- Starting bulk import of flights.csv (Chunk Size: {CHUNK_SIZE}) ---")

try:
    # Use a dedicated connection for the entire bulk import transaction
    with closing(engine.connect()) as connection:
        # Start a transaction block
        with connection.begin():
            print("\n--- Pre-Import Setup: Preparing Table and Disabling Checks ---")
            
            # Step 1: Recreate the table with the correct VARCHAR sizes
            recreate_flights_table(connection)

            # Step 2: Ensure checks are disabled (belt and suspenders approach)
            connection.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
            print("    ✅ Foreign Key Checks Disabled for Bulk Insert Transaction.")

            # Read CSV in chunks
            csv_iterator = pd.read_csv(
                CSV_FILE_PATH, 
                chunksize=CHUNK_SIZE, 
                encoding='utf-8', 
                low_memory=False
            )
            
            # Loop through each chunk and load it to the database using the active connection
            for chunk in csv_iterator:
                # Load the chunk into the 'flights' table using the transaction connection
                chunk.to_sql(
                    'flights', 
                    con=connection,
                    if_exists='append', 
                    index=False
                )
                
                rows_processed += len(chunk)
                # Progress update printed on the same line
                print(f"\r➡️ Inserted {rows_processed:,} rows...", end='', flush=True)

    # Final status update
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\n\n🎉 Success! All data loaded.")
    print(f"Total rows inserted: {rows_processed:,}")
    print(f"Time taken: {duration:.2f} seconds")

except FileNotFoundError:
    print(f"❌ Error: CSV file not found at path: {CSV_FILE_PATH}. Please check the file path.")
except Exception as e:
    # This catches errors during the to_sql operation
    print(f"\n❌ An error occurred during data ingestion: {e}")
    print("The final error indicates a data type problem, likely due to unexpected values in the CSV.")

finally:
    # --- 5. POST-IMPORT SETUP: RE-ENABLE FOREIGN KEY CHECKS (Best practice for cleanup) ---
    print("\n\n--- Post-Import Cleanup: Re-enabling Foreign Key Checks ---")
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=MYSQL_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
        # Ensure checks are enabled globally after the operation finishes
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Foreign Key Checks Re-enabled. Database integrity restored.")
    except Exception as e:
        print(f"❌ Failed to re-enable foreign key checks (SET FOREIGN_KEY_CHECKS = 1;): {e}")
