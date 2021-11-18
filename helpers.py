from functools import wraps
from flask import redirect, session
import pandas as pd
import numpy as np
import datetime
import json
import plotly
import plotly.express as px


def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return func(*args, **kwargs)
    return decorated_function


def process_diary_data(sql_query):
    dataframe = pd.DataFrame(sql_query)

    def get_24h_time(df, col, return_col):

        def split_1(col):
            first_split = pd.to_numeric(col.split(":")[0])
            if "pm" in col:
                return str(first_split + 12)
            elif "12" in col and "am" in col:
                return "00"
            else:
                return str(first_split)

        df['split_1'] = df[col].apply(lambda x: split_1(x))
        df['split_2'] = df[col].apply(lambda x: x.split(":")[1][:len(x.split(":")[1]) - 2])
        # df[return_col] = df['split_1'] + df['split_2']/60
        df[return_col] = df['split_1'] + ":" + df['split_2']
        df = df.drop(['split_1', 'split_2'], axis=1)

        return df

    def get_hours_in_bed(start, end):

        DECIMAL_SCALAR = 60

        def splitter(col):
            split = [pd.to_numeric(i) for i in col.split(":")]
            return split[0], split[1]

        start_h, start_m = splitter(start)
        end_h, end_m = splitter(end)

        start_time = start_h + start_m / DECIMAL_SCALAR
        end_time = end_h + end_m / DECIMAL_SCALAR

        return ((start_time - end_time) + 24) % 24

    def find_digit(x):
        integer = int(''.join([i for i in x if i.isdigit()]))

        return integer / 60 if integer in [15, 30, 45] else integer

    def parse_gaps(x):
        try:
            gap_list = x.split(",")
            gap_ints = [find_digit(i) if "Length" not in i else 0 for i in gap_list]
            return sum(gap_ints)
        except AttributeError:
            return 0

    def get_hours_asleep(hours_in_bed, time_to_fall_asleep, time_to_get_out_bed, gap_duration):
        total_hours = hours_in_bed - time_to_fall_asleep - time_to_get_out_bed - gap_duration
        return 0 if total_hours < 1 else total_hours

    def get_weekday(x):
        weekday_int = datetime.date(*map(int, x.split("-"))).weekday()
        weekday_map = {i: j for i, j in
                       zip(range(7), ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])}

        return weekday_map[weekday_int]

    dataframe = get_24h_time(dataframe, 'in_bed', 'in_bed_24h')
    dataframe = get_24h_time(dataframe, 'out_bed', 'out_bed_24h')
    dataframe['hours_in_bed'] = dataframe.apply(lambda x: get_hours_in_bed(x['out_bed_24h'], x['in_bed_24h']), axis=1)
    dataframe['time_to_fall_decimal'] = dataframe['time_to_fall_asleep'].apply(lambda x: find_digit(x))
    dataframe['time_to_getout_decimal'] = dataframe['time_to_get_out_bed'].apply(lambda x: find_digit(x))
    dataframe['gap_duration_decimal'] = dataframe['gap_lengths'].apply(lambda x: parse_gaps(x))
    dataframe['hours_asleep'] = dataframe.apply(
        lambda x: get_hours_asleep(x['hours_in_bed'], x['time_to_fall_decimal'], x['time_to_getout_decimal'],
                                   x['gap_duration_decimal']), axis=1)
    dataframe['sleep_efficiency'] = np.round(dataframe['hours_asleep'] / dataframe['hours_in_bed'], 1) * 100
    dataframe['weekday'] = dataframe['created_date'].apply(lambda x: get_weekday(x))

    return dataframe


def get_previous_wcs(df) -> list:
    """Returns past four weeks based on week commencing"""
    wc_values = df['wc'].unique().tolist()

    return wc_values


