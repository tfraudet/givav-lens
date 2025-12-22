import streamlit as st

def info_logbook():
	if 'logbook' not in st.session_state:
		st.sidebar.warning("No glider logbook loaded.")
	else:
		st.sidebar.success("Logbook loaded with {} flights.".format(len(st.session_state['logbook'])))  

	# st.sidebar.write(st.session_state)