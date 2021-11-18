from sql_utils import SleepDatabase
import random

user_id = 4

sleep_db = SleepDatabase('database/sleep.db')

def generate_time_in_bed(user_id):
    print("Calling time_in_bed")
    bed_times = ['10:30pm', '11:00pm', '11:15pm', '11:30pm', '11:45pm', '12:00am', '12:15am', '12:30am']
    wake_times = ['05:30am', '05:45am', '06:00am', '06:15am', '06:45am', '07:00am', '07:15am', '07:30am']

    for i in range(4, 25):
        if i < 10:
            created_on = f'2021-10-0{i} 15:09:34'
        else:
            created_on = f'2021-10-{i} 15:09:34'
        created_date = created_on[0:10]
        user_key = f"{user_id}_{created_date}".replace("-", "_")
        in_bed = random.choice(bed_times)
        out_bed = random.choice(wake_times)

        sleep_db.update(
            f"INSERT or REPLACE INTO time_in_bed (user_key, user_id, in_bed, out_bed, created_on, created_date) VALUES (?, ?, ?, ?, ?, ?)",
            (user_key, user_id, in_bed, out_bed, created_on, created_date))


def generate_time_to_sleep(user_id):
    print("Calling time_to_sleep")
    for i in range(4, 25):
        sleep_times = ['Less than 15 minutes', 'About 15 minutes', '30 minutes', '45 minutes', '1 hour', '2 hours',
                       'More than 2 hours']

        if i < 10:
            created_on = f'2021-10-0{i} 15:09:34'
        else:
            created_on = f'2021-10-{i} 15:09:34'

        created_date = created_on[0:10]
        user_key = f"{user_id}_{created_date}".replace("-", "_")
        to_sleep = random.choice(sleep_times)
        to_wake = random.choice(sleep_times)
        sleep_db.update(
            f"INSERT or REPLACE INTO time_to_sleep (user_key, user_id, time_to_fall_asleep, time_to_get_out_bed, created_on, created_date) VALUES (?, ?, ?, ?, ?, ?)",
            (user_key, user_id, to_sleep, to_wake, created_on, created_date))


def generate_sleep_gaps(user_id):
    print("Calling sleep_gaps")
    for i in range(4, 25):
        gaps = ['0', '1', '2', '3', '4', '5']

        if i < 10:
            created_on = f'2021-10-0{i} 15:09:34'
        else:
            created_on = f'2021-10-{i} 15:09:34'

        created_date = created_on[0:10]
        user_key = f"{user_id}_{created_date}".replace("-", "_")
        gaps = random.choice(gaps)

        sleep_db.update(
            f"INSERT  or REPLACE INTO sleep_gaps (user_key, user_id, gaps, created_on, created_date) VALUES (?, ?, ?, ?, ?)",
            (user_key, user_id, gaps, created_on, created_date))


def generate_gap_lengths(user_id):
    print("Calling gap_lengths")
    for i in range(4, 25):
        gap_lengths = ['Less than 15 minutes', 'About 15 minutes', '30 minutes', '45 minutes', '1 hour', '2 hours',
                       'More than 2 hours']

        if i < 10:
            created_on = f'2021-10-0{i} 15:09:34'
        else:
            created_on = f'2021-10-{i} 15:09:34'

        created_date = created_on[0:10]
        user_key = f"{user_id}_{created_date}".replace("-", "_")
        gap_lengths = random.choice(gap_lengths)

        sleep_db.update(
            f"INSERT or REPLACE INTO gap_lengths (user_key, user_id, gap_lengths, created_on, created_date) VALUES (?, ?, ?, ?, ?)",
            (user_key, user_id, gap_lengths, created_on, created_date))


def generate_sleep_moods(user_id):
    print("Calling sleep_moods")
    for i in range(4, 25):

        moods = ['tired', 'frustrated', 'irritable', 'refreshed', 'alert', 'groggy']
        user_moods = ",".join([i for i in moods])

        if i < 10:
            created_on = f'2021-10-0{i} 15:09:34'
        else:
            created_on = f'2021-10-{i} 15:09:34'

        created_date = created_on[0:10]
        user_key = f"{user_id}_{created_date}".replace("-", "_")
        mood = random.choice(moods)

        sleep_db.update(
            f"INSERT  or REPLACE INTO sleep_moods (user_key, user_id, user_moods, selected_moods, created_on, created_date) VALUES (?, ?, ?, ?, ?, ?)",
            (user_key, user_id, user_moods, mood, created_on, created_date))


def generate_slept_well(user_id):
    print("Calling slept_well")
    for i in range(4, 25):

        slept_well = ['yes', 'somewhat', 'no']

        if i < 10:
            created_on = f'2021-10-0{i} 15:09:34'
        else:
            created_on = f'2021-10-{i} 15:09:34'

        created_date = created_on[0:10]
        user_key = f"{user_id}_{created_date}".replace("-", "_")
        well = random.choice(slept_well)

        sleep_db.update(
            f"INSERT or REPLACE INTO slept_well (user_key, user_id, slept_well, created_on, created_date) VALUES (?, ?, ?, ?, ?)",
            (user_key, user_id, well, created_on, created_date))


