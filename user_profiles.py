def create_user_profile(df, user):
    user_df = df[df['user'] == user]
    avg_message_length = user_df['message'].str.len().mean()
    most_active_hour = user_df['datetime'].dt.hour.mode()[0]

    profile = {
        "user": user,
        "avg_message_length": avg_message_length,
        "most_active_hour": most_active_hour,
    }
    return profile
