import csv
import argparse
import logging
from datetime import date, timedelta
from dataclasses import dataclass

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__file__)


@dataclass
class TableAvailability:
    id: int
    table_id: int
    booking_time: str
    order_id: int = None
    is_available: bool = True


def get_restaurant_table_ids(path_to_restaurant_table: str):
    with open(path_to_restaurant_table, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        table_id_index = None
        for row in csv_reader:
            if table_id_index is None:
                table_id_index = row.index('table_id')
            else:
                yield row[table_id_index]


def generate(path_to_restaurant_table: str, start_date: date, end_date: date, hour_range: list, interval: int, output: str):
    logger.info(f"generate table availability data...")
    logger.info(f"start_date={start_date}, end_date={end_date}")
    index = 1
    with open(output, 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=list(TableAvailability.__dataclass_fields__.keys()))
        csv_writer.writeheader()
        for restaurant_table_id in get_restaurant_table_ids(path_to_restaurant_table):
            logger.debug(f"adding available tables for restaurant_table={restaurant_table_id}, current_index={index}...")
            for _delta_days in range((end_date-start_date).days + 1):
                for start_hour, end_hour in hour_range:
                    for _hours in range(start_hour, end_hour+1, interval):
                        current_date = start_date + timedelta(days=_delta_days)
                        current_datetime_str = f"{current_date}T{_hours:02d}:00:00"
                        table_availability = TableAvailability(id=index, table_id=restaurant_table_id, booking_time=current_datetime_str)
                        csv_writer.writerow(table_availability.__dict__)
                        index += 1
    logger.info(f"data is saved into {output} successfully!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input',  default='data/restaurant_table.csv', help='a csv file contains restaurant table information')
    parser.add_argument('-o', '--output', default='data/table_availability.csv', help='output file path')
    parser.add_argument('--startdate', type=date.fromisoformat, default=date.today(), help='start date of table availability, format=YYYY-MM-DD (Inclusive)')
    parser.add_argument('--enddate', type=date.fromisoformat, default=date.today()+timedelta(days=30), help='end date of table availability, format=YYYY-MM-DD (Inclusive)')
    parser.add_argument('--hourrange', type=list, default=[(11, 13), (17, 22)], help='daily operating hour range, format=HH (Inclusive)')
    parser.add_argument('--interval', type=int, default=1, help='interval between each window in hours')
    args = parser.parse_args()
    generate(args.input, args.startdate, args.enddate, args.hourrange, args.interval, args.output)