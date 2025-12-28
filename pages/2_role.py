import streamlit as st
import time
import pandas
import numpy as np

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from sidebar import info_logbook, footer, date_range_selector, language_selector
from translations import _, get_language, TRANSLATIONS

st.set_page_config(page_title="GivavLens - Role", page_icon="📔",layout="wide")

# Side Bar
info_logbook()
st.sidebar.header(_("role_sidebar_header"))
st.sidebar.write(_("role_sidebar_description"))
start_date, end_date = date_range_selector()
language_selector()
footer()

# Main page
st.title(":violet[:material/area_chart:] " + _("role_title"))

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

dfr = df.copy()
dfr = dfr.groupby('Fonc.',as_index = True)['Durée'].agg(['sum','count'])
dfr = dfr.rename(columns={"count": "#Nbr de vol", "sum": "Durée de vol"}).sort_values(by=['Fonc.'], ascending=True)
dfr = dfr.reset_index()
dfr['Heures de vol'] = dfr['Durée de vol'].apply(lambda x: '{}h {}m'.format(x.components.days*24 + x.components.hours, x.components.minutes))
total_flights_duration = dfr['Durée de vol'].sum()

st.write(_("role_total", dfr['#Nbr de vol'].sum(), total_flights_duration.components.days*24 + total_flights_duration.components.hours, total_flights_duration.components.minutes ))

# Plot flight hours by role
st.header(_("hours_per_role"),divider="violet")
df_hours = dfr.sort_values(by='Durée de vol', ascending=False)
fig = px.bar(df_hours, x='Durée de vol', y='Fonc.', orientation='h', text='Heures de vol')
fig.update_traces(textposition='outside', hoverinfo='none')
fig.update_xaxes(showticklabels=False, title_text='')
fig.update_yaxes(title_text=_('role_sidebar_header'), autorange='reversed')
st.plotly_chart(fig,width='stretch')

# Plot number of flight by role
st.header(_("flights_per_role"),divider="violet")
df_count = dfr.sort_values(by='#Nbr de vol', ascending=False)
fig = px.bar(df_count, x='#Nbr de vol', y='Fonc.', orientation='h', text='#Nbr de vol')
fig.update_traces(marker_color='SpringGreen',textposition='outside')
fig.update_xaxes(title_text='Number of flights')
fig.update_yaxes(title_text=_('role_sidebar_header'), autorange='reversed')
st.plotly_chart(fig,width='stretch')

# Plot most  used instructors
st.header(_("instructors_used"),divider="violet")
dfi = df.copy()
dfi = dfi[dfi['Fonc.'] == 'Elv']
dfi = dfi.groupby('Commentaire',as_index = True)['Durée'].agg(['sum','count']).sort_values(by=['sum'], ascending=False)
dfi = dfi.reset_index().rename(columns={"count": "#Nbr de vol", "sum": "Durée de vol", 'Commentaire': 'Instructor'})
dfi['Heures de vol'] = dfi['Durée de vol'].apply(lambda x: '{}h {}m'.format(x.components.days*24 + x.components.hours, x.components.minutes))

# Using plotly subplots
fig = make_subplots(rows=1, cols=2,column_widths=[0.6, 0.4],
					horizontal_spacing=0.05, 
					subplot_titles=("<b>" + _('flight_count') + "</b>", "<b>" + _('flight_hours_column') + "</b>"),
					specs=[[{"secondary_y": False}, {"secondary_y": True}]])

dfi = dfi.sort_values(by='Durée de vol', ascending=True)
fig.add_trace(
	go.Bar(x=dfi['Durée de vol'], y=dfi['Instructor'], customdata=dfi['#Nbr de vol'], name="", orientation='h', 
		text=dfi['Heures de vol'],
		texttemplate=_('flight_hours_column') +': %{text}',
		hovertemplate='<b>%{y}</b><br><br>' + _('flight_count') + ' = %{customdata}<br>' + _('flight_hours_column') + '= %{text}'
	), 
	row=1, col=1, secondary_y=False,
)

dfi = dfi.sort_values(by='#Nbr de vol', ascending=True)
fig.add_trace(
	go.Bar(x=dfi['#Nbr de vol'], y=dfi['Instructor'], name="",customdata=dfi['Heures de vol'], marker=dict(color='SpringGreen'), orientation='h',
		text=dfi['#Nbr de vol'] ,textposition='outside',
		hovertemplate='<b>%{y}</b><br><br>' + _('flight_count') + ' = %{x}<br>' + _('flight_hours_column') + ' = %{customdata}'
	),
	row=1, col=2, secondary_y=True,
)
fig.update_layout(showlegend=False)
fig.update_yaxes(showticklabels=False, secondary_y=True)
fig.update_yaxes(title_text=_('instructor'), secondary_y=False)
fig.update_xaxes(showticklabels=False)
st.plotly_chart(fig,width='stretch')

# Display detail
st.header(_('role_breakdown'),divider="violet")
# st.dataframe(df,hide_index=True, width='stretch',)

# Use pandas styler object and HTML conversion to format the table to display
headers = {
	'selector': 'th:not(.index_name)',
	'props': 'background-color: rgb(26, 28, 36); color: rgb(144, 145, 149); font-size: 16px; font-weight: 400;'
}
df_html = dfi.style \
	.hide() \
	.set_properties(subset=['Durée de vol', '#Nbr de vol', 'Heures de vol'], **{'text-align': 'center'}) \
	.relabel_index([_('role_sidebar_header'),  _('flight_duration_column'),  _('flight_count'),_('flight_hours')], axis=1) \
	.set_table_styles([ headers]) \
	.to_html()
st.markdown(df_html, unsafe_allow_html=True)

# Debug
# st.divider()
# st.write(st.session_state)