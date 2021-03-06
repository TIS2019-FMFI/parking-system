import sqlite3
from Database import Database

connection = sqlite3.connect("kvant.db")
cursor = connection.cursor()


cursor.execute("DROP TABLE IF EXISTS records")
cursor.execute("DROP TABLE IF EXISTS companies")
cursor.execute("DROP TABLE IF EXISTS boxes")

# Table from companies
cursor.execute('''CREATE TABLE IF NOT EXISTS companies
                  (companyID INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT)''')

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

# Table for notifications
cursor.execute('''CREATE TABLE IF NOT EXISTS notifications
                  (notificationId INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT)''')

print("Tables created.")

def fill_data(data):
    db=Database("kvant.db")
    for i in data:
        db.createCompany(i)
fill_data(['KVANT', 'Integard', 'D4R7', 'Škola.sk', 'MKMs', 'MTRUST', 'Businessmedia', 'Reštaurácia'])

# Save (commit) the changes
connection.commit()

# Close connection
connection.close()

print("All done!")
