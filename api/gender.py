import os
dir_path = os.path.dirname(os.path.realpath(__file__))

with open(dir_path + '/data/female_name.txt') as f:
	female_name = f.read().splitlines()

def name_to_gender(name):
	global female_name

	name = name.encode('utf8').lower()
	gender = 'female' if (s.lower() in name for s in female_name) else 'unknown'

	if gender == 'unknown':
		# TODO: male name
		gender = 'male'

	return gender