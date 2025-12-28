# Givav-Lens - AI Coding Instructions

## Project Overview

A Streamlit web application for analyzing personal glider flight statistics and logging. Combines:

- **Data source**: CSV files scraped from Givav Smart'Glide (aviation club logbook system)
- **Web UI**: Streamlit multi-page dashboard showing flight hours, aircraft usage, and instructor statistics
- **Data scraper**: Click CLI tool that authenticates to Givav and extracts flight data via BeautifulSoup

## Architecture & Data Flow

### Core Workflow

1. **Main entry**: `main.py` renders login form and handles Givav authentication
2. **Scraping**: `givav/scrape.py` crawls Givav website, extracts flight data as list of dicts
3. **Data conversion**: `glider_utils.py` transforms raw data into pandas DataFrame with normalized types
4. **Session state**: Logbook stored in `st.session_state['logbook']` - accessed by all pages
5. **Visualization**: Sub-pages (`pages/*.py`) read session state, aggregate with pandas, render with Plotly

### CSV Data Schema

Files in `db/` directory use `;` delimiter. Columns:
- `Date` (DD/MM/YYYY), `Immat.`, `Type`, `Catégorie`, `Fonc.`, `Nat.`, `Lanc.`, `Décol.`, `Durée` (HH:MM), `Montagne`, `Lieu`, `Commentaire`, `Club`, `Abréviation`, `Nom`

**Critical**: `Durée` is always "HH:MM" string → must convert via `make_delta()` to timedelta.

## Key Development Patterns

### Duration Handling

- **Input**: String "HH:MM" (e.g., "01:45")
- **Conversion**: `df['Durée'] = df['Durée'].apply(lambda x: make_delta(x))` in `glider_utils.py`
- **Display**: `'{0}h {1}m'.format(x.components.days*24 + x.components.hours, x.components.minutes)`
- **Arithmetic**: `x.total_seconds() / 3600` converts to decimal hours for Plotly

### Aircraft Type Normalization

In [glider_utils.py](../glider_utils.py#L11-L18), map variant names to canonical types:
```python
normalizations = {
    'LAK19-18M': ('LAK 19', 'LAK 19 18M'),
    'LS6c-18M': ('LS 6/18M', 'LS 6 18M'),
    # Add new mappings as variants appear in CSV files
}
```
Ensure both `parse_csv()` and `to_dataframe()` call `normalize_aircraft_types()`.

### Multi-Page Architecture

- **Main page** ([main.py](../main.py)): Authentication, CSV upload, Givav sync via `scrappe_logbook()`
- **Sub-pages** ([pages/0_flights.py](../pages/0_flights.py), [pages/1_aircraft.py](../pages/1_aircraft.py), [pages/2_role.py](../pages/2_role.py)): Always access `st.session_state['logbook']` - never load CSV directly
- **Sidebar utilities** ([sidebar.py](../sidebar.py)): `info_logbook()` checks session state, `date_range_selector()` provides date filtering

### Givav Scraper Details

- **Entry point**: `givav-scrape` CLI (defined in [setup.py](../setup.py#L11))
- **Flow**: Login → extract club number via regex → iterate backward through years → parse HTML `<tr>` rows via `surrounded()` predicate
- **Output**: List of dicts with keys matching CSV columns, ready for `to_dataframe()`

## Running & Debugging

```bash
# Web app
streamlit run main.py

# Scraper (interactive)
givav-scrape  # Prompts for username/password

# Install scraper in development
pip install --editable .
```

## Common Tasks

### Add New Statistics Page

1. Create `pages/X_name.py` (Streamlit auto-discovers)
2. Copy pattern from [pages/1_aircraft.py](../pages/1_aircraft.py#L20-L30):
   ```python
   df = st.session_state.logbook
   df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
   df = df.groupby('Type')['Durée'].agg(['sum', 'count'])
   ```
3. Format display durations with `make_delta()` pattern
4. Use Plotly charts (see examples in existing pages)

### Load New CSV Data

1. Place file in `db/` as `glider-flights-tf-YYYYMM.csv`
2. Update hardcoded path in [pages/0_flights.py](../pages/0_flights.py#L22): `parse_csv('./db/glider-flights-tf-YYYYMM.csv')`
3. Add aircraft type mappings in [glider_utils.py](../glider_utils.py#L11-L18) if needed
4. Test in any page - session state ensures consistency

## Code Quality Notes

- Plotly subplots use `make_subplots(rows, cols, shared_xaxes=True)` for multi-year comparisons
- Session state with `@st.cache_data` prevents unnecessary reloads on page navigation
- Streamlit page config: `layout="wide"`, icon `"📔"` (consistent across all pages)
- Fragment-based UI updates (see [main.py](../main.py#L43)) isolate re-renders
