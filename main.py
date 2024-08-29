import streamlit as st
import parser
import analysis
import visualizations
import export
import user_profiles
import matplotlib.pyplot as plt
import seaborn as sns


st.set_page_config(
    page_title="Chatalytics",
    page_icon="icon.png",
    layout="wide"
)


# Set global styles for plots
plt.rcParams.update({
    'text.color': 'white',
    'axes.labelcolor': 'white',
    'xtick.color': 'white',
    'ytick.color': 'white',
    'figure.figsize': (6, 4)
})

st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = parser.preprocess(data)

    # Fetch unique users
    user_list = df['user'].unique().tolist()

    # Check if 'group_notification' is in the list before removing
    if 'group_notification' in user_list:
        user_list.remove('group_notification')

    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Select User for Analysis", user_list)

    if st.sidebar.button("Show Analysis"):

        # Stats Area
        num_messages, words, num_media_messages, num_links = analysis.fetch_stats(
            selected_user, df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)

        # Monthly Timeline
        st.title("Monthly Timeline")
        timeline = analysis.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        fig.patch.set_alpha(0.0)  # Transparent figure background
        ax.patch.set_alpha(0.5)    # Semi-transparent axes background
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily Timeline
        st.title("Daily Timeline")
        daily_timeline = analysis.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        fig.patch.set_alpha(0.0)
        ax.patch.set_alpha(0.5)
        ax.plot(daily_timeline['only_date'],
                daily_timeline['message'], color='yellow')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # # Message Frequency Analysis
        # st.title("Message Frequency Analysis")
        # freq_fig = visualizations.plot_message_frequency(df, time_unit='hour')
        # st.pyplot(freq_fig)

        # # Advanced Emoji Analysis
        # st.title("Advanced Emoji Analysis")
        # emoji_df = analysis.emoji_analysis(selected_user, df)
        # emoji_fig = visualizations.plot_emoji_usage(emoji_df)
        # st.pyplot(emoji_fig)

        # # User Interaction Map
        # st.title("User Interaction Map")
        # interaction_fig = visualizations.plot_user_interaction(df)
        # st.pyplot(interaction_fig)

        # Activity Map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = analysis.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            fig.patch.set_alpha(0.0)
            ax.patch.set_alpha(0.5)
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = analysis.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            fig.patch.set_alpha(0.0)
            ax.patch.set_alpha(0.5)
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # Weekly Activity Map
        st.title("Weekly Activity Map")
        user_heatmap = analysis.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        fig.patch.set_alpha(0.0)
        ax.patch.set_alpha(0.5)
        heatmap = sns.heatmap(user_heatmap, cmap="YlGnBu", cbar=True)
        heatmap.figure.colorbar(
            heatmap.collections[0], ax=ax, shrink=0.8, aspect=10).ax.yaxis.label.set_color('white')
        st.pyplot(fig)

        # WordCloud
        st.title("Wordcloud")
        df_wc = analysis.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        fig.patch.set_alpha(0.0)
        ax.patch.set_alpha(0.5)
        ax.imshow(df_wc, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)

         # Export Analysis Report
        st.title("Export Analysis Report")
        if st.button("Export as CSV"):
            export.export_to_csv(df, "chat_analysis.csv")
            st.success("Analysis exported as CSV!")
        
        if st.button("Export as PDF"):
            # Generate HTML from the analysis, then export to PDF
            html_content = f"<h1>{selected_user}'s Analysis</h1><p>...</p>"
            export.export_to_pdf(html_content, "chat_analysis.pdf")
            st.success("Analysis exported as PDF!")

        # # Custom User Profiles
        # st.title("User Profile")
        # profile = user_profiles.create_user_profile(df, selected_user)
        # st.write(f"Average Message Length: {profile['avg_message_length']}")
        # st.write(f"Most Active Hour: {profile['most_active_hour']}")

        # Most common words
        most_common_df = analysis.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        fig.patch.set_alpha(0.0)
        ax.patch.set_alpha(0.5)
        ax.barh(most_common_df[0], most_common_df[1], color='skyblue')
        plt.xticks(rotation='vertical')
        st.title('Most common words')
        st.pyplot(fig)

         # Keyword Analysis
        st.title("Keyword Analysis")
        keyword_wc = analysis.keyword_analysis(df, selected_user)
        fig, ax = plt.subplots(figsize=(14, 10))
        fig.patch.set_alpha(0.0)
        ax.patch.set_alpha(0.5)
        ax.imshow(keyword_wc)
        ax.axis("off")
        st.pyplot(fig)

        # Emoji Analysis
        st.title("Emoji Analysis")
        emoji_df = analysis.emoji_analysis(selected_user, df)
        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df.style.set_properties(**{'color': 'white'}))

        with col2:
            fig, ax = plt.subplots()
            fig.patch.set_alpha(0.0)
            ax.patch.set_alpha(0.5)
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(),
                   autopct="%0.2f", textprops={'color': 'white'})
            st.pyplot(fig)

        # Sentiment Analysis
        #st.title("Sentiment Analysis")
        #df, sentiment_summary = analysis.sentiment_analysis(df)
        
        # # Display sentiment summary
        #st.subheader("Sentiment Summary")
        #st.bar_chart(sentiment_summary)
        # Sentiment Analysis
        st.title("Sentiment Analysis")
        sentiment_counts = analysis.sentiment_analysis(selected_user, df)
        fig, ax = plt.subplots()
        fig.patch.set_alpha(0.0)
        ax.patch.set_alpha(0.5)
        ax.bar(sentiment_counts.index, sentiment_counts.values, color=['green', 'red', 'gray'])
        st.pyplot(fig)

