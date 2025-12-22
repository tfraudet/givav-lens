import streamlit as st

__version__ = "1.0.0"

def info_logbook():
	if 'logbook' not in st.session_state:
		st.sidebar.warning("No glider logbook loaded.")
	else:
		st.sidebar.success("Logbook loaded with {} flights.".format(len(st.session_state['logbook'])))  

	# st.sidebar.write(st.session_state)

def footer():
	st.sidebar.divider()
	material_favorote_html = '<span role="img" aria-label="favorite icon" style="display: inline-block; font-family: &quot;Material Symbols Rounded&quot;; font-weight: 400; user-select: none; vertical-align: bottom; white-space: nowrap; overflow-wrap: normal;">favorite</span>'

	st.sidebar.image('img/acph-logo-v2017-gray.png', width=100)
	st.sidebar.html('Made with <span style="color: green">{}</span> by <a href="https://aeroclub-issoire.fr/">ACPH</a> - version {}'.format(material_favorote_html, __version__))