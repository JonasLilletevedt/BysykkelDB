
import sqlite3
import csv

path_db = "bysykkel.db"
path_csv = "bysykkel.csv"
con = sqlite3.connect(path_db)
cur = con.cursor()

def get_tables():
    result = []
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()

    for t in tables:
        result.append(t[0])
    return result

def get_attributes_from_table(table):
    attributes = []
    cur.execute(f"SELECT * FROM {table} LIMIT 1;")
    for attribute in cur.description:
        attributes.append(attribute[0])
    return attributes

def convert_to_string(value):
    return str(value)

def formatter(attributes):
    streng = ""
    for attribute in attributes:
         streng += f"\"{attribute}\"" + ","
    return streng[:-1]

def read_CSV():
    with open(path_csv, "r") as f:
        reader = csv.reader(f)
        return list(reader)
    
# Returns a tuple
# [0] for attributes
# [1] for values
def get_all_values_in_row(index, attributes):
    values = []
    nyeAt= []
    head = read_CSV()
    i = 1
    for i in range(0,len(head[0])):
        if head[0][i] in attributes:
            nyeAt.append(head[0][i])
            values.append(head[index][i])
    return tuple((nyeAt,values))

def get_rows():
    head = read_CSV()
    count = 0
    for line in head:
        count += 1
    return count




def insert_to_table(table):
    columns = get_attributes_from_table(table)
    columns = formatter(columns)

    size = get_rows()
    row_index = 1
    while row_index < size:
        try:
            # List of attributes to be inserted
            attributes_to_be_inserted = get_all_values_in_row(row_index, get_attributes_from_table(f"{table}"))[0]
            # Change to correct format for insertion
            attributes_to_be_inserted = formatter(attributes_to_be_inserted)
            # List of attributes to be inserted
            values_to_be_inserted = get_all_values_in_row(row_index, get_attributes_from_table(f"{table}"))[1]
            # Change to correct format for insertion
            values_to_be_inserted =formatter(values_to_be_inserted)

            print(f"INSERT INTO {table} ({attributes_to_be_inserted}) VALUES({values_to_be_inserted})")
            cur.execute(f"INSERT INTO {table} ({attributes_to_be_inserted}) VALUES({values_to_be_inserted})")

            con.commit()
        except:
            pass
        row_index += 1

def insert_to_all_tables():
    tables = get_tables()
    for t in tables:
        insert_to_table(f"\"{t}\"")

insert_to_all_tables()

#insert_to_table("start_station")

