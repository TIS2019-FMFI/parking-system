import sqlite3
from Database import Database

connection = sqlite3.connect("kvant.db")
cursor = connection.cursor()


cursor.execute("DROP TABLE IF EXISTS records")
cursor.execute("DROP TABLE IF EXISTS companies")

# Table from companies
cursor.execute('''CREATE TABLE IF NOT EXISTS companies
                  (companyID INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT)''')

# Insert firiem, ktore uz existuje podla ID v configu
# DOROBIT !!!

# Table for records
cursor.execute('''CREATE TABLE IF NOT EXISTS records
                  (recordId INTEGER PRIMARY KEY AUTOINCREMENT,
                   ecv TEXT,
                   arrivalTime DATETIME DEFAULT CURRENT_TIMESTAMP,
                   departureTime DATETIME,
                   companyId INTEGER,
                   boxId INTEGER,
                   photoFileName TEXT,
                   status TEXT,
                   FOREIGN KEY (companyID) REFERENCES companies(companyID))''')

print("Tables created")

def fill_data(data):
    db=Database("kvant.db")
    for i in data:
        db.createCompany(i)
fill_data(['Lampy.sk', 'Malovanky', 'Kroksovo', 'Kosovo', 'Losovo','Lampy.sk', 'Malovanky', 'Kroksovo', 'Kosovo', 'Losovo','Lampy.sk', 'Malovanky', 'Kroksovo', 'Kosovo', 'Losovo','Lampy.sk', 'Malovanky', 'Kroksovo', 'Kosovo', 'Losovo','Lampy.sk', 'Malovanky', 'Kroksovo', 'Kosovo', 'Losovo','Lampy.sk', 'Malovanky', 'Kroksovo', 'Kosovo', 'Losovo','Lampy.sk', 'Malovanky', 'Kroksovo', 'Kosovo', 'Losovo','Lampy.sk', 'Malovanky', 'Kroksovo', 'Kosovo', 'Losovo','Lampy.sk', 'Malovanky', 'Kroksovo', 'Kosovo', 'Losovo','Lampy.sk', 'Malovanky', 'Kroksovo', 'Kosovo', 'Losovo','Lampy.sk', 'Malovanky', 'Kroksovo', 'Kosovo', 'Losovo'])
# Save (commit) the changes
connection.commit()

# Close connection
connection.close()
