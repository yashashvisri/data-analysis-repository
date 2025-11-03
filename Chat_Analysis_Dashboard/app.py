import streamlit as st
import pandas as pd
import preprocess  
import helper       
import matplotlib.pyplot as plt
import seaborn as sns
import os 


st.set_page_config(layout="wide", page_title="Chat Analyzer")


plt.style.use('seaborn-v0_8-bright')


st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .stMetricValue {
        color: #00BCD4; /* Bright cyan for metric values */
    }
    .stMetricLabel {
        color: #B0B3B8; /* Lighter grey for metric labels */
    }
    .stButton>button {
        background-color: #00BCD4;
        color: white;
        border-radius: 8px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #0097A7;
        color: white;
    }
    .stHeader, .stTitle, .stSubheader {
        color: #FAFAFA;
    }
    /* Sidebar styling */
    .st-emotion-cache-16txtl3 {
        background-color: #1A1C24;
    }
    /* Matplotlib figure background */
    .stPlot, .stImage {
        background-color: transparent;
    }
    </style>
    """, unsafe_allow_html=True)


st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a chat file (_chat.txt)")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    
    try:
        df = preprocess.preprocess(data)
    except Exception as e:
        st.error(f"Error in preprocessing: {e}")
        st.error("Please ensure your preprocessor.py file is correct and the uploaded file is a valid WhatsApp chat.")
        st.stop()

   
    if not df.empty:
        user_list = df['user'].unique().tolist()
        if 'group_notification' in user_list:
            user_list.remove('group_notification')
        user_list.sort()
        user_list.insert(0, "Overall")
        
        selected_user = st.sidebar.selectbox("Show analysis for", user_list)

       
        if st.sidebar.button("Show Analysis"):

           
            try:
                df['year'] = df['date'].dt.year
                df['month_num'] = df['date'].dt.month
                df['month'] = df['date'].dt.month_name()
                df['day'] = df['date'].dt.day
                df['day_name'] = df['date'].dt.day_name()
                df['hour'] = df['date'].dt.hour
                df['minute'] = df['date'].dt.minute
                df['only_date'] = df['date'].dt.date
                df['period'] = df['hour'].apply(lambda h: f"{h:02d}-{((h+1)%24):02d}")
            except AttributeError as e:
                st.error(f"Error creating date columns. Is the 'date' column correctly formatted in your preprocessor? Error: {e}")
                st.stop()
            except Exception as e:
                st.error(f"An unexpected error occurred while creating date columns: {e}")
                st.stop()

           

            st.title(f"WhatsApp Chat Analysis for: {selected_user}")

            
            st.header("Top Statistics")
            num_messages, num_words, num_media, num_links = helper.fetch_stats(selected_user, df)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Messages", num_messages)
            with col2:
                st.metric("Total Words", num_words)
            with col3:
                st.metric("Media Shared", num_media)
            with col4:
                st.metric("Links Shared", num_links)

            st.header("Timelines")
            plt.rcParams['text.color'] = '#FAFAFA'
            plt.rcParams['axes.labelcolor'] = '#FAFAFA'
            plt.rcParams['xtick.color'] = '#FAFAFA'
            plt.rcParams['ytick.color'] = '#FAFAFA'

            # Monthly Timeline
            st.subheader("Monthly Timeline")
            timeline = helper.monthly_timeline(selected_user, df)
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(timeline['time'], timeline['message'], color='#00BCD4') # Cyan
            ax.set_facecolor('#1A1C24') 
            fig.set_facecolor('#0E1117') 
            plt.xticks(rotation='vertical')
            fig.tight_layout()
            st.pyplot(fig)

            # Daily Timeline
            st.subheader("Daily Timeline")
            daily_timeline = helper.daily_timeline(selected_user, df)
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='#E91E63') # Pink
            ax.set_facecolor('#1A1C24')
            fig.set_facecolor('#0E1117')
            plt.xticks(rotation='vertical')
            fig.tight_layout()
            st.pyplot(fig)

            # --- Activity Maps (2 Columns) ---
            st.header("Activity Maps")
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Most Busy Day")
                busy_day = helper.week_activity_map(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_day.index, busy_day.values, color='#9C27B0')
                ax.set_facecolor('#1A1C24')
                fig.set_facecolor('#0E1117')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.subheader("Most Busy Month")
                busy_month = helper.month_activity_map(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_month.index, busy_month.values, color='#FF9800') 
                ax.set_facecolor('#1A1C24')
                fig.set_facecolor('#0E1117')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            # --- Weekly Heatmap (Full Width) ---
            st.header("Weekly Activity Heatmap")
            try:
                user_heatmap = helper.activity_heatmap(selected_user, df)
                fig, ax = plt.subplots(figsize=(10, 5))
                ax = sns.heatmap(user_heatmap, cmap='viridis') 
                fig.set_facecolor('#0E1117')
                st.pyplot(fig)
            except Exception as e:
                st.error(f"Error generating heatmap: {e}")


            # --- Busy Users (Only for 'Overall') ---
            if selected_user == 'Overall':
                st.header("User Analysis")
                col1, col2 = st.columns(2)
                
                x, new_df = helper.most_busy_users(df)
                with col1:
                    st.subheader("Most Busy Users (Top 5)")
                    fig, ax = plt.subplots()
                    ax.bar(x.index, x.values, color='#F44336') # Red
                    ax.set_facecolor('#1A1C24')
                    fig.set_facecolor('#0E1117')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)
                with col2:
                    st.subheader("User Contribution (%)")
                    # Style the dataframe to match dark theme
                    st.dataframe(new_df.style.set_properties(**{
                        'background-color': '#1A1C24',
                        'color': '#FAFAFA',
                        'border-color': '#0E1117'
                    }))

            # --- WordCloud (Full Width) ---
            st.header("Word Cloud")
            try:
                df_wc = helper.create_wordcloud(selected_user, df)
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.imshow(df_wc)
                ax.axis('off')
                fig.set_facecolor('#0E1117')
                st.pyplot(fig)
            except FileNotFoundError:
                st.error("Error: 'stop_hinglish.txt' not found. Please add the file to your project directory.")
            except Exception as e:
                st.error(f"Error creating WordCloud: {e}")

            # --- Detailed Analysis (2 Columns) ---
            st.header("Detailed Analysis")
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Most Common Words")
                try:
                    most_common_df = helper.most_common_words(selected_user, df)
                    
                    if not most_common_df.empty:
                        fig, ax = plt.subplots()
                        ax.barh(most_common_df['word'], most_common_df['count'], color='#2196F3') # Blue
                        ax.set_facecolor('#1A1C24')
                        fig.set_facecolor('#0E1117')
                        st.pyplot(fig)
                    else:
                        st.write("No common words found.")
                except FileNotFoundError:
                     st.error("Error: 'stop_hinglish.txt' not found for common words.")
                except Exception as e:
                    st.error(f"Error creating common words chart: {e}")

            with col2:
                st.subheader("Emoji Analysis")
                emoji_df = helper.emoji_helper(selected_user, df)
                
                if not emoji_df.empty:
                    fig, ax = plt.subplots()
                    # Use a color palette
                    colors = sns.color_palette('bright', n_colors=10)
                    ax.pie(emoji_df['count'].head(10), labels=emoji_df['emoji'].head(10), autopct="%0.2f", colors=colors)
                    fig.set_facecolor('#0E1117')
                    st.pyplot(fig)
                else:
                    st.write("No emojis found.")

        else:
            st.info("Click 'Show Analysis' in the sidebar to begin.")
    else:
        st.error("Preprocessing failed. The DataFrame is empty. Please check your file.")
else:
    st.info("Please upload a WhatsApp _chat.txt file to get started.")

