import streamlit as st
from glider_utils import parse_csv

st.set_page_config(page_title="Glider logbook - Upload CSV", page_icon="📁", layout="wide")

st.write("# 📁 Upload CSV")
st.sidebar.header("Upload CSV")

col1, col2 = st.columns([3, 1])

with col1:
    uploaded_file = st.file_uploader("Upload a glider flights CSV file (semicolon-separated)", type=["csv"])
    if uploaded_file is not None:
        try:
            df = parse_csv(uploaded_file)
            st.session_state['logbook'] = df
            st.success("CSV uploaded and parsed successfully. You can now open the other pages.")
            st.experimental_rerun()
        except Exception as e:
            st.error(f"Failed to parse CSV: {e}")

with col2:
    st.markdown("**Developer / offline options**")
    st.write("Load a bundled sample CSV from the `db/` folder for testing.")
    if st.button("Load sample CSV (db/glider-flights-tf-202512.csv)"):
        try:
            df = parse_csv('./db/glider-flights-tf-202512.csv')
            st.session_state['logbook'] = df
            st.success("Sample CSV loaded into session.")
            st.experimental_rerun()
        except Exception as e:
            st.error(f"Failed to load sample CSV: {e}")

st.markdown("---")
st.info("After a successful upload, the app pages will become available. If you have issues, ensure the CSV follows the project's schema and uses `;` as separator.")
