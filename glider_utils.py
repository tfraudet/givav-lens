import pandas as pd
import datetime


def make_delta(entry: str) -> datetime.timedelta:
	h, m = entry.split(':')
	return datetime.timedelta(hours=int(h), minutes=int(m))

def normalize_aircraft_types(df: pd.DataFrame) -> pd.DataFrame:
	"""Normalize aircraft type variants to canonical names."""
	normalizations = {
		'LAK19-18M': ('LAK 19', 'LAK 19 18M'),
		'LS6c-18M': ('LS 6/18M', 'LS 6 18M'),
		'ALLIANCE-34': ('SNC34C', 'ALLIANCE 34'),
		'Janus C': ('JANUS C TRAIN RENTRANT', 'JANUS C'),
		'Marianne': ('C201 MARIANNE', 'MARIANNE'),
	}
	
	for canonical, variants in normalizations.items():
		df['Type'] = df['Type'].apply(lambda x: canonical if x in variants else x)
	
	return df
	
def parse_csv(file_like) -> pd.DataFrame:
	"""Parse an uploaded or local CSV file following the project's conventions.

	- separator: `;`
	- parse `Date` with `dayfirst=True`
	- keep columns as strings, then convert `Durée` to timedelta
	- apply the same `Type` normalizations used elsewhere in the app
	"""
	df = pd.read_csv(file_like, sep=';', parse_dates=['Date'], dayfirst=True, dtype=str)

	# Convert duration strings 'HH:MM' into timedeltas
	df['Durée'] = df['Durée'].apply(lambda entry: make_delta(entry))

	# Normalize `Type` variants to canonical names
	df = normalize_aircraft_types(df)

	return df

def to_dataframe(logbook: list[dict]) -> pd.DataFrame:
	"""Convert a logbook list of dicts into a pandas DataFrame with proper types."""
	df = pd.DataFrame(logbook)
	df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')

	# Convert duration strings 'HH:MM' into timedeltas
	df['Durée'] = df['Durée'].apply(lambda entry: make_delta(entry))

	# Normalize `Type` variants to canonical names
	df = normalize_aircraft_types(df)

	return df