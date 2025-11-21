from faker import Faker

fake = Faker()


def profile_faker():
    """Generate fake user profile data.

    Returns:
            dict: Fake profile with name, address, email, etc.
    """
    return {
        "name": fake.name(),
        "address": fake.address(),
        "city": fake.city(),
        "state": fake.state(),
        "email": fake.email(),
        "company": fake.company(),
        "birthday": str(fake.date_time()),
        "ssn": fake.ssn(),
        "phone_number": fake.phone_number(),
        "job": fake.job(),
    }
