import json


def find_speed_on_date(json_path, designation, target_date):
    """
    Print and return the relative velocity of a Near-Earth Object (NEO)
    on a specific date.

    Args:
        json_path (str): Path to the NASA CAD JSON file.
        designation (str): The NEO designation to search for.
        target_date (str): The date to filter (format: 'YYYY-MMM-DD', e.g., '2000-Jan-01').

    Returns:
        str or None: The velocity in km/s if found, else None.
    """
    with open(json_path, "r") as file:
        data = json.load(file)

    for entry in data["data"]:
        entry_designation = entry[0]
        entry_date = entry[3]
        velocity = entry[7]

        if entry_designation == designation and entry_date.startswith(target_date):
            print(f"{designation} speed on {target_date}: {velocity} km/s")
            return velocity

    return None


if __name__ == "__main__":
    speed = find_speed_on_date("cad.js", "2002 PB", "2000-Jan-01")
    if speed is None:
        print("No matching data found.")
