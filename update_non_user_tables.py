from sql_utils import SleepDatabase, WEEK_COMMENCING, week_commencing_data

sleep_db = SleepDatabase('database/sleep.db')
sleep_db.table_rendering(WEEK_COMMENCING)


month_hash = {(f"0{str(i)}" if i < 10 else str(i)): j for i, j in zip(list(range(1, 13)), ['Jan', 'Feb', 'Mar', 'Apr',
                                                                                           'May', 'Jun', 'Jul', 'Aug',
                                                                                           'Sept', 'Oct', 'Nov', 'Dec'])}


def update_week_commencing_data(month_hash=month_hash):
    '''Run this to update the week commencing table'''
    wc_dict = week_commencing_data(month_hash)

    for k, v in wc_dict.items():
        sleep_db.update("INSERT or REPLACE INTO week_commencing_ref (created_date, wc) VALUES (?, ?)", (k, v))

update_week_commencing_data()