generate_time_in_bed(user_id)
generate_time_to_sleep(user_id)
generate_sleep_gaps(user_id)
generate_gap_lengths(user_id)
generate_sleep_moods(user_id)
generate_slept_well(user_id)

sleep_data = [{'day': 'Monday', 'inbed': '12:30pm', 'outbed': '5:30pm', 'hours': 3, 'sef': 35, 'how_slept': 'bad',
               'wc': '13th Sept'},
              {'day': 'Tuesday', 'inbed': '12:00am', 'outbed': '7:30pm', 'hours': 2, 'sef': 10,
               'how_slept': 'well', 'wc': '13th Sept'},
              {'day': 'Wednesday', 'inbed': '11:45pm', 'outbed': '7:00pm', 'hours': 7, 'sef': 90,
               'how_slept': 'ok', 'wc': '13th Sept'},
              {'day': 'Thursday', 'inbed': '11:45pm', 'outbed': '6:30pm', 'hours': 6, 'sef': 77,
               'how_slept': 'ok', 'wc': '13th Sept'},
              {'day': 'Friday', 'inbed': '11:00pm', 'outbed': '6:00pm', 'hours': 3, 'sef': 33,
               'how_slept': 'bad', 'wc': '13th Sept'},
              {'day': 'Saturday', 'inbed': '1:30pm', 'outbed': '4:30pm', 'hours': 2, 'sef': 44,
               'how_slept': 'bad', 'wc': '13th Sept'},
              {'day': 'Sunday', 'inbed': '12:30pm', 'outbed': '6:30pm', 'hours': 6, 'sef': 100,
               'how_slept': 'well', 'wc': '13th Sept'},
              {'day': 'Monday', 'inbed': '12:30pm', 'outbed': '5:30pm', 'hours': 4, 'sef': 55, 'how_slept': 'bad',
               'wc': '20th Sept'},
              {'day': 'Tuesday', 'inbed': '12:00am', 'outbed': '7:30pm', 'hours': 7, 'sef': 80,
               'how_slept': 'well', 'wc': '20th Sept'},
              {'day': 'Wednesday', 'inbed': '11:45pm', 'outbed': '7:00pm', 'hours': 5, 'sef': 75,
               'how_slept': 'ok', 'wc': '20th Sept'},
              {'day': 'Thursday', 'inbed': '11:45pm', 'outbed': '6:30pm', 'hours': 6, 'sef': 77,
               'how_slept': 'ok', 'wc': '20th Sept'},
              {'day': 'Friday', 'inbed': '11:00pm', 'outbed': '6:00pm', 'hours': 3, 'sef': 33,
               'how_slept': 'bad', 'wc': '20th Sept'},
              {'day': 'Saturday', 'inbed': '1:30pm', 'outbed': '4:30pm', 'hours': 2, 'sef': 44,
               'how_slept': 'bad', 'wc': '20th Sept'},
              {'day': 'Sunday', 'inbed': '12:30pm', 'outbed': '6:30pm', 'hours': 6, 'sef': 100,
               'how_slept': 'well', 'wc': '20th Sept'},
              {'day': 'Monday', 'inbed': '11:30pm', 'outbed': '6:30pm', 'hours': 5, 'sef': 71, 'how_slept': 'ok',
               'wc': '27th Sept'},
              {'day': 'Tuesday', 'inbed': '12:00am', 'outbed': '7:30pm', 'hours': 7, 'sef': 80,
               'how_slept': 'well', 'wc': '27th Sept'},
              {'day': 'Wednesday', 'inbed': '11:30pm', 'outbed': '7:00pm', 'hours': 5, 'sef': 71,
               'how_slept': 'ok', 'wc': '27th Sept'},
              {'day': 'Thursday', 'inbed': '11:45pm', 'outbed': '6:30pm', 'hours': 6, 'sef': 77,
               'how_slept': 'ok', 'wc': '27th Sept'},
              {'day': 'Friday', 'inbed': '11:00pm', 'outbed': '6:00pm', 'hours': 3, 'sef': 33,
               'how_slept': 'bad', 'wc': '27th Sept'},
              {'day': 'Saturday', 'inbed': '11:30pm', 'outbed': '6:30pm', 'hours': 5, 'sef': 71,
               'how_slept': 'ok', 'wc': '27th Sept'},
              {'day': 'Sunday', 'inbed': '12:30pm', 'outbed': '6:30pm', 'hours': 6, 'sef': 100,
               'how_slept': 'well', 'wc': '27th Sept'}, ]
