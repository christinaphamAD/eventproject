import sqlite3
import csv

conn = sqlite3.connect('event_finder.db')
c = conn.cursor()

# Create table
try:c.execute('''CREATE TABLE Events (
ID INTEGER PRIMARY KEY,
Name TEXT,
Description TEXT,
Category TEXT,
Website_URL TEXT,
Image_URL TEXT,
Start_Date NUMERIC,
End_Date NUMERIC,
Location TEXT,
Up_Votes NUMERIC,
Down_Votes NUMERIC,
Tickets TEXT)''')
except:pass


#Get CSV data
csvFile = open('events.csv','U')
csvData=csv.reader(csvFile)
csvData.next() #skips the heading line with field names

#Insert row of data
for row in csvData:
    c.execute('''INSERT INTO Events (Name, Description, Category, Website_URL, Image_URL, Start_Date, End_Date, Location, Up_Votes, Down_Votes, Tickets, ID)
    VALUES ("'''+'", "'.join(row)+'")')

csvFile.close()

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
