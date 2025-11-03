import re
import pandas as pd
def preprocess(data):
    pattern = r'^(\d{1,2}/\d{1,2}/\d{2,4}),\s(\d{1,2}:\d{2}\s(AM|PM))\s-\s(.*?):\s(.*)$'

    messages = re.split(pattern, data, re.MULTILINE)

    dates = re.findall(pattern, data)[1:]

    pattern = r'^(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s(?:AM|PM)\s-\s)'
    


    split_data = re.split(pattern, data, flags=re.M)



    dates = []
    messages = []


    for i in range(1, len(split_data), 2):
        date_item = split_data[i]
        message_item = split_data[i+1].strip() 
    
        dates.append(date_item)
        messages.append(message_item)




    df = pd.DataFrame({'user_message': messages, 'message_date': dates})


    df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %I:%M %p - ')


    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []

    pattern = r'([\w\W]+?):\s' 

    for message in df['user_message']:
   
        entry = re.split(pattern, message)
    
   
        if entry[1:]: 
       
            users.append(entry[1])
       
            messages.append(entry[2].strip()) 
        else:
        
            users.append('group_notification')
            messages.append(entry[0].strip()) 

    df['user'] = users
    df['message'] = messages


    df.drop(columns=['user_message'], inplace=True)


    df['year'] = df['date'].dt.year

# Extract 'month' (as the month name, e.g., "July")
    df['month'] = df['date'].dt.month_name()

    # Extract 'day'
    df['day'] = df['date'].dt.day

    # Extract 'hour'
    df['hour'] = df['date'].dt.hour

    # Extract 'minute'
    df['minute'] = df['date'].dt.minute

    df['month_num'] = df['date'].dt.month

    df['only_date'] = df['date'].dt.date

    df['day_name'] = df['date'].dt.day_name()

    df['period'] = df['hour'].apply(lambda h: f"{h:02d}-{((h+1)%24):02d}")

    return df 