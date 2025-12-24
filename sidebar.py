import streamlit as st
import pandas as pd
import datetime

__version__ = "1.0.0"

def info_logbook():
	if 'logbook' not in st.session_state:
		st.sidebar.warning("No glider logbook loaded.")
	else:
		st.sidebar.success("Logbook loaded with {} flights.".format(len(st.session_state['logbook'])))  

	# st.sidebar.write(st.session_state)

def update_data_range():
    # Transfer the widget value to our persistent variable
	st.session_state.date_range = st.session_state.widget_data_range

def date_range_selector():
	"""Add a date range selector in the sidebar based on logbook data."""
	if 'logbook' not in st.session_state:
		return None, None
		
	# Get min and max dates
	df = st.session_state['logbook']
	min_date = df['Date'].min().date()
	# max_date = df['Date'].max().date()
	max_date = datetime.datetime.now().date()

	# Ensure date_range is always initialized (handles page navigation resets)
	if 'date_range' not in st.session_state:
		st.session_state['date_range'] = (min_date, max_date)
	
	# Create date range selector
	st.sidebar.subheader("Filters")
	date_range = st.sidebar.date_input(
		"Select Date Range",
		value=st.session_state.date_range,
		min_value=min_date,
		max_value=max_date, 
		key='widget_data_range',
		format="DD/MM/YYYY",
		on_change=update_data_range
	)
	
	# Handle single date vs date range
	if len(st.session_state.date_range) == 2:
		start_date, end_date = st.session_state['date_range']
	else:
		start_date = st.session_state['date_range'][0]
		end_date = st.session_state['date_range'][0]
		st.sidebar.write('from', start_date, ' to ', end_date)
	
	start_date = pd.to_datetime(start_date)
	end_date = pd.to_datetime(end_date)

	return start_date, end_date

def footer():
	st.sidebar.divider()
	material_favorote_html = '<span role="img" aria-label="favorite icon" style="display: inline-block; font-family: &quot;Material Symbols Rounded&quot;; font-weight: 400; user-select: none; vertical-align: bottom; white-space: nowrap; overflow-wrap: normal;">favorite</span>'

	st.sidebar.image('img/acph-logo-v2017-gray.png', width=100)
	st.sidebar.html('Made with <span style="color: green">{}</span> by <a href="https://aeroclub-issoire.fr/">ACPH</a> - version {}'.format(material_favorote_html, __version__))