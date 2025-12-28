import streamlit as st
import time
import pandas
import numpy as np
import plotly.express as px
from sidebar import info_logbook, footer, date_range_selector, language_selector
from translations import _, get_language, TRANSLATIONS

st.set_page_config(page_title="GivavLens - Aircraft", page_icon="📔",layout="wide")

# Side bar
info_logbook()
st.sidebar.header(_("aircraft_sidebar_header"))
st.sidebar.write(_("aircraft_sidebar_description"))
start_date, end_date = date_range_selector()
language_selector()
footer()

# Main page
st.title(":violet[:material/area_chart:] " + _("aircraft_title"))

if 'logbook' not in st.session_state:
	st.warning(_("logbook_warning"))
	st.stop()

# read the logbook data from the session state
df = st.session_state.logbook

# filter the logbook on start_date and end_date if set
if start_date and end_date:
	df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

# Logbook empty check
if df.empty:
	st.warning(_("aircraft_empty_warning"))
	st.stop()

# group data by aircraft
df = df.groupby('Type',as_index = True)['Durée'].agg(['sum','count'])
df = df.rename(columns={"count": "#Nbr de vol", "sum": "Durée de vol"}).sort_values(by=['Type'], ascending=False)
df = df.reset_index()

df['Heures de vol'] = df['Durée de vol'].apply(lambda x: '{}h {}m'.format(x.components.days*24 + x.components.hours, x.components.minutes))
total_flights_duration = df['Durée de vol'].sum()
st.write(_("aircraft_total", df['#Nbr de vol'].sum(), total_flights_duration.components.days*24 + total_flights_duration.components.hours, total_flights_duration.components.minutes ))

# Plot flight hours by aircraft
st.header(_("hours_per_aircraft"),divider="violet")
df = df.sort_values(by='Durée de vol', ascending=True)
fig = px.bar(df, x='Durée de vol', y='Type', orientation='h', text='Heures de vol', hover_data=[] )
fig.update_traces(textposition='outside', hoverinfo='none', hovertemplate=None)
fig.update_xaxes(showticklabels=False, title_text='')
fig.update_yaxes(title_text= _('glider'))

st.plotly_chart(fig,width='stretch')

# Plot number of flight by aircraft
st.header(_("flights_per_aircraft"),divider="violet")
df = df.sort_values(by='#Nbr de vol', ascending=True)
fig = px.bar(df, x='#Nbr de vol', y='Type', orientation='h', text='#Nbr de vol')
fig.update_traces(marker_color='SpringGreen',textposition='outside', hoverinfo='none', hovertemplate=None)
fig.update_xaxes(title_text=_('flight_count'))
fig.update_yaxes(title_text= _('glider'))
st.plotly_chart(fig,width='stretch')

# Display dataframe detail
st.header(_("aircraft_details"),divider="violet")
# st.dataframe(df,hide_index=True,width='stretch', 
# 	column_config={'Durée de vol' : 'Flight duration', 
# 					'#Nbr de vol' : 'Flight number',
# 					'Type' : '🛩 Aircraft',
# 					'Heures de vol' : 'Flight hours'
# 				}
# 			)

# Use pandas styler object and HTML conversion to format the table to display
headers = {
	'selector': 'th:not(.index_name)',
	'props': 'background-color: rgb(26, 28, 36); color: rgb(144, 145, 149); font-size: 16px; font-weight: 400;'
}
# df_html = df.drop('Durée de vol', axis=1).style \
df_html = df.style \
	.hide() \
	.set_properties(subset=['Durée de vol','#Nbr de vol', 'Heures de vol'], **{'text-align': 'center'}) \
	.relabel_index([_('glider'), _('flight_duration_column'), _('flight_count'),_('flight_hours')], axis=1) \
	.set_table_styles([ headers]) \
	.to_html()
st.markdown(df_html, unsafe_allow_html=True)

# Debug
# st.divider()
# st.write(st.session_state)