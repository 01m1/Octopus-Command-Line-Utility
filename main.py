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
                                          "DATE": reading_date,
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
    valid_readings = [reading["READING_VALUE"] for meter in data.values()
                      for reading in meter.values() if reading["READING_STATUS"] == "V"]

    # No need to check if file actually has valid readings as notes say to assume file conforms to the schema supplied.
    return [max(valid_readings), min(valid_readings)]


def most_recent_and_oldest_readings(data):
    print()


print(parse_flow('meter_readings'))
flow_data = parse_flow('meter_readings')
print("Count of meters:", meter_count(flow_data))
print("Total sum of valid meter readings:", total_sum_valid_readings(flow_data))
print("Total sum of invalid meter readings:", total_sum_invalid_readings(flow_data))
print("Highest valid meter reading:", highest_and_lowest_valid_readings(flow_data)[0])
print("Lowest valid meter reading:", highest_and_lowest_valid_readings(flow_data)[1])
