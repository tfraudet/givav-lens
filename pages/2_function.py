import streamlit as st
import time
import pandas
import numpy as np

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from sidebar import info_logbook,footer

st.set_page_config(page_title="Glider logbook - Fonction", page_icon="📈",layout="wide")

# Side Bar
info_logbook()
st.sidebar.header("Function")
st.sidebar.write("Glider flight statistics by pilot role.")
footer()

# Main page
st.write("# 📈 Function statistics")

if 'logbook' not in st.session_state:
	st.warning("Please upload a CSV using the 'Upload CSV' page before accessing this page.")
	st.stop()

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
st.plotly_chart(fig,width='stretch')

# Plot number of flight by function
st.header('Number of flights per function',divider=True)
fig = px.bar(df, x='#Nbr de vol', y='Fonc.', orientation='h', text='#Nbr de vol')
fig.update_traces(marker_color='SpringGreen',textposition='outside')
fig.update_xaxes(title_text='Number of flights')
fig.update_yaxes(title_text='Function')
st.plotly_chart(fig,width='stretch')

# Plot most  used instructors
st.header('Most used instructors',divider=True)
dfi = st.session_state.logbook
dfi = dfi[dfi['Fonc.'] == 'Elv']
dfi = dfi.groupby('Commentaire',as_index = True)['Durée'].agg(['sum','count']).sort_values(by=['sum'], ascending=True)
dfi = dfi.reset_index().rename(columns={"count": "#Nbr de vol", "sum": "Durée de vol", 'Commentaire': 'Instructor'})
dfi['Heures de vol'] = dfi['Durée de vol'].apply(lambda x: '{}h {}m'.format(x.components.days*24 + x.components.hours, x.components.minutes))

# st.dataframe(dfi,hide_index=True, width='stretch')
# print(dfi.info())	

# col1, col2 = st.columns([0.6,0.4],gap="small")
# with col1:
# 	fig = px.bar(dfi, x='Durée de vol', y='Instructor', orientation='h', text='Heures de vol' , hover_name='Instructor', custom_data=['#Nbr de vol'])
# 	fig.update_traces(
# 		texttemplate='duration is %{text}',
# 		hovertemplate='<b>%{y}</b><br><br>Number of flight = %{customdata[0]}<br>Flight duration = %{text}'
# 	)
# 	fig.update_xaxes(showticklabels=False, title_text='<b>Flight duration</b>')
# 	st.plotly_chart(fig,width='stretch')

# with col2:
# 	fig = px.bar(dfi, x='#Nbr de vol', y='Instructor', orientation='h' , text='#Nbr de vol', hover_name='Instructor',
# 			hover_data={'Instructor': False, 'Heures de vol': True, 'Durée de vol': False, '#Nbr de vol': True})
# 	fig.update_traces(marker_color='SpringGreen',textposition='outside')
# 	fig.update_xaxes(showticklabels=False, title_text='<b>Number of flight</b>')
# 	fig.update_yaxes(showticklabels=False, title_text='')
# 	st.plotly_chart(fig,width='stretch')

# Using plotly subplots
fig = make_subplots(rows=1, cols=2,column_widths=[0.6, 0.4],
					horizontal_spacing=0.05, 
					subplot_titles=("<b>Flight duration</b>", "<b>Number of flight</b>"),
					specs=[[{"secondary_y": False}, {"secondary_y": True}]])
fig.add_trace(
	go.Bar(x=dfi['Durée de vol'], y=dfi['Instructor'], customdata=dfi['#Nbr de vol'], name="", orientation='h', 
		text=dfi['Heures de vol'],
		texttemplate='duration is %{text}',
		hovertemplate='<b>%{y}</b><br><br>Number of flight = %{customdata}<br>Flight duration = %{text}'
	), 
	row=1, col=1, secondary_y=False,
)
fig.add_trace(
	go.Bar(x=dfi['#Nbr de vol'], y=dfi['Instructor'], name="",customdata=dfi['Heures de vol'], marker=dict(color='SpringGreen'), orientation='h',
		text=dfi['#Nbr de vol'] ,textposition='outside',
		hovertemplate='<b>%{y}</b><br><br>Number of flight = %{x}<br>Flight duration = %{customdata}'
	),
	row=1, col=2, secondary_y=True,
)
fig.update_layout(showlegend=False)
fig.update_yaxes(showticklabels=False, secondary_y=True)
fig.update_yaxes(title_text='Instructor', secondary_y=False)
fig.update_xaxes(showticklabels=False)
st.plotly_chart(fig,width='stretch')

# Display detail
st.header('Details hours & number of flights per function',divider=True)
# st.dataframe(df,hide_index=True, width='stretch',)

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

