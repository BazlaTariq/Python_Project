import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import scipy

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df,region_df)

st.sidebar.title("120 Years of Olympics")
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete wise Analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " performance in " + str(selected_year) + " Olympics")
    st.table(medal_tally)
if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1 #Since 1906 Olympics isn't officially recogonized by IOC
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]
    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Athletes")
        st.title(athletes)
    with col3:
        st.header("Nations")
        st.title(nations)

    st.title("Nations Participating Over The Years")

    nations_over_time = helper.data_over_time(df, col = 'region')
    fig = px.line(nations_over_time, x='Year', y='count', labels={'Year': 'Edition', 'count': 'Number of Countries'})
    st.plotly_chart(fig)

    st.title("Events Happening Over The Years")

    events_over_time = helper.data_over_time(df, col='Event')
    fig = px.line(events_over_time, x='Year', y='count', labels={'Year': 'Edition', 'count': 'Number of Events'})
    st.plotly_chart(fig)

    st.title("Athletes Participating Over The Years")

    athletes_over_time = helper.data_over_time(df, col='Name')
    fig = px.line(athletes_over_time, x='Year', y='count', labels={'Year': 'Edition', 'count': 'Number of Athletes'})
    st.plotly_chart(fig)

    st.title("Number of events over time")
    fig,ax = plt.subplots(figsize=(10,10))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    plt.xlabel("Year", fontsize=14)  # X-axis label font size
    plt.ylabel("Sport", fontsize=14)  # Y-axis label font size
    st.pyplot(fig)

    st.title("Most Successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    x = helper.most_successful(df, selected_sport)
    st.table(x)

if user_menu == 'Country-wise Analysis':
    st.sidebar.title("Country_wise Analysis")
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country =st.sidebar.selectbox("Select a country",country_list)
    country_df = helper.year_wise_medal_tally(df,selected_country)
    fig = px.line(country_df, x='Year', y='Medal', labels={'Year': 'Edition', 'Medal': 'Number of Medals'})
    st.title(selected_country + " medal tally over the years")
    st.plotly_chart(fig)

    st.title(selected_country + " excels in the following sports")

    pt = helper.country_event_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(15,15))
    ax = sns.heatmap(pt, annot=True, annot_kws={"size": 20})
    plt.xlabel("Year", fontsize=14)  # X-axis label font size
    plt.ylabel("Sport", fontsize=14)  # Y-axis label font size
    plt.xticks(fontsize=15)  # Increase x-axis tick font size
    plt.yticks(fontsize=15)  # Increase y-axis tick font size
    st.pyplot(fig)

    st.title("Top 10 athletes of " + selected_country )

    top10_df = helper.most_successful_country_wise(df, selected_country)
    st.table(top10_df)

if user_menu == 'Athlete wise Analysis':
    athletes_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athletes_df['Age'].dropna().tolist()
    x2 = athletes_df[athletes_df['Medal'] == 'Gold']['Age'].dropna().tolist()
    x3 = athletes_df[athletes_df['Medal'] == 'Silver']['Age'].dropna().tolist()
    x4 = athletes_df[athletes_df['Medal'] == 'Bronze']['Age'].dropna().tolist()
    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    st.title("Distribution of Age")
    fig.update_layout(autosize = False, width = 1000, height = 600)
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athletes_df[athletes_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports (Gold Medalists)")
    st.plotly_chart(fig)

    st.title('Height V Weight')

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df, selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(x = temp_df['Weight'], y= temp_df['Height'], hue = temp_df['Medal'], style = temp_df['Sex'], s = 60)
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)

