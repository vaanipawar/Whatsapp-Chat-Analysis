import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import emoji


st.sidebar.title("Whatsapp Chat Analyser")
uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    data = uploaded_file.read().decode("utf-8")
    df = preprocessor.preprocessor(data)


    st.dataframe(df)

    #unique user

    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"overall")
    selected_user = st.sidebar.selectbox("Show analysis wrt" , user_list)



    if st.sidebar.button("Show analysis"):
        # Stats
        num_messages,words,num_media_messages,links  = helper.fetch_stats(selected_user,df)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)

        with col4:
            st.header("Links Shared")
            st.title(links)    

         # busiest user in group
        if selected_user == 'overall':
            st.title('Most Busy User')
            x,new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index,x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

# wordcloud
st.title("Word Cloud")
wordcloud_img = helper.create_wordcloud(selected_user,df)
fig,ax = plt.subplots()
ax.imshow(wordcloud_img)
st.pyplot(fig)

# most common words
most_common_df = helper.most_commmon_words(selected_user,df)
fig,ax= plt.subplots()
ax.barh(most_common_df['word'],most_common_df['count'])
plt.xticks(rotation='vertical')
st.title("most common words")     
st.pyplot(fig)

        
#emoji analysis
emoji_df = helper.emoji_helper(selected_user,df)
st.title("Emoji Analysis")


col1,col2 = st.columns(2)
with col1:
    st.dataframe(emoji_df)
with col2:
    fig,ax = plt.subplots()
    ax.pie(emoji_df['count'], labels=emoji_df['emoji'], autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  
    st.pyplot(fig)


