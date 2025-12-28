import time
import streamlit as st
from givav.scrape import scrappe_logbook
from glider_utils import parse_csv, to_dataframe
from sidebar import info_logbook, footer, language_selector
from translations import _, get_language, TRANSLATIONS

import requests
from datetime import datetime
from contextlib import contextmanager, redirect_stdout
from io import StringIO

import pandas as pd

# See https://discuss.streamlit.io/t/cannot-print-the-terminal-output-in-streamlit/6602/2
@contextmanager
def st_capture(output_func):
	with StringIO() as stdout, redirect_stdout(stdout):
		old_write = stdout.write

		def new_write(string):
			ret = old_write(string)
			output_func(stdout.getvalue())
			return ret
		
		stdout.write = new_write
		yield

@st.cache_data(show_spinner="Fetching data from CSV file...")
def upload_data(file_like):
	return parse_csv(file_like)

def update_login_info():
	st.session_state.givav_username = st.session_state.widget_givav_username
	st.session_state.givav_password = st.session_state.widget_givav_password

def init_login_info():
	st.session_state.givav_username = ''
	st.session_state.givav_password = ''

@st.fragment
def ui_givav_sync():
	def givav_synchronize():
		with st.spinner("Wait for it...", show_time=True):
			# with st.container(height=400,border=False):
			with st.container(border=False):
				output = st.empty()
				with st_capture(output.code):
					logbook = scrappe_logbook(st.session_state.givav_username, st.session_state.givav_password)

		# if logbook is not an empty list
		if logbook:
			st.session_state['logbook'] =  to_dataframe(logbook)
			st.session_state['givav'] = True

	if 'givav' not in st.session_state:
		st.session_state['givav'] = False 

	if st.session_state['givav']:
		# st.success("Connected to Smart'Glide. Logbook imported successfully.")
		st.write(_("givav_sync_status_connected", st.session_state.givav_username))

		if st.button(_("givav_resync_button")):
			try:
				givav_synchronize()

				# st.rerun(scope='fragment')
				st.rerun(scope='app')
			except Exception as e:
				st.error(f"{_('givav_resync_error')}: {e}")
		
		if st.button(_("givav_disconnect_button")):
			st.session_state['givav'] = False
			if 'logbook' in st.session_state:
				del st.session_state['logbook']
			init_login_info()
			# st.rerun(scope='fragment')
			st.rerun(scope='app')
	else:
		st.write(_("givav_sync_status_disconnected"))  # Empty column for spacing

		with st.form("giva_form_connect"):
			st.text_input(_("givav_username_label"), key="widget_givav_username")
			st.text_input(_("givav_password_label"), type="password", key="widget_givav_password")

			submitted = st.form_submit_button(_("givav_connect_button"))
			# Simulate connection and data fetching
			if submitted:
				try:
					update_login_info()
					givav_synchronize()

					if 'logbook' in st.session_state:
						st.rerun(scope='app')
				except Exception as e:
					st.error(f"{_('givav_connect_error')}: {e}")

st.set_page_config(
	page_title="GivavLens",
	page_icon="📔",
	layout="wide",
)

# Debug
# st.write(st.session_state)
# st.divider()

# Language selector
language_selector()

# Main page
st.title(_("welcome_title"))
if 'logbook' not in st.session_state:
	st.info(_("logbook_info"))
info_logbook()
footer()

# Option#1:  upload glider logbook as csv file
st.subheader(_("upload_subtitle"))

with st.expander(_("csv_format_help")):
	st.markdown("""
### Expected CSV Format
The CSV file must be **semicolon-separated** (`;`) with the following columns:

| Column | Description |
|--------|-------------|
| **Date** | Flight date (DD/MM/YYYY) |
| **Immat.** | Aircraft registration (e.g., F-CIAT) |
| **Type** | Aircraft type (e.g., ASK 21, ALLIANCE 34) |
| **Catégorie** | Category (e.g., Planeur) |
| **Fonc.** | Function (e.g., Elv = training, Tol = towing pilot) |
| **Nat.** | Nature (e.g., Loc = rental) |
| **Lanc.** | Launch method (e.g., R = auto-tow) |
| **Décol.** | Departure time (HH:MM) |
| **Durée** | Flight duration (HH:MM) |
| **Montagne** | Mountain flight (OUI/NON) |
| **Lieu** | Location |
| **Commentaire** | Comments |
| **Club** | Club code |
| **Abréviation** | Club abbreviation |
| **Nom** | Pilot name |
| **Durée Compute** | Computed duration (auto-generated) |
| **Année** | Year |

### Example
```
Date;Immat.;Type;Catégorie;Fonc.;Nat.;Lanc.;Décol.;Durée;Montagne;Lieu;Commentaire;Club;Abréviation;Nom;Durée Compute;Année
16/10/2022;F-CJDT;JANUS C;Planeur;Cdt;Loc;R;14:33;00:45;NON;LFHA-Aérodrome d'Issoire - Le Broc;;836301;ISSOIRE ACPH;Aéro-club Pierre Herbaud;0h 45m;2022
16/10/2022;F-CJDT;JANUS C;Planeur;Cdt;Loc;R;16:14;00:31;NON;LFHA-Aérodrome d'Issoire - Le Broc;;836301;ISSOIRE ACPH;Aéro-club Pierre Herbaud;0h 31m;2022
```
	""")

uploaded_file = st.file_uploader(_("upload_button_label"), type=["csv"])
if uploaded_file is not None:
	try:
		df = parse_csv(uploaded_file)
		st.session_state['givav'] = False
		st.session_state['logbook'] = df
		st.success(_("csv_uploaded_success"))
	except Exception as e:
		st.error(f"{_('csv_upload_error')}: {e}")

# Option#2: synchronized glider logbook from Givav
st.subheader(_("connect_subtitle"))
ui_givav_sync()
