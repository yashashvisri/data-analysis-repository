## WhatsApp Chat Analyzer

A simple and powerful web application built with Streamlit to analyze, visualize, and gain insights from your WhatsApp chat exports.

This tool transforms your raw _chat.txt file into an interactive dashboard, allowing you to explore statistics, user activity, common words, emoji usage, and more.



## 🚀 Features

This dashboard provides a detailed analysis of both group chats and individual chats:

Top Statistics Cards:

Total Messages

Total Words

Total Media Shared

Total Links Shared

Timeline Analysis:

Monthly Timeline: Visualize chat frequency over different months and years.

Daily Timeline: See a day-by-day breakdown of chat activity.

Activity Analysis:

Activity Heatmap: A weekly heatmap showing the most active time slots of the day and days of the week.

Most Busy Day: A bar chart showing the most active day of the week.

Most Busy Month: A bar chart showing the most active month.

User Analysis (Overall View):

Most Busy Users: A bar chart identifying the top 5 most active users.

User Contribution: A data table showing the percentage contribution of each user.

Content Analysis:

WordCloud: A word cloud of the most frequently used words (ignoring "stop words").

Most Common Words: A horizontal bar chart of the top 20 most common words.

Emoji Analysis: A pie chart showing the top 10 most used emojis.


## 🛠️ File Structure

The project is organized into three main Python files for modularity:

app.py: The main Streamlit file that builds and runs the web application frontend.

preprocessor.py: A utility file that takes the raw WhatsApp export file and preprocesses it into a clean Pandas DataFrame.

helper.py: A file containing all the core analysis functions (fetching stats, creating plots, etc.) that are called by app.py.

stop_hinglish.txt: A text file containing a list of "stop words" (common words in Hindi/English) to be excluded from the word cloud and word frequency analysis.



##🔧 How to Use

To run this project locally, follow these steps:

Clone the repository:

git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
cd YOUR_REPO_NAME


Install the required dependencies:
Make sure you have Python 3.8+ installed.

pip install -r requirements.txt


(You will need to create a requirements.txt file. See dependencies below)

Run the Streamlit app:

streamlit run app.py

Open the app:
Your browser will automatically open to http://localhost:8501.

Upload your file:
Use the sidebar to upload your WhatsApp _chat.txt export file and click "Show Analysis".


## 📦 Dependencies

You will need to create a requirements.txt file with the following libraries:

streamlit
pandas
matplotlib
seaborn
wordcloud
emoji
urlextract


## ✨ Future Improvements

Sentiment Analysis on messages.

More granular time-of-day analysis.

Support for different chat export languages.
