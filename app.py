import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout='wide')
st.title('Titanic Dashboard')

df = pd.read_csv('titani_data.csv')
st.write(df)
# print(df.info())
df['Embarked'] = df['Embarked'].fillna('Unknown')

# get unique values for embarked port
embarked_port = list(df['Embarked'].unique())
gender = list(df['Sex'].unique())

col1, col2 = st.columns([1,1])
selected_port = col1.selectbox(options=embarked_port,
                               label='Select a port')
selected_gender = col2.selectbox(options=gender,
                                 label='Select a gender')

# Filter dataframe based on the widget values
df_plot = df[df['Embarked'] == selected_port]
df_plot = df_plot[df_plot['Sex'] == selected_gender]

hist_plot = px.histogram(data_frame=df_plot,
                        template='seaborn',
                        color='Survived',
                        title='Distribution of Age',
                        facet_col='Survived',
                        x='Age')
col1.plotly_chart(hist_plot)

# add a pie chart
# Create the pie chart using plotly express
df_plot_pie = df_plot.loc[:, ['PassengerId', 'Survived']].groupby(['Survived']).count().reset_index()
df_plot_pie.rename({'PassengerId': 'Count of passengers'},
                   axis='columns',
                   inplace=True)

pie_plot = px.pie(data_frame=df_plot_pie,
                  template='seaborn',
                  title='Count of passengers that survived',
                  values='Count of passengers',
                  names='Survived')
# attach to the dashboard
col2.plotly_chart(pie_plot)

# add a boxplot of the fare prices
# wrangle the data
# create the visual
box_plot = px.box(data_frame=df_plot,
                  y='Fare',
                  template='seaborn',
                  color='Survived',
                  title='Distribution of fare across survival status',
                  x='Survived')
# attach to the dashboard
st.plotly_chart(box_plot)
