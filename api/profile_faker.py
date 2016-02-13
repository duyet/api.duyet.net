from faker import Factory

fake = Factory.create()

def profile_faker():
	return {
		"name": fake.name(),
		"address": fake.address(),
		"city": fake.city(),
		"state": fake.state(),
		"email": fake.email(),
		"company": fake.company(),
		"birthday": fake.date_time(),
		"ssn": fake.ssn(),
		"phone_number": fake.phone_number(),
		"job": fake.job()
	}