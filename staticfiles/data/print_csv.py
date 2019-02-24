import csv, string

country_file = 'India_pincodes.csv'

with open(country_file, "rt") as file:
	reader = csv.reader(file, delimiter=",")
	#header = next(reader)
	#print('line[{}] = {} | {} | {} | {}'.format(0, header[0], header[1], header[8], string.capwords(header[9])))
	#curr_city = City(name='')
	#curr_state = State(name='')
	for i, line in enumerate(reader, start=1):
		area_name = line[0]
		area_pincode = line[1]
		city_name = line[8]
		state_name = string.capwords(line[9])

		if area_name.endswith(" B.O") or area_name.endswith(" S.O"):
			area_name = area_name[:-3]

		'''
		if curr_state.name != state_name:
			# time to create new state
			curr_state = State.add_state(state_name, curr_country)
			print('new state created : '+curr_state.name)

		if curr_city.name != city_name:
				curr_city = City.add_city(city_name, curr_state, curr_country)
		'''

		print('line[{}] = {} | {} | {} | {}'.format(i, area_name, area_pincode, city_name, state_name))
