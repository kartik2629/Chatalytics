import re
import pandas as pd

def preprocess(data):
    # Adjusted pattern for date and time matching based on your chat format
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[APMapm]{2}\s-\s'

    # Remove omitted media mentions from the data before processing
    data = re.sub(r'\b(omitted media|media omitted)\b', '', data, flags=re.IGNORECASE)

    # Split messages and dates
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # Create a DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Convert message_date to datetime
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M %p - ')

    # Rename columns
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Split user and message
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # If user name exists
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # Add additional datetime attributes
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # Define periods for heatmap
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(f'{hour}-00')
        elif hour == 0:
            period.append(f'00-01')
        else:
            period.append(f'{hour:02}-{hour + 1:02}')

    df['period'] = period

    return df
