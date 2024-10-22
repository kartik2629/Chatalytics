import streamlit as st
import parser
import analysis
import visualizations
import export
import user_profiles
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import pandas as pd

if 'user_activity' not in st.session_state:
    st.session_state.user_activity = []

ADMIN_USER = "admin"
ADMIN_PASS = "admin123"

st.set_page_config(
    page_title="Chatalytics",
    page_icon="icon.png",
    layout="wide"
)

plt.rcParams.update({
    'text.color': 'white',
    'axes.labelcolor': 'white',
    'xtick.color': 'white',
    'ytick.color': 'white',
    'xtick.labelsize': 5,
    'ytick.labelsize': 5,
    'figure.figsize': (12,8)
})

st.sidebar.title("WhatsApp Chat Analyzer")

if not st.session_state.get('is_admin', False):
    admin_section = st.sidebar.expander("Admin Login", expanded=False)
    with admin_section:
        admin_user = st.text_input("Username")
        admin_pass = st.text_input("Password", type="password")
        
        if st.button("Login as Admin"):
            if admin_user == ADMIN_USER and admin_pass == ADMIN_PASS:
                st.success("Logged in as Admin!")
                st.session_state['is_admin'] = True
            else:
                st.error("Invalid credentials")

if st.session_state.get('is_admin', False):
    st.sidebar.title("Admin Panel")

    if st.sidebar.button("Logout"):
        st.session_state['is_admin'] = False
        st.success("Logged out successfully!")

    st.title("Admin Report")
    
    if st.session_state.user_activity:
        activity_df = pd.DataFrame(st.session_state.user_activity, columns=["User", "Analysis Time"])
        st.table(activity_df)
    else:
        st.info("No user activity found.")
else:
    uploaded_file = st.sidebar.file_uploader("Choose a file")
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8")
        df = parser.preprocess(data)

        user_list = df['user'].unique().tolist()
        if 'group_notification' in user_list:
            user_list.remove('group_notification')
        user_list.sort()
        user_list.insert(0, "Overall")

        selected_user = st.sidebar.selectbox("Select User for Analysis", user_list)

        if st.sidebar.button("Show Analysis"):
            st.session_state.user_activity.append(
                {"User": selected_user, "Analysis Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            )

            num_messages, words, num_media_messages, num_links = analysis.fetch_stats(selected_user, df)
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

            st.title("Monthly Timeline")
            timeline = analysis.monthly_timeline(selected_user, df)
            fig, ax = plt.subplots(figsize=(3,1))
            fig.patch.set_alpha(0.0)
            ax.patch.set_alpha(0.5)
            ax.plot(timeline['time'], timeline['message'], color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

            st.title("Daily Timeline")
            daily_timeline = analysis.daily_timeline(selected_user, df)
            fig, ax = plt.subplots(figsize=(4,2))
            fig.patch.set_alpha(0.0)
            ax.patch.set_alpha(0.5)
            ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='yellow')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

            st.title('Activity Map')
            col1, col2 = st.columns(2)

            with col1:
                st.header("Most busy day")
                busy_day = analysis.week_activity_map(selected_user, df)
                fig, ax = plt.subplots(figsize=(3,2))
                fig.patch.set_alpha(0.0)
                ax.patch.set_alpha(0.5)
                ax.bar(busy_day.index, busy_day.values, color='purple')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.header("Most busy month")
                busy_month = analysis.month_activity_map(selected_user, df)
                fig, ax = plt.subplots(figsize=(3,2))
                fig.patch.set_alpha(0.0)
                ax.patch.set_alpha(0.5)
                ax.bar(busy_month.index, busy_month.values, color='orange')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            st.title("Weekly Activity Map")
            user_heatmap = analysis.activity_heatmap(selected_user, df)
            fig, ax = plt.subplots(figsize=(5,3))
            fig.patch.set_alpha(0.0)
            ax.patch.set_alpha(0.5)
            heatmap = sns.heatmap(user_heatmap, cmap="YlGnBu", cbar=True)
            heatmap.figure.colorbar(
                heatmap.collections[0], ax=ax, shrink=0.8, aspect=10).ax.yaxis.label.set_color('white')
            st.pyplot(fig)

            st.title("Wordcloud")
            df_wc = analysis.create_wordcloud(selected_user, df)
            fig, ax = plt.subplots()
            fig.patch.set_alpha(0.0)
            ax.patch.set_alpha(0.5)
            ax.imshow(df_wc, interpolation='bilinear')
            ax.axis("off")
            st.pyplot(fig)

            st.title("Export Analysis Report")
            if st.button("Export as CSV"):
                export.export_to_csv(df, "chat_analysis.csv")
                st.success("Analysis exported as CSV!")
            
            if st.button("Export as PDF"):
                html_content = f"<h1>{selected_user}'s Analysis</h1><p>...</p>"
                export.export_to_pdf(html_content, "chat_analysis.pdf")
                st.success("Analysis exported as PDF!")

            most_common_df = analysis.most_common_words(selected_user, df)
            fig, ax = plt.subplots(figsize=(5,3))
            fig.patch.set_alpha(0.0)
            ax.patch.set_alpha(0.5)
            ax.barh(most_common_df[0], most_common_df[1], color='skyblue')
            plt.xticks(rotation='vertical')
            st.title('Most common words')
            st.pyplot(fig)

            st.title("Keyword Analysis")
            keyword_wc = analysis.keyword_analysis(df, selected_user)
            fig, ax = plt.subplots()
            fig.patch.set_alpha(0.0)
            ax.patch.set_alpha(0.5)
            ax.imshow(keyword_wc)
            ax.axis("off")
            st.pyplot(fig)

            st.title("Emoji Analysis")
            emoji_df = analysis.emoji_analysis(selected_user, df)

            if emoji_df is not None and not emoji_df.empty:
                emoji_df.reset_index(drop=True, inplace=True)
                emoji_df['S.No'] = emoji_df.index + 1

                emoji_df.columns = ['EMOJI', 'COUNT', 'S.NO']
                emoji_df = emoji_df[['S.NO', 'EMOJI', 'COUNT']]

                col1, col2 = st.columns(2)

                with col1:
                    st.dataframe(emoji_df.style.set_properties(**{'color': 'white'}))

                with col2:
                    fig, ax = plt.subplots(figsize=(10,5))
                    fig.patch.set_alpha(0.0)
                    ax.patch.set_alpha(0.5)
                    ax.tick_params(axis='x', labelsize=12)
                    ax.tick_params(axis='y', labelsize=12)
                    ax.pie(emoji_df['COUNT'].head(), labels=emoji_df['EMOJI'].head(),
                        autopct="%0.2f%%", textprops={'color': 'white'})
                    st.pyplot(fig)
            else:
                st.write("No emoji data available or analysis failed.")

            st.title("Sentiment Analysis")
            sentiment_counts = analysis.sentiment_analysis(selected_user, df)
            fig, ax = plt.subplots(figsize=(10,4))
            fig.patch.set_alpha(0.0)
            ax.patch.set_alpha(0.5)
            ax.tick_params(axis='x', labelsize=12)
            ax.tick_params(axis='y', labelsize=12)
            ax.bar(sentiment_counts.index, sentiment_counts.values, color=['green', 'red', 'gray'])
            st.pyplot(fig)
