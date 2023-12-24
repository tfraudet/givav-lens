import streamlit as st
import time
import pandas
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Glider logbook - Fonction", page_icon="📈",layout="wide")

st.write("# 📈 Function statistics")
st.sidebar.header("Function")

# read the logbook data from the session state
df = st.session_state.logbook

df = df.groupby('Fonc.',as_index = True)['Durée'].agg(['sum','count'])
df = df.rename(columns={"count": "#Nbr de vol", "sum": "Durée de vol"}).sort_values(by=['Fonc.'], ascending=True)
df = df.reset_index()
df['Heures de vol'] = df['Durée de vol'].apply(lambda x: '{}h {}m'.format(x.components.days*24 + x.components.hours, x.components.minutes))
total_flights_duration = df['Durée de vol'].sum()

st.write('\nFor a total of :green[{}] flight in :green[{}] hours and :green[{}] minutes'.format(df['#Nbr de vol'].sum(), total_flights_duration.components.days*24 + total_flights_duration.components.hours, total_flights_duration.components.minutes ))

# Plot flight hours by function
st.header('Flight hours per function',divider=True)
fig = px.bar(df, x='Durée de vol', y='Fonc.', orientation='h', text='Heures de vol', )
fig.update_traces(textposition='outside', hoverinfo='none')
fig.update_xaxes(showticklabels=False, title_text='')
fig.update_yaxes(title_text='Function')
st.plotly_chart(fig,use_container_width=True)

# Plot number of flight by function
st.header('Number of flights per function',divider=True)
fig = px.bar(df, x='#Nbr de vol', y='Fonc.', orientation='h', text='#Nbr de vol')
fig.update_traces(marker_color='SpringGreen',textposition='outside')
fig.update_xaxes(title_text='Number of flights')
fig.update_yaxes(title_text='Function')
st.plotly_chart(fig,use_container_width=True)

# Display detail
st.header('Details hours & number of flights per function',divider=True)
# st.dataframe(df,hide_index=True, use_container_width=True)

# Use pandas styler object and HTML conversion to format the table to display
headers = {
	'selector': 'th:not(.index_name)',
	'props': 'background-color: rgb(26, 28, 36); color: rgb(144, 145, 149); font-size: 16px; font-weight: 400;'
}
df_html = df.style \
	.hide() \
	.set_properties(subset=['Durée de vol', '#Nbr de vol', 'Heures de vol'], **{'text-align': 'center'}) \
	.relabel_index(["Function", "Flight duration", 'Number of flights', "Flight hours"], axis=1) \
	.set_table_styles([ headers]) \
	.to_html()
st.markdown(df_html, unsafe_allow_html=True)