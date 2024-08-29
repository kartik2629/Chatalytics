import re

def clean_data(df):
    df['message'] = df['message'].apply(lambda x: re.sub(r"omitted media|media omitted", "", x))
    return df
