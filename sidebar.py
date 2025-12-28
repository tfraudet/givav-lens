import streamlit as st
import pandas as pd
import datetime
from translations import _, get_language, TRANSLATIONS

__version__ = "1.0.0"

def language_selector():
	"""Add a language selector in the sidebar."""
	st.sidebar.subheader("Language / Langue")
	
	# Create columns for flag icons
	col1, col2 = st.sidebar.columns(2)
	
	with col1:
		if st.button("🇺🇸 English", key="lang_en", use_container_width=True):
			st.session_state.language = "en"
			st.rerun()
	
	with col2:
		if st.button("🇫🇷 Français", key="lang_fr", use_container_width=True):
			st.session_state.language = "fr"
			st.rerun()

def info_logbook():
	if 'logbook' not in st.session_state:
		st.sidebar.warning(_("logbook_not_loaded"))
	else:
		st.sidebar.success(_("logbook_loaded", len(st.session_state['logbook'])))  

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
	st.sidebar.subheader(_("filters"))
	date_range = st.sidebar.date_input(
		_("date_range"),
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