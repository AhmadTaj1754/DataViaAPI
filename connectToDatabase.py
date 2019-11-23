

import requests
import json
import csv
import mysql.connector


#Obtain "Chained Consumer Price Index for All Urban Consumers: All Items in U.S.
#City Average " data from U.S. Bureau of Labor Statistics via public API, in
#the form of JSON, and write to CSV file
headers = {'Content-type': 'application/json'}
data = json.dumps({"seriesid": ['SUUR0000SA0'],"startyear":"2000", "endyear":"2019", "registrationkey":"KEY"})
reqst = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
json_data = json.loads(reqst.text)
# print(json_data)
with open('file.cvs', 'w') as csvfile:
    datawriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    for series in json_data['Results']['series']:
        seriesId = series['seriesID']
        for item in series['data']:
            year = item['year']
            period = item['period']
            periodName = item["periodName"]
            value = item['value']
            footnotes=item['footnotes']
            if series['seriesID']=="SUUR0000SA0":
                seriesName = "Chained Consumer Price Index for All Urban Consumers: All Items in U.S. City Average "
            else:
                seriesName = "Not Available"
            for footnote in item['footnotes']:
                if footnote:
                    footnotes = footnotes + footnote['text']
            datawriter.writerow([seriesId,seriesName,year,period,periodName, value,footnotes[0:2]])

#connect to MySQL database and insert values obtianed with BLS API into
#pre-created BLS database table
mydb = mysql.connector.connect(
  host="IP Address",
  user="username",
  passwd="password",
  database="BLS",
  buffered=True,
)
mycursor = mydb.cursor()
with open('file.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        sqlstatement="INSERT INTO Chained_ConsumerPrice_US_City_Average(SeriesID,SeriesName, year,period, PeriodName, DataPoint, Footnotes) Values({0},{1},{2},{3},{4},{5},{6})".format(repr(row[0]),repr(row[1]),repr(row[2]),repr(row[3]),repr(row[4]),repr(row[5]),repr(row[6]))
        mycursor.execute(sqlstatement)
mydb.commit()
mycursor.execute("SHOW TABLES")




























#end
