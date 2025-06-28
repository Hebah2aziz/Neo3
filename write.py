import csv
import json

def write_to_csv(results, filename):
    """
    Write a stream of CloseApproach results to a CSV file.

    Each row contains details about a close approach and its associated NEO.
    If there are no results, only the header row is written.

    :param results: An iterable of CloseApproach objects.
    :param filename: The output CSV file path.
    """
    # Define the CSV column headers
    fieldnames = [
        'datetime_utc', 'distance_au', 'velocity_km_s',
        'designation', 'name', 'diameter_km', 'potentially_hazardous'
    ]

    # Open the file and prepare to write CSV data
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()  # Write the header row

        # Write each CloseApproach as a row
        for approach in results:
            neo = approach.neo
            writer.writerow({
                'datetime_utc': approach.time_str,                     # Approach time (formatted)
                'distance_au': approach.distance,                      # Approach distance
                'velocity_km_s': approach.velocity,                    # Relative velocity
                'designation': neo.designation,                        # NEO designation
                'name': neo.name or '',                                # Name or empty string
                'diameter_km': '' if neo.diameter is None else neo.diameter,  # Diameter or blank
                'potentially_hazardous': str(neo.hazardous),           # True/False as string
            })


def write_to_json(results, filename):
    """
    Write a stream of CloseApproach results to a JSON file.

    Each entry is a dictionary that includes details about the approach and the NEO.
    An empty list is written if there are no results.

    :param results: An iterable of CloseApproach objects.
    :param filename: The output JSON file path.
    """
    output = []

    # Create dictionary entries for each CloseApproach
    for approach in results:
        neo = approach.neo
        entry = {
            "datetime_utc": approach.time_str,         # Approach time
            "distance_au": approach.distance,          # Distance in AU
            "velocity_km_s": approach.velocity,        # Velocity in km/s
            "neo": {
                "designation": neo.designation,        # NEO designation
                "name": neo.name or '',                # Name or empty string
                "diameter_km": None if neo.diameter is None else neo.diameter,
                "potentially_hazardous": neo.hazardous  # Boolean flag
            }
        }
        output.append(entry)

    # Write the entire list to the JSON file with indentation
    with open(filename, 'w') as jsonfile:
        json.dump(output, jsonfile, indent=2)
