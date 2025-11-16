import os

dir_path = os.path.dirname(os.path.realpath(__file__))

with open(dir_path + "/data/female_name.txt") as f:
    female_name = f.read().splitlines()


def name_to_gender(name):
    """Predict gender from first name using female name database.

    Args:
            name: First name to analyze

    Returns:
            str: 'female', 'male', or 'unknown'
    """
    global female_name

    name = name.lower()
    gender = "female" if any(s.lower() in name for s in female_name) else "unknown"

    if gender == "unknown":
        # Default to male if not found in female names
        gender = "male"

    return gender
