# Glider Logbook - AI Coding Instructions

## Project Overview
A Streamlit web application for analyzing personal glider flight statistics and logging. It combines:
- **Data source**: CSV files scraped from Givav Smart'Glide website (aviation club logbook system)
- **Web UI**: Streamlit multi-page app showing flight hours, aircraft usage, and instructor statistics
- **Data scraper**: Click CLI tool that authenticates and extracts flight data from Givav website

## Key Architecture Patterns

### Data Flow
1. **Scraping**: `givav/scrape.py` uses BeautifulSoup to extract HTML tables from Givav, outputs CSV with `;` delimiter
2. **Data Loading**: `logbook.py:load_data()` reads CSV (currently hardcoded to `db/glider-flights-tf-202509.csv`)
3. **Session State**: Main page loads data into `st.session_state['logbook']` for multi-page access
4. **Visualization**: Pages use Plotly for interactive charts, pandas for aggregations

### CSV Schema
CSV files (in `db/` directory) use `;` delimiter with columns:
- Date, Immat., Type, Catégorie, Fonc., Nat., Lanc., Décol., Durée, Montagne, Lieu, Commentaire, Club, Abréviation, Nom

Critical: **Durée column is in "HH:MM" format** - must convert to timedelta via `make_delta()` function. Function type (Fonc.) includes: "Elv" (training), others for different pilot roles.

## Development Conventions

### Duration Handling
- Input: String format "HH:MM" (e.g., "02:45")
- Transformation: `logbook['Durée'] = logbook['Durée'].apply(lambda entry: make_delta(entry))`
- Display: Convert to "XhYYm" format: `'{0}h {1}m'.format(x.components.days*24 + x.components.hours, x.components.minutes)`

### Aircraft Type Normalization
Standardize variant names in [logbook.py lines 159-163]:
```python
logbook['Type'] = logbook['Type'].apply(lambda x: 'LAK19-18M' if x in ('LAK 19', 'LAK 19 18M') else x)
```
Add new mappings here when variants appear in new CSV files.

### Multi-Page Data Sharing
Pages (`pages/1_aircraft.py`, `pages/2_function.py`) access logbook via `st.session_state['logbook']` - **never reload CSV directly** in pages to maintain consistency.

### Streamlit Configuration
- Main page: wide layout, page icon "📔"
- Sub-pages: wide layout with custom icons
- Use sidebar sections (`st.sidebar.header()`) for page-specific controls
- Use session state radio buttons to control rendering (e.g., `st.session_state['graphic_type']`)

## Common Tasks

### Adding New Statistics Pages
1. Create `pages/X_name.py` (Streamlit auto-discovers these)
2. Read logbook from session: `df = st.session_state.logbook`
3. Use pandas `groupby()` + `agg()` for aggregations
4. Render with Plotly charts, normalize durations for display

### Updating Givav Scraper
- **Authentication**: `scrappe_logbook()` logs in, extracts club number, then iterates backwards through years
- **HTML parsing**: Uses `surrounded()` predicate to find flight rows (`<tr>` in `<tbody>`)
- **CLI interface**: Click decorators define user/password/output options; stdout is default
- Install via: `pip install --editable .` (entry point: `givav-scrape`)

### Working with New CSV Data
1. Place new file in `db/` (naming: `glider-flights-tf-YYYYMM.csv`)
2. Update hardcoded path in `load_data()` function
3. If aircraft names differ, add normalization mappings
4. Test with `logbooks.ipynb` exploration notebook

## Dependencies
- **Runtime**: streamlit, plotly, pandas, click, beautifulsoup4, requests
- **Development**: Jupyter (for `logbooks.ipynb` exploration)

## Running Locally
```bash
# Web app
streamlit run logbook.py

# Scraper (interactive)
givav-scrape

# Or with credentials
givav-scrape --user USERNAME --password PASSWORD -o export.csv
```

## Code Quality Notes
- Duration arithmetic uses pandas timedelta: `x.total_seconds() / 3600` for hours
- Plotly subplots: `make_subplots(rows, cols, shared_xaxes=True, shared_yaxes=True)` for year-month comparisons
- Session state pattern prevents data reload on page navigation - critical for multi-page performance
