import re
import pandas as pd

def preprocessor(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4}, \s*\d{1,2}:\d{2}[\u202f ]?[ap]m - '

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    dates = [d.replace('\u202f', ' ').replace('-', '') for d in dates]

    df = pd.DataFrame({'date_time': dates, 'message': messages})
    df['date_time'] = pd.to_datetime(df['date_time'])

    users = []
    messages = []
    for msg in df['message']:
        entry = re.split(r'^([^:]+):\s', msg, maxsplit=1)

        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(msg)
    df['user'] = users
    df['user_message'] = messages
    df.drop(columns=['message'], inplace=True)


    df[df['user_message'] == "null\n"]
    df['user_message'] = df['user_message'].str.strip()
    df = df[df['user_message'] != "null"]

    df = df.copy()
    df['year'] = df['date_time'].dt.year
    df['month'] = df['date_time'].dt.month_name()
    df['day'] = df['date_time'].dt.day
    df['hour'] = df['date_time'].dt.hour
    df['minute'] = df['date_time'].dt.minute

    return df





