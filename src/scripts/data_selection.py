import csv

filepath = "../../data/time_series_covid19_confirmed_US.csv"

locations = {
	"Florida" : ["Miami-Dade", "Orange", "Osceola", "Glades"], 
	"New York" : ["Queens", "Orange", "Allegany", "Hamilton"], 
	"California" : ["Santa Clara", "Monterey", "Madera", "Modoc"], 
	"Texas" : ["Dallas", "Cameron", "Crockett", "Fisher"]
}

collected = []


with open(filepath, 'r') as f:

	reader = csv.reader(f)
	collected.append(f.readline().split(',')) # append the dates, header row
	
	# search for the cities specified in the locations dictionary
	for row in reader: 
		try:
			if locations[row[6]] and locations[row[6]].index(row[5]) != -1:
				print(row[5])
				collected.append(row)
		except:
			pass

# write to the output file with collected data
with open("../../data/selected_cities.csv", "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerows(collected)

#print(collected)
