import streamlit as st
from glider_utils import parse_csv
from sidebar import info_logbook

@st.cache_data(show_spinner="Fetching data from CSV file...")
def upload_data(file_like):
	return parse_csv(file_like)

st.set_page_config(
	page_title="Glider logbook",
	page_icon="📔",
	layout="wide",
)
	
# Main page
st.title("📔 Welcome to Glider logbook")
if 'logbook' not in st.session_state:
	st.info("After a successful glider logbook upload, the app pages will become available.")
info_logbook()

# upload glider logbook as csv file
st.subheader("Option#1: Upload your glider logbook CSV file")
uploaded_file = st.file_uploader("Upload a glider flights CSV file (semicolon-separated)", type=["csv"])
if uploaded_file is not None:
	try:
		df = parse_csv(uploaded_file)
		st.session_state['logbook'] = df
		st.success("CSV uploaded and parsed successfully. You can now open the other pages.")
	except Exception as e:
		st.error(f"Failed to parse CSV: {e}")


# upload glider logbook from Givav
st.subheader("Option#2: Connect to Smart'Glide and import your logbook")


st.markdown("---")
# st.info("After a successful upload, the app pages will become available. If you have issues, ensure the CSV follows the project's schema and uses `;` as separator.")
