import argparse
import datetime


def parse_flow(path):
    data = {}
    with open(path, 'r') as file:
        # Split lines of file and strip \n characters for new lines
        flow = [line.strip() for line in file.readlines()]

        # Iterate through lines except 'Header' and 'Footer'
        for i in range(1, len(flow) - 1, 2):
            meter = flow[i].strip().split('|')
            reading = flow[i + 1].strip().split('|')  # Meter and Readings come in pairs so this shouldn't cause errors

            # Process data
            meter_id = int(meter[1])
            reading_id = int(reading[1])
            reading_value = float(reading[2])
            reading_date = datetime.datetime.strptime(reading[3], "%Y%m%d").date()
            reading_status = str(reading[4])

            # Store data into dictionary, meters can have multiple readings so store using 'dictionary of dictionaries'
            if meter_id not in data:
                data[meter_id] = {}
            data[meter_id][reading_id] = {"READING_VALUE": reading_value,
                                          "READING_DATE": reading_date,
                                          "READING_STATUS": reading_status}

    return data


# Console Outputs


def meter_count(data):
    return len(data)


def total_sum_valid_readings(data):
    # Iterate through reading dictionaries inside meter dictionary and sum valid values
    return sum(reading['READING_VALUE'] for meter in data.values()
               for reading in meter.values() if reading['READING_STATUS'] == 'V')


def total_sum_invalid_readings(data):
    # Iterate through reading dictionaries inside meter dictionary and sum invalid values
    return sum(reading['READING_VALUE'] for meter in data.values()
               for reading in meter.values() if reading['READING_STATUS'] == 'F')


def highest_and_lowest_valid_readings(data):
    # Iterate through reading dictionaries inside meter dictionary to create a list of valid readings
    valid_readings = [(readings[reading]["READING_VALUE"], meter_id) for meter_id, readings in data.items()
                      for reading in readings if readings[reading]["READING_STATUS"] == "V"]

    # No need to check if file actually has valid readings as notes say to assume file conforms to the schema supplied.
    highest_value = max(valid_readings)[0]
    lowest_value = min(valid_readings)[0]
    # Check for multiple occurrences of values
    highest_value_ids = find_occurrences(data, 'READING_VALUE', highest_value)
    lowest_value_ids = find_occurrences(data, 'READING_VALUE', lowest_value)

    return highest_value, highest_value_ids, lowest_value, lowest_value_ids


def most_recent_and_oldest_readings(data):
    # Iterate through reading dictionaries inside meter dictionary to create a list of all readings
    all_readings = [(readings[reading]["READING_DATE"], meter_id) for meter_id, readings in data.items()
                    for reading in readings]

    # No need to check if file has readings as notes say to assume file conforms to the schema supplied.
    newest_date = max(all_readings)[0]
    oldest_date = min(all_readings)[0]
    # Check for multiple occurrences of values
    newest_meter_ids = find_occurrences(data, 'READING_DATE', newest_date)
    oldest_meter_ids = find_occurrences(data, 'READING_DATE', oldest_date)
    return newest_date, newest_meter_ids, oldest_date, oldest_meter_ids


def find_occurrences(data, key, value):
    # Go through whole dictionary of dictionaries to check for multiple occurrences of a value under a certain key
    return [reading_id for meter_id, values in data.items()
            for reading_id in values if values[reading_id][key] == value]


if __name__ == "__main__":
    # Parse flow as input
    parser = argparse.ArgumentParser(description="Process flow and output result,")
    parser.add_argument("file_path", type=str, help="File path of the flow file.")
    args = parser.parse_args()
    flow_data = parse_flow(args.file_path)

    # Output
    print("+-----------------------------------------------------------------+")
    print(" Flow Data")
    print("\n")
    print(" Number of Meters:", meter_count(flow_data))

    print("\n Total sum of valid meter readings:", total_sum_valid_readings(flow_data))
    print("\n Total sum of invalid meter readings:", total_sum_invalid_readings(flow_data))

    print("\n Highest valid meter reading:", highest_and_lowest_valid_readings(flow_data)[0],
          "\n Reading ID(s):", highest_and_lowest_valid_readings(flow_data)[1])
    print("\n Lowest valid meter reading:", highest_and_lowest_valid_readings(flow_data)[2],
          "\n Reading ID(s):", highest_and_lowest_valid_readings(flow_data)[3])
    print("\n Most recent valid meter reading:", most_recent_and_oldest_readings(flow_data)[0],
          "\n Reading ID(s):", most_recent_and_oldest_readings(flow_data)[1])
    print("\n Oldest valid meter reading:", most_recent_and_oldest_readings(flow_data)[2],
          "\n Reading ID(s):", most_recent_and_oldest_readings(flow_data)[3])
    print("\n")
    print("+-----------------------------------------------------------------+")