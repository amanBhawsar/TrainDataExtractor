import csv
from bs4 import BeautifulSoup
from itertools import zip_longest
import requests
import datetime
import time
# csv file name
trainNumber=[]
file = open("SelectedTrain.csv")
reader = csv.reader(file)
for line in reader:
    trainNumber.append(line)
while True:
    for a in trainNumber:
        r = requests.get("https://trainstatus.info/running-status/" + a[0])  # train status.info
        soup = BeautifulSoup(r.text, "html.parser")
        results = soup.find("table", {"class": "table table-striped runtable"})
        try:
            child = results.find("tbody")
            all_tr = child.find_all("tr")
            StationName = ['Station Name']
            SchArrival = ['Sch. Arrival']
            SchDeparture = ['Sch. Departure']
            ActualArrival = ['Actual Arrival (Delay)']
            ActualDeparture = ['Actual Departure (Delay)']
            Distance = ['Distance']
        except:
            print(a[0] + " ")
        for i in all_tr:
            # print(i)
            c = i.find_all("td")

            if len(c) == 7:
                StationName.append(c[1].text)
                SchArrival.append(c[2].text)
                SchDeparture.append(c[3].text)
                ActualArrival.append(c[4].text)
                ActualDeparture.append(c[5].text)
                Distance.append(c[6].text)

        fields = ['Station Name', 'Sch. Arrival', 'Sch. Departure', 'Actual Arrival (Delay)',
                  'Actual Departure (Delay)', 'Distance']
        rows = [StationName, SchArrival, SchDeparture, ActualArrival, ActualDeparture, Distance]
        filename = "train.csv"
        currDateTime = str(datetime.datetime.now())
        currDateTime = currDateTime.replace(' ', 'and_Time_is_')
        currDateTime = currDateTime.replace('.', 'uniq')
        currDateTime = currDateTime.replace('-', '_')
        currDateTime = currDateTime.replace(':', '_')
        print(currDateTime)
        # currDateTime="ahah"
        with open(filename, 'w') as csvfile:
            # creating a csv writer object
            csvwriter = csv.writer(csvfile)

            # writing the fields
            csvwriter.writerow(fields)

            # writing the data rows
            csvwriter.writerow(rows)

            d = [StationName, SchArrival, SchDeparture, ActualArrival, ActualDeparture, Distance]
            export_data = zip_longest(*d, fillvalue='')
            with open(currDateTime + '.csv', 'w', encoding="ISO-8859-1", newline='') as myfile:
                wr = csv.writer(myfile)
                wr.writerows(export_data)
            myfile.close()
    time.sleep(4)   #delay in seconds
