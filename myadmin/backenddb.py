import os, csv, string
from django.utils import timezone
from django.conf import settings

## models import
from user.models import User
from locus.models import *
## debug
from pprint import pprint
# Create your models here.


gCountries = (
	{'name':'India', 'file': os.path.join(settings.STATIC_DATA_DIR, 'India_pincodes.csv')},
)

def insert_default_values():
	for country in gCountries:
		if Country.fetch(name=country['name']) != None:
			continue

		curr_country = Country.create(country['name'])
		print('curr_country : '+curr_country.name)
		print('file_path : '+country['file'])
		with open(country['file'], "rt") as file:
			reader = csv.reader(file, delimiter=",")
			header = next(reader)
			#print('line[{}] = {} | {} | {} | {}'.format(0, header[0], header[1], header[8], string.capwords(header[9])))
			curr_city = City(name='')
			curr_state = State(name='')
			for i, line in enumerate(reader, start=1):
				area_name = line[0]
				area_pincode = line[1]
				city_name = line[8]
				state_name = string.capwords(line[9])

				if area_name.endswith(" B.O") or area_name.endswith(" S.O"):
					area_name = area_name[:-3]

				if curr_state.name != state_name:
					## time to create new state
					curr_state = State.fetch_or_create(state_name, curr_country)
					#print('new state created : '+curr_state.name)

				if curr_city.name != city_name:
						curr_city = City.fetch_or_create(city_name, curr_state, curr_country)

				#print('line[{}] = {} | {} | {} | {}'.format(i, area_name, area_pincode, city_name, state_name))
				Area.fetch_or_create(area_name, area_pincode, curr_city, curr_state, curr_country)
		print('Done!! Country : '+curr_country.name)



def insert_custom_values(p_city_name, p_state_name, p_country_name):
	country_name = 'India'
	country_file = os.path.join(settings.STATIC_DATA_DIR, 'India_pincodes.csv')
	curr_country = Country.fetch_or_create(country_name)

	with open(country_file, "rt") as file:
		reader = csv.reader(file, delimiter=",")
		header = next(reader)
		print('line[{}] = {} | {} | {} | {}'.format(0, header[0], header[1], header[8], string.capwords(header[9])))

		curr_city = City(name='')
		curr_state = State(name='')
		for i, line in enumerate(reader, start=1):
			state_name = string.capwords(line[9])
			city_name = line[8]
			if p_state_name != state_name or p_city_name != city_name:
				continue

			area_name = line[0]
			area_pincode = line[1]

			if area_name.endswith(" B.O") or area_name.endswith(" S.O"):
				area_name = area_name[:-3]
			#print('line[{}] = {} | {} | {} | {}'.format(i, area_name, area_pincode, city_name, state_name))

			if curr_state.name != state_name:
				## time to create new state
				curr_state = State.fetch_or_create(state_name, curr_country)
				print('new state created : '+curr_state.name)

			if curr_city.name != city_name:
				curr_city = City.fetch_or_create(city_name, curr_state, curr_country)

			Area.fetch_or_create(area_name, area_pincode, curr_city, curr_state, curr_country)
		print('Done!!')
