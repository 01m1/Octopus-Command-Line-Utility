import argparse
import datetime


def parse_flow(path):
    data = {}
    with open(path, 'r') as file:
        flow = [line.strip() for line in file.readlines()]  # Split lines of file and strip \n characters for new lines.

        for i in range(1, len(flow) - 1, 2):  # Iterate through lines except 'Header' and 'Footer'
            meter = flow[i].strip().split('|')
            reading = flow[i + 1].strip().split('|')  # Meter and Readings come in pairs so this shouldn't cause errors.

            # Process data
            meter_id = int(meter[1])
            reading_id = int(reading[1])
            reading_value = float(reading[2])
            reading_date = datetime.datetime.strptime(reading[3], "%Y%m%d").date()
            reading_status = str(reading[4])

            # Store data into dictionary
            data[meter_id] = {"READING_ID": reading_id,
                              "READING_VALUE": reading_value,
                              "DATE": reading_date,
                              "READING_STATUS": reading_status}

    return data

# Console Outputs


def meter_count(data):
    return len(data)


def total_sum_valid_readings(flow):
    print()


def total_sum_invalid_readings(flow):
    print()


def highest_and_lowest_valid_readings(flow):
    print()


def most_recent_and_oldest_readings(flow):
    print()


print(parse_flow('meter_readings'))
flow_data = parse_flow('meter_readings')
print("Count of meters:", meter_count(flow_data))
