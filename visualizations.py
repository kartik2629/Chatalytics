import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx

def plot_message_frequency(df, time_unit='hour'):
    if time_unit == 'hour':
        df['hour'] = df['datetime'].dt.hour
        freq = df.groupby('hour').size()
    elif time_unit == 'day':
        df['day'] = df['datetime'].dt.day_name()
        freq = df.groupby('day').size()

    fig, ax = plt.subplots()
    freq.plot(kind='bar', ax=ax, color='blue')
    ax.set_xlabel(f'Messages per {time_unit}')
    ax.set_ylabel('Frequency')
    return fig

def plot_emoji_usage(emoji_df):
    fig, ax = plt.subplots()
    emoji_df.plot(kind='bar', ax=ax, x=0, y=1, color='green')
    ax.set_xlabel('Emoji')
    ax.set_ylabel('Frequency')
    return fig

def plot_user_interaction(df):
    interactions = df.groupby(['user', 'mentioned_user']).size().unstack(fill_value=0)
    G = nx.from_pandas_adjacency(interactions)
    fig, ax = plt.subplots()
    nx.draw_networkx(G, ax=ax, with_labels=True, node_color='lightblue', edge_color='gray')
    return fig
