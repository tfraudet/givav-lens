import time
import streamlit as st
from givav.scrape import scrappe_logbook
from glider_utils import parse_csv, to_dataframe
from sidebar import info_logbook,footer

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
		st.write(f':green[:material/check_circle:] Givav logbook synced for account :blue[{st.session_state.givav_username}]')

		if st.button("Resync"):
			try:
				givav_synchronize()

				# st.rerun(scope='fragment')
				st.rerun(scope='app')
			except Exception as e:
				st.error(f"Failed to resync from Smart'Glide: {e}")
		
		if st.button("Disconnect"):
			st.session_state['givav'] = False
			if 'logbook' in st.session_state:
				del st.session_state['logbook']
			init_login_info()
			# st.rerun(scope='fragment')
			st.rerun(scope='app')
	else:
		st.write(':red[:material/cancel:] Givav logbook not synced.')  # Empty column for spacing

		with st.form("giva_form_connect"):
			st.text_input("Smart'Glide Username", key="widget_givav_username")
			st.text_input("Smart'Glide Password", type="password", key="widget_givav_password")

			submitted = st.form_submit_button("Connect")
			# Simulate connection and data fetching
			if submitted:
				try:
					update_login_info()
					givav_synchronize()

					st.rerun(scope='app')
				except Exception as e:
					st.error(f"Failed to connect to Smart'Glide: {e}")

st.set_page_config(
	page_title="Glider logbook",
	page_icon="📔",
	layout="wide",
)

# Debug
# st.write(st.session_state)
# st.divider()

# Main page
st.title("📔 Welcome to Glider logbook")
if 'logbook' not in st.session_state:
	st.info("After a successful glider logbook upload, the app pages will become available.")
info_logbook()
footer()

# Option#1:  upload glider logbook as csv file
st.subheader("Option#1: Upload your glider logbook CSV file")
uploaded_file = st.file_uploader("Upload a glider flights CSV file (semicolon-separated)", type=["csv"])
if uploaded_file is not None:
	try:
		df = parse_csv(uploaded_file)
		st.session_state['givav'] = False
		st.session_state['logbook'] = df
		st.success("CSV uploaded and parsed successfully. You can now open the other pages.")
	except Exception as e:
		st.error(f"Failed to parse CSV: {e}")

# Option#2: synchronized glider logbook from Givav
st.subheader("Option#2: Connect to Smart'Glide and import your logbook")
ui_givav_sync()
