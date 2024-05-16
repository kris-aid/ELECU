import sqlite3
import pandas as pd

# Function to create a SQLite database and table
def create_database(database_name, table_name, column_names):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    # Construct the CREATE TABLE statement using the column names
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join([f'{name} TEXT' for name in column_names])})"
    c.execute(create_table_query)
    conn.commit()
    conn.close()

# Function to read the header row of the text file and extract column names
def get_column_names(text_file, encoding):
    df = pd.read_csv(text_file, sep='|', encoding=encoding, nrows=1)
    return df.columns.tolist()

# Function to read the text file and insert its contents into the database
def insert_data_from_textfile(database_name, table_name, text_file, column_names, encoding):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()

    with open(text_file, 'r', encoding=encoding) as file:
        # Skip the header row
        next(file)
        # Read lines from the text file and insert them into the table
        for line in file:
            # Split the line using "|" separator
            columns = line.strip().split("|")
            # Insert the columns into the table
            c.execute(f"INSERT INTO {table_name} VALUES ({', '.join(['?']*len(column_names))})", tuple(columns))
    
    conn.commit()
    conn.close()

#Crear indices en la tabla en base a los campos que se consideren necesarios
#Campos: NOMBRE, FECHA_NAC

def create_index(database_name, table_name):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    
    #c.execute(f"CREATE INDEX idx_nac_nombre on {table_name} (FECH_NAC, NOMBRES)")
    c.execute(f"CREATE INDEX idx_nac ON {table_name} (FECH_NAC)")
    c.execute(f"CREATE INDEX idx_nombre ON {table_name} (NOMBRES)")
   
    
    #delete the idx_nac_nombre index
    #c.execute(f"DROP INDEX idx_nac_nombre")
    conn.commit()
    conn.close()
    



# Main function
def main():
    database_name = 'cedulas.db'  # Name of the SQLite database
    table_name = 'cedulas_data'  # Name of the table
    text_file = 'CI_2019.txt'  # Path to your text file
    encoding = 'latin1'  # Encoding of the text file
    
    # Get column names from the text file
    column_names = get_column_names(text_file, encoding)
    
    # Create database and table
    create_database(database_name, table_name, column_names)
    
    # Insert data from text file into the database
    insert_data_from_textfile(database_name, table_name, text_file, column_names, encoding)
    
    create_index(database_name, table_name)

if __name__ == "__main__":
    main()
    #create_index('cedulas.db', 'cedulas_data')
    