def df_for_diary(df, wc):
    #TODO: rename columns at beginning!

    columns = ['weekday', 'in_bed', 'out_bed', 'hours_asleep', 'sleep_efficiency', 'slept_well', 'wc', 'created_date']
    new_columns = ['day', 'in_bed', 'out_bed', 'hours', 'sef', 'how_slept', 'wc']

    filtered_data = df[df['wc'].isin(wc)].sort_values(by=['created_date'], ascending=False)
    filtered_data = filtered_data[columns].drop(['created_date'], axis=1)
    filtered_data.columns = new_columns
    return filtered_data


def get_mood_data(df):
    columns = ['created_date', 'selected_moods']
    df = df[columns]

    def split_list(x):
        if "," in x:
            return x.split(",")
        else:
            return [x]

    def mood_object(mood, count):
        return {'mood': mood, 'count': count}

    df['selected_moods'] = df['selected_moods'].apply(lambda x: split_list(x))
    df = df.explode('selected_moods')
    #df = df.groupby('created_date')['selected_moods'].value_counts().to_frame('counts').reset_index()
    df = df.groupby('selected_moods').count().reset_index()
    df.columns = ['selected_moods', 'count']
    df = df.sort_values(by="count", ascending=False)
    #return {k: v for k, v in zip(df['selected_moods'], df['count'])}

    return [mood_object(i, j) for i, j in zip(df['selected_moods'], df['count'])]

def this_week_last_week_sef(ordered_week_commencing, diary_table_df):

    this_week, last_week = ordered_week_commencing[-1], ordered_week_commencing[-2]

    def calculate_weekly_sef(week_filter, df):
        filtered_df = df[df['wc'] == week_filter]

        return np.round(filtered_df.hours_asleep.sum()/filtered_df.hours_in_bed.sum()*100, 0)

    return calculate_weekly_sef(this_week, diary_table_df), calculate_weekly_sef(last_week, diary_table_df)


def df_to_dict(df, *columns):

    return df[columns[0]].to_dict('records')


def generate_diary_inputs(diary_table):
    wc_lookup = json.load(open("C:/Users/matth/sleep_app/database/wc_map.json"))

    diary_table_df = process_diary_data(diary_table)
    hours_data = df_to_dict(diary_table_df, ['created_date', 'hours_asleep'])
    efficiency_data = df_to_dict(diary_table_df, ['created_date', 'sleep_efficiency'])
    mood_data = get_mood_data(diary_table_df)
    week_commencing_dates = list(set(get_previous_wcs(diary_table_df)))
    ordered_week_commencing = list(dict(sorted({i: wc_lookup[i] for i in week_commencing_dates}.items(),
                                               key=lambda item: item[1])).keys())
    sleep_data = df_for_diary(diary_table_df, week_commencing_dates).to_dict('records')
    this_week_sef, last_week_sef = this_week_last_week_sef(ordered_week_commencing, diary_table_df)

    return sleep_data, hours_data, efficiency_data, ordered_week_commencing, mood_data, this_week_sef, last_week_sef


def create_moods_chart(mood_data):
    """This was a bit too tricky to do using plotly js"""

    fig = px.bar(mood_data, x="created_date", y="counts", color="selected_moods", color_discrete_sequence=px.colors.sequential.thermal,
                 title="How I felt the next day")

    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)'},
        font=dict(color="white")
    )

    fig.update_yaxes(visible=False)
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=7,
                         label="1w",
                         step="day",
                         stepmode="backward"),
                    dict(count=14,
                         label="2w",
                         step="day",
                         stepmode="backward",
                         ),
                    dict(count=1,
                         label="1m",
                         step="month",
                         stepmode="backward",
                         ),
                    dict(count=6,
                         label="6m",
                         step="month",
                         stepmode="backward"),
                    dict(count=1,
                         label="YTD",
                         step="year",
                         stepmode="todate"),
                    dict(count=1,
                         label="1y",
                         step="year",
                         stepmode="backward"),
                    dict(step="all")
                ]),
                bgcolor= '#000000'
            ),
            rangeslider=dict(
                visible=False
            ),
            type="date",
        )
    )
    fig.update_xaxes(title_text='')

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


