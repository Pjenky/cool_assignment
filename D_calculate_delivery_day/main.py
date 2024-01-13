from datetime import timedelta, time, datetime, timezone
import pytz
# TODO: 
# remove pytz dependency due to deprecation
# potentially use Sets instead of Lists for faster lookup in is_closed()

# Meeus/Jones/Butcher algorithm for calculating the date of Easter
def calculate_easter_day(year):
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return datetime(year, month, day)

# Function to check if a given date is a holiday
def is_closed(dt):
    easter_day = calculate_easter_day(dt.year)
    days_closed = [datetime(dt.year, 1, 1), # Nytårsdag
                     easter_day - timedelta(days=7), # Palmesøndag
                     easter_day - timedelta(days=3), # Skærtorsdag
                     easter_day - timedelta(days=2), # Langfredag
                     easter_day, # Påskedag
                     easter_day + timedelta(days=1), # 2. påskedag
                     easter_day + timedelta(days=26), # Store bededag (i mine øjne er det stadig en helligdag)
                     easter_day + timedelta(days=39), # Kristi himmelfartsdag
                     easter_day + timedelta(days=49), # Pinsedag
                     easter_day + timedelta(days=50), # 2. pinsedag
                     datetime(dt.year, 6, 5), # Grundlovsdag
                     datetime(dt.year, 12, 24), # Juleaften
                     datetime(dt.year, 12, 25), # Juledag
                     datetime(dt.year, 12, 26), # 2. juledag
                     datetime(dt.year, 12, 31) # Nytårsaften
                     ]
    
    if dt in days_closed:
        return True
    else:
        return False

def next_working_day(dt):
    # Keep adding days until a non-weekend, non-holiday is found
    while dt.weekday() >= 5 or is_closed(dt):
        dt += timedelta(days=1)
    return dt

def get_delivery_date(order_datetime):
    denmark_tz = pytz.timezone("Europe/Copenhagen")

    # Define the cutoff time for next-day delivery
    cutoff_time = time(15, 0, 0, tzinfo=denmark_tz)

    # Convert the order time to the same timezone as the cutoff time
    order_datetime = order_datetime.astimezone(denmark_tz)
    order_time = order_datetime.time()

    # Check if the order was placed before or after the cutoff time
    if order_time < cutoff_time:
        order_send_date = order_datetime + timedelta(days=1)
    else:
        order_send_date = order_datetime + timedelta(days=2)

    # Adjust for weekends and holidays
    delivery_time = next_working_day(order_send_date.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None))

    return delivery_time

# Example usage:
example_orders = [datetime(2021, 5, 20, 12, 51, 32, 199883, timezone.utc),
                    datetime(2021, 5, 20, 13, 3, 31, 245381, timezone.utc),
                    datetime(2020, 12, 29, 12, 15, 12, 0, timezone.utc),
                    datetime(2020, 12, 29, 14, 15, 12, 0, timezone.utc)]
for i in example_orders:
    print("Order Placed:", i.strftime("%d-%m-%Y %H:%M:%S %Z"))
    print("Estimated Delivery Date:", get_delivery_date(i).strftime("%d-%m-%Y"))
    print()
