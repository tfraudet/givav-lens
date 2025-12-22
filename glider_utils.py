import pandas as pd
import datetime


def make_delta(entry: str) -> datetime.timedelta:
    h, m = entry.split(':')
    return datetime.timedelta(hours=int(h), minutes=int(m))


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
    df['Type'] = df['Type'].apply(lambda x: 'LAK19-18M' if x in ('LAK 19', 'LAK 19 18M') else x)
    df['Type'] = df['Type'].apply(lambda x: 'LS6c-18M' if x in ('LS 6/18M', 'LS 6 18M') else x)
    df['Type'] = df['Type'].apply(lambda x: 'ALLIANCE-34' if x in ('SNC34C', 'ALLIANCE 34') else x)
    df['Type'] = df['Type'].apply(lambda x: 'Janus C' if x in ('JANUS C TRAIN RENTRANT', 'JANUS C') else x)
    df['Type'] = df['Type'].apply(lambda x: 'Marianne' if x in ('C201 MARIANNE', 'MARIANNE') else x)

    return df
