import argparse
import logging
from datetime import date, timedelta, datetime
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__file__)


@dataclass
class TableAvailability:
    id: int
    restaurant_table_id: int
    order_id: int 
    booking_time: str
    is_available: bool = True


def get_restaurant_table_ids(path_to_restaurant_table: str):
    with open(path_to_restaurant_table, 'r') as f:
        for line in f:
            #TODO: wait for restaurant table data
            restaurant_table_id = None
            yield restaurant_table_id


def generate(path_to_restaurant_table: str, start_date: date, start_hour: int, end_date: date, end_hour: int, interval: int, output: str):
    logger.info(f"generate table availability data...")
    logger.info(f"start_datetime={start_date}T{start_hour:02d}:00:00, end_datetime={end_date}T{end_hour:02d}:00:00")
    index = 1
    with open(output, 'w') as f:
        header = ','.join(TableAvailability.__dataclass_fields__.keys())
        f.write(header + "\n")
        for restaurant_table_id in get_restaurant_table_ids(path_to_restaurant_table):
            logger.debug(f"adding available tables for restaurant_table={restaurant_table_id}, current_index={index}...")
            for _delta_days in range((end_date-start_date).days + 1):
                for _hours in range(start_hour, end_hour+1, step=interval):
                    current_date = start_date + timedelta(days=_delta_days)
                    current_datetime_str = f"{current_date}T{_hours:02d}:00:00"
                    table_availability = TableAvailability(id=index, restaurant_table_id=restaurant_table_id, booking_time=current_datetime_str)
                    f.write(table_availability.__dict__ + "\n")
                    index += 1
    logger.info(f"data is saved into {output} successfully!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('path_to_restaurant_table', help='a csv file contains restaurant table information')
    parser.add_argument('-o', '--output', default='data/table_availability.csv', help='output file path')
    parser.add_argument('--startdate', type=date.fromisoformat, default=date.today(), help='start date of table availability, format=YYYY-MM-DD (Inclusive)')
    parser.add_argument('--starthour', type=int, default=10, help='start hour of each day, format=HH (Inclusive)')
    parser.add_argument('--enddate', type=date.fromisoformat, default=date.today()+timedelta(days=45), help='end date of table availability, format=YYYY-MM-DD (Inclusive)')
    parser.add_argument('--endhour', type=int, default=22, help='end hour of each day, format=HH (Inclusive)')
    parser.add_argument('--interval', type=int, default=1, help='interval between each window in hours')
    args = parser.parse_args()
    generate(args.startdate, args.starthour, args.enddate, args.endhour, args.interval, args.output)