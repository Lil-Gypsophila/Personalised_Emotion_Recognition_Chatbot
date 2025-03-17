"""
NAME: CHEAH WENG HOE
DATE CREATED: 28/1/2025
LAST MODIFIED: 28/1/2025

Module to Handle Database
"""

import sqlite3

# Connect to the database
conn = sqlite3.connect("database\\debs.db")
cursor = conn.cursor()


# System Paths
# Create sys path table (Store path to perform tasks)
query = "CREATE TABLE IF NOT EXISTS sys_path(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
cursor.execute(query)

# Web Paths
# Create web path table
query = "CREATE TABLE IF NOT EXISTS web_path(id integer primary key, name VARCHAR(100), url VARCHAR(1000))"
cursor.execute(query)


# Update
# # Adding an alias column to sys_path and web_path tables
# query = "ALTER TABLE sys_path ADD COLUMN alias VARCHAR(100)"
# cursor.execute(query)
# conn.commit()


# # Adding an alias column to sys_path and web_path tables
# query = "ALTER TABLE web_path ADD COLUMN alias VARCHAR(100)"
# cursor.execute(query)
# conn.commit()


# Create
# Insert into sys path
query = "INSERT INTO sys_path VALUES (null,'league of legends', 'G:\\Riot Games\\Riot Client\\RiotClientServices.exe', 'league')"
cursor.execute(query)
conn.commit()


# Insert YT into web path
query = "INSERT INTO web_path VALUES (null,'youtube', 'https://www.youtube.com/', 'yt')"
cursor.execute(query)
conn.commit()

# Insert FB into web path
query = "INSERT INTO web_path VALUES (null,'facebook', 'https://www.facebook.com/', 'fb')"
cursor.execute(query)
conn.commit()

# Insert Github into web path
query = "INSERT INTO web_path VALUES (null,'github', 'https://github.com/', 'git')"
cursor.execute(query)
conn.commit()


# Delete
# # SQL to Delete Path
# query = "DELETE FROM sys_path WHERE name = 'league of legends'"
# cursor.execute(query)
# conn.commit()