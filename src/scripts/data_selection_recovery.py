from datetime import date, timedelta
import csv

# FIPS is a code for US cities, our selected city keys are in here
fips_dict = {	
				"11" : "D.C.",
				"44" : "Rhode Island",
				"24" : "Maryland",
				"51" : "Virginia",
			}

base_dir = "../../data/csse_covid_19_daily_reports_us"
start_date = date(2020, 4, 12) 
end_date = date.today() - timedelta(1)

# create a max-length list for each city, we can cut them down later
day_count = (end_date - start_date).days + 1
cumulative = { key: [[0, 0, 0, 0] for i in range(0, day_count)] for key in fips_dict.keys()} 
# {fips_id => [ [cumulative_recovery, daily_proportion_recovery, total_recovered, active], .. ]}


for n in range(day_count):

	date = start_date + timedelta(n)
	filepath = base_dir + "/" + date.strftime("%m-%d-%Y") + ".csv"

	with open(filepath, 'r') as f:

		
		for row in f: 

			info = row.split(',')
			date_s = date.strftime("%m-%d-%Y")

			"""
			info:
				[5]	: confirmed cases
				[6] : deaths
				[7]	: recovered
						recovered 	= total - active - deaths
									= [7] - [10] - [8]
									*** this doesn't work, data is not accurate
				[8]	: active
				[9]	: FIPS key

				so, 
					// how many recover?
					recovery_rate 	= total recovered / total cases
									= [7] / [5]
					// how much will recover into the next day?
					daily_recovered_proportion'	= (recovered - recovered') / active'
												= ([7] - [7']) / [8']
												= ([7] - [n-1][2]) / [n-1][3]

			"""

			try:

				if (str(int(float(info[9]))) in fips_dict.keys()): # the FIPS ID matches one of our cities
					
					# everything is read as a string, so need to convert numeric data for calculations
					for i in range(5, 10):
						if info[i] == '':
							info[i] = 0
						else:
							info[i] = int(float(info[i]))

					# convert FIPS back since the key is a str
					fips_id = str(info[9])

					# [cumulative_recovery, daily_proportion_recovery, total_recovered, active]
					vals = [0, 0, 0, 0]

					# total recovery rate
					if info[7] != 0:
						vals[0] = info[7] / info[5] 

					# daily recovery proprtion for n-1
					if cumulative[fips_id][n-1][3] != 0:
						vals[1] = (info[7] - cumulative[fips_id][n-1][2]) / cumulative[fips_id][n-1][3]

					# total recovered  
					vals[2] = info[7]

					# active
					vals[3] = info[8]

					cumulative[fips_id][n] = vals 

			except:
				continue






file_dict = {
	0 : "../../data/selected/cumulative_recovery_rate.csv",
	1 : "../../data/selected/daily_recovery_proportion.csv",
	2 : "../../data/selected/cumulative_recoved_total.csv",
	3 : "../../data/selected/active.csv"
}

header = [(start_date + timedelta(n)).strftime("%m/%d/%Y") for n in range(day_count)] 
header.insert(0, "State")
header.insert(0, "FIPS")

for index_key in file_dict.keys():
	with open(file_dict[index_key], 'w', newline='') as f:
		writer = csv.writer(f)

		writer.writerow(header)
		for fips_key in cumulative:
			sub = [daily_vals[index_key] for daily_vals in cumulative[fips_key]]
			name = fips_dict[fips_key]
			sub.insert(0, name)		# state
			sub.insert(0, fips_key)	# fips
			writer.writerow(sub)




