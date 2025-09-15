from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extractor = URLExtract()
def fetch_stats(selected_user, df):

    if selected_user != 'overall':
        df = df[df['user'] == selected_user]
     # num of messages
    num_messages = df.shape[0]
     # num of words
    words =[]
    for message in df['user_message']:
        words.extend(message.split())
    

   #  number of media messages  
    num_media_messages = df[df['user_message'].str.contains(r"<Media omitted>|media omitted|\[Media omitted\]", case=False, na=False)].shape[0]

    
    # number of links
    links = []
    for message in df['user_message']:
        urls = extractor.find_urls(message)
        
        filtered_urls = [url for url in urls if url.startswith("http://") or url.startswith("https://")]
        links.extend(filtered_urls)

    
    return num_messages,len(words),num_media_messages,len(links)


def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'precent'})
    return x,df

def create_wordcloud(selected_user, df):
    f = open(r"C:\Users\roshn\Downloads\stop_hinglish.txt",'r')
    stop_words = f.read()
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['user_message'] != '<media omitteed>\n']

    words =[]
    for message in temp['user_message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    text = temp['user_message'].str.cat(sep=" ")
    wc = WordCloud(background_color='white',width=500,height=500,min_font_size=10)
    wc.generate(text)
    return wc.to_image()

def most_commmon_words(selected_user,df):

    f = open(r"C:\Users\roshn\Downloads\stop_hinglish.txt",'r')
    stop_words = f.read()
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['user_message'] != '<media omitteed>\n']

    words =[]
    for message in temp['user_message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20), columns=['word', 'count'])
    return most_common_df
def emoji_helper(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['user_message']:
        emojis_in_msg = emoji.emoji_list(message)
        for item in emojis_in_msg:
            emojis.append(item['emoji'])

    emoji_counts = Counter(emojis).most_common(10)
    emoji_df = pd.DataFrame(emoji_counts, columns=['emoji', 'count'])

    return emoji_df