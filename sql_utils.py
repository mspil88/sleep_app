import sqlite3
from datetime import datetime
from sqlalchemy import create_engine
from datetime import timedelta
import itertools


class SleepDatabase:
    def __init__(self, path):
        self.path = path

    def establish_connection(self):
        try:
            connection = sqlite3.connect(self.path, isolation_level=None)
            return connection
        except sqlite3.Error as e:
            print(e)

    def _execute(self, sql):
        try:
            connection = self.establish_connection().cursor()
            connection.execute(sql)
        except sqlite3.Error as e:
            print(e)

    def select(self, sql, task=None):

        def dictionary_factory(cursor, row):
            d = {}
            for i, c in enumerate(cursor.description):
                d[c[0]] = row[i]
            return d

        try:
            connection = self.establish_connection()
            connection.row_factory = dictionary_factory
            cur = connection.cursor()

            if task:
                result = connection.execute(sql, task).fetchall()
            else:
                result = connection.execute(sql).fetchall()
            return result
        except sqlite3.Error as e:
            print(e)

    def update(self, sql, task):
        try:
            connection = self.establish_connection()
            if not task:
                raise KeyError("Must provide arguments for UPDATE")
            connection.cursor().execute(sql, task)
            connection.commit()
        except sqlite3.Error as e:
            print(e)

    def table_rendering(self, *tables):
        for table in tables:
            self._execute(table)


def create_db_key(user_id, date):
    date = date.replace("-", "_")
    return f"{user_id}_{date}"


def get_weekday(date):
    date_format = "%Y-%m-%d"
    weekday_int = datetime.strptime(date, date_format).weekday()
    weekday_map = {i: j for i, j in zip(range(7), ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])}
    return weekday_map[weekday_int]

#NEED TO ADD MONTH AT END OF DATE AS WELL - CHECK BELOW WORKS

def week_commencing_data(month_hash):
    start_date = '2021-08-02'
    date_format = "%Y-%m-%d"

    def format_week_commencing(day_str, month_hash):
        day_str_spt = day_str[-2:].split("-")[0]
        orig_day_str = day_str.split("-")

        if day_str_spt == "01":
            day_str_spt += "st"
        elif day_str_spt == "02":
            day_str_spt += "nd"
        elif day_str_spt == "03":
            day_str_spt += "rd"
        else:
            day_str_spt += "th"

        month = month_hash[orig_day_str[1]]

        return f"{day_str_spt} {month}"

    dates = [datetime.strftime(datetime.strptime(start_date, date_format) + timedelta(days=i), date_format) for i in
             range(0, 1827)]
    days = [get_weekday(dates[i]) for i in range(len(dates))]
    wc_date = list(itertools.chain.from_iterable([itertools.repeat(i, 7) for i in
                                                  [format_week_commencing(i, month_hash) for i, j in zip(dates, days) if
                                                   j == 'Monday']]))

    return {k: v for k, v in zip(dates, wc_date)}


USER_TABLE = """CREATE TABLE IF NOT EXISTS users (
                 id integer PRIMARY KEY,
                 email_address text,
                 password text,
                 created_on timestamp);"""

TIME_IN_BED_TABLE = """CREATE TABLE IF NOT EXISTS time_in_bed (
                 user_key text PRIMARY KEY,
                 user_id integer,
                 in_bed text,
                 out_bed text,
                 created_on timestamp,
                 created_date date);"""

TIME_TO_SLEEP = """CREATE TABLE IF NOT EXISTS time_to_sleep (
                 user_key text PRIMARY KEY,
                 user_id integer,
                 time_to_fall_asleep text,
                 time_to_get_out_bed text,
                 created_on timestamp,
                 created_date date);"""

NUMBER_OF_GAPS = """CREATE TABLE IF NOT EXISTS sleep_gaps (
                user_key text PRIMARY KEY,
                user_id integer,
                gaps integer,
                created_on timestamp,
                created_date date);"""

GAP_LENGTHS = """CREATE TABLE IF NOT EXISTS gap_lengths (
                user_key text PRIMARY KEY,
                user_id integer,
                gap_lengths text,
                created_on timestamp,
                created_date date);"""

SLEEP_MOODS = """CREATE TABLE IF NOT EXISTS sleep_moods (
                user_key text PRIMARY KEY,
                user_id integer,
                user_moods text,
                selected_moods text,
                created_on timestamp,
                created_date date);"""

SLEPT_WELL = """CREATE TABLE IF NOT EXISTS slept_well (
                user_key text PRIMARY KEY,
                user_id integer,
                slept_well text,
                created_on timestamp,
                created_date date);"""

WEEK_COMMENCING = """CREATE TABLE IF NOT EXISTS week_commencing_ref (
                     created_date date PRIMARY KEY,
                     wc text); """
