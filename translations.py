import streamlit as st

"""
Internationalization (i18n) module for GivavLens.
Provides language dictionaries and utility functions for multi-language support.
"""

TRANSLATIONS = {
	"en": {
		# Main page
		"welcome_title": "📔 Welcome to GivavLens",
		"logbook_info": "Once the Givav logbook has been successfully uploaded, the app's statistics pages become accessible.",
		"upload_subtitle": "Option#1: Upload glider logbook data from CSV file",
		"connect_subtitle": "Option#2: Connect to Smart'Glide and import your logbook",
		"csv_format_help": ":material/help: CSV Format Help",
		"expected_csv_format": "Expected CSV Format",
		"csv_description": "The CSV file must be **semicolon-separated** (`;`) with the following columns:",
		"csv_example": "Example",
		"upload_button_label": "Upload a glider flights CSV file (semicolon-separated)",
		"csv_uploaded_success": "CSV uploaded and parsed successfully. You can now open the other pages.",
		"csv_upload_error": "Failed to parse CSV",
		"givav_sync_status_connected": ":green[:material/check_circle:] Givav logbook synced for account :blue[{}]",
		"givav_sync_status_disconnected": ":red[:material/cancel:] Givav logbook not synced.",
		"givav_resync_button": ":material/sync: Resync",
		"givav_disconnect_button": ":material/logout: Disconnect",
		"givav_connect_button": ":material/login: Connect",
		"givav_username_label": "Smart'Glide Username",
		"givav_password_label": "Smart'Glide Password",
		"givav_connect_error": "Failed to connect to Smart'Glide",
		"givav_resync_error": "Failed to resync from Smart'Glide",
		"wait_for_it" : "Please wait...",
		
		# Sidebar
		"logbook_loaded": "Logbook loaded with {} flights.",
		"logbook_not_loaded": "No glider logbook loaded.",
		"filters": "Filters",
		"date_range": "Select Date Range",
		"language_selectore" : "Select your language",

		# All pages
		"logbook_warning": "No logbook loaded. Go to the main page to upload or sync your Givav data.",
		"glider": "Glider",
		"value": "Value",

		# Flights page
		"flights_title": "Flight statistics over time",
		"flights_empty_warning": "The logbook is empty for the selected date range.",
		"total_flights": "The total number of flight hours is :green[{}] hours and :green[{}] minutes.\nFor :green[{}] flights.\nOver a period of :green[{}] years, :green[{}] months and :green[{}] day(s).",
		"statistics_by_year": "Flight statistics by year",
		"hours_by_month": "Flight hours per year and month",
		"logbook_detail": "Logbook raw data",
		"flights_sidebar_header": "Flights",
		"flights_sidebar_description": "Historical trends and statistical analysis of glider flight over time.",
		"graphic_type_label": "Type of graphic available for flight hours per year and month:",
		"flight_count": "Flight count",
		"total_per_year": "Total per year",
		"mean_per_flight": "Mean per flight",
		"flight_hours": "Flight hours",
		"full_stats": "Full statistics",
		"total_hours_by_year_and_month": "Total Flight Hours by Year and Month",

		# Aircraft page
		"aircraft_title": "Aircraft statistics over time",
		"aircraft_empty_warning": "The logbook is empty for the selected date range.",
		"aircraft_total": "For a total of :green[{}] flights in :green[{}] hours and :green[{}] minutes",
		"hours_per_aircraft": "Flight hours per aircraft",
		"flights_per_aircraft": "Number of flights per aircraft",
		"aircraft_details": "Details hours & number of flights per aircraft",
		"aircraft_sidebar_header": "Aircraft",
		"aircraft_sidebar_description": "Glider flight statistics by aircraft type.",
		
		# Role page
		"role_title": "Role statistics over time",
		"role_empty_warning": "The logbook is empty for the selected date range.",
		"role_total": "For a total of :green[{}] flight in :green[{}] hours and :green[{}] minutes",
		"hours_per_role": "Flight hours per role",
		"flights_per_role": "Number of flights per role",
		"instructors_used": "Most used instructors",
		"role_details": "Details hours & number of flights per role",
		"role_sidebar_header": "Role",
		"role_sidebar_description": "Glider flight statistics by pilot role.",
		"instructor" : "Instructor",
		"role_breakdown" : "Role Breakdown: Hours & Flight Totals",
		
		# Table columns
		"year_column": "🗓 Year",
		"count_column": "Count",
		"mean_column": "Mean",
		"aircraft_type_column": "🛩 Aircraft type",
		"flight_duration_column": "Flight duration",
		"flight_number_column": "Flight number",
		"flight_hours_column": "Flight hours",
		"function_column": "Function",
		"number_of_flights_column": "Number of flights",
	},
	"fr": {
		# Main page
		"welcome_title": "📔 Bienvenue dans GivavLens",
		"logbook_info": "Une fois le carnet de vol Givav chargé avec succès, les pages de statistiques de l\'application deviennent accessibles.",
		"upload_subtitle": "Option#1 : Téléverser les données du carnet de vol depuis un fichier CSV",
		"connect_subtitle": "Option#2 : Connectez-vous à Smart'Glide et importez votre carnet de vol",
		"csv_format_help": ":material/help: Aide au format CSV",
		"expected_csv_format": "Format CSV attendu",
		"csv_description": "Le fichier CSV doit être **séparé par des points-virgules** (`;`) avec les colonnes suivantes :",
		"csv_example": "Exemple",
		"upload_button_label": "Téléverser un fichier CSV de vols de planeur (séparé par des points-virgules)",
		"csv_uploaded_success": "CSV téléversé et analysé avec succès. Vous pouvez maintenant ouvrir les autres pages.",
		"csv_upload_error": "Erreur lors de l'analyse du CSV",
		"givav_sync_status_connected": ":green[:material/check_circle:] Carnet de vol Givav synchronisé pour le compte :blue[{}]",
		"givav_sync_status_disconnected": ":red[:material/cancel:] Carnet de vol Givav non synchronisé.",
		"givav_resync_button": ":material/sync: Resynchroniser",
		"givav_disconnect_button": ":material/logout: Déconnexion",
		"givav_connect_button": ":material/login: Connecter",
		"givav_username_label": "Nom d'utilisateur Smart'Glide",
		"givav_password_label": "Mot de passe Smart'Glide",
		"givav_connect_error": "Impossible de se connecter à Smart'Glide",
		"givav_resync_error": "Impossible de resynchroniser à partir de Smart'Glide",
		"wait_for_it" : "Veuillez patienter...",
		
		# Sidebar
		"logbook_loaded": "Carnet de vol chargé avec {} vols.",
		"logbook_not_loaded": "Aucun carnet de vol de planeur chargé.",
		"filters": "Filtres",
		"date_range": "Sélectionner la plage de dates",
		"language_selectore" : "Selectionner la langue",

		# All pages
		"logbook_warning": "Aucun carnet de vol n'est chargé. Rendez-vous sur la page principale pour téléverser ou synchroniser vos données Givav.",
		"glider": "Planeur",
		"value": "Valeur",

		# Flights page
		"flights_title": "Statistiques de vol au fil du temps",
		"flights_empty_warning": "Le carnet de vol est vide pour la plage de dates sélectionnée.",
		"total_flights": "Le nombre total d'heures de vol est :green[{}] heures et :green[{}] minutes. Pour :green[{}] vols.\nSur une période de :green[{}] ans, :green[{}] mois et :green[{}] jour(s).",
		"statistics_by_year": "Statistiques de vol par année",
		"hours_by_month": "Heures de vol par année et par mois",
		"logbook_detail": "Données sources du carnet de vol",
		"flights_sidebar_header": "Vols",
		"flights_sidebar_description": "Tendances historiques et analyse statistique des vols de planeur au fil du temps.",
		"graphic_type_label": "Type de graphique disponible pour les heures de vol par année et par mois :",
		"flight_count": "Nombre de vols",
		"total_per_year": "Total par année",
		"mean_per_flight": "Moyenne par vol",
		"flight_hours": "Heures de vol",
		"full_stats": "Statistiques complètes",
		"total_hours_by_year_and_month": "Total des heures de vol par année et par mois",

		# Aircraft page
		"aircraft_title": "Statistiques des aéronefs au fil du temps",
		"aircraft_empty_warning": "Le carnet de vol est vide pour la plage de dates sélectionnée.",
		"aircraft_total": "Pour un total de :green[{}] vols en :green[{}] heures et :green[{}] minutes",
		"hours_per_aircraft": "Heures de vol par aéronef",
		"flights_per_aircraft": "Nombre de vols par aéronef",
		"aircraft_details": "Détails des heures et du nombre de vols par aéronef",
		"aircraft_sidebar_header": "Aéronefs",
		"aircraft_sidebar_description": "Statistiques de vol en planeur par type d'aéronef.",
		
		# Role page
		"role_title": "Statistiques des rôles au fil du temps",
		"role_empty_warning": "Le carnet de vol est vide pour la plage de dates sélectionnée.",
		"role_total": "Pour un total de :green[{}] vol en :green[{}] heures et :green[{}] minutes",
		"hours_per_role": "Heures de vol par rôle",
		"flights_per_role": "Nombre de vols par rôle",
		"instructors_used": "Instructeurs les plus utilisés",
		"role_details": "Détails des heures et du nombre de vols par rôle",
		"role_sidebar_header": "Rôle",
		"role_sidebar_description": "Statistiques de vol en planeur par rôle de pilote.",
		"instructor" : "Instructeur",
		"role_breakdown" : "Répartition par rôle: total des heures et vols",

		# Table columns
		"year_column": "🗓 Année",
		"count_column": "Nombre",
		"mean_column": "Moyenne",
		"aircraft_type_column": "🛩 Type d'aéronef",
		"flight_duration_column": "Durée du vol",
		"flight_number_column": "Numéro de vol",
		"flight_hours_column": "Heures de vol",
		"function_column": "Fonction",
		"number_of_flights_column": "Nombre de vols",
	}
}

def get_language() -> str:
	"""Get the current language from session state."""

	if 'language' not in st.session_state:
		st.session_state.language = detect_browser_language()
	return st.session_state.language

def detect_browser_language() -> str:
	"""
	Detect browser language preference.
	Defaults to 'fr' (French) if available, otherwise 'en' (English).
	"""
	try:
		# Safely get the locale attribute; it may be None or missing
		browser_locale = getattr(st.context, "locale", None)

		# Ensure it's a non-empty string before slicing
		if isinstance(browser_locale, str) and browser_locale:
			lang = browser_locale[:2]
			if lang in TRANSLATIONS:
				return lang
	except Exception:
		# Any error getting the locale falls back to default
		pass
	
	# Default to French
	return 'en'

def translate(key: str, *args, **kwargs) -> str:
	"""
	Translate a key to the current language.
	Supports formatting with positional and keyword arguments.
	Falls back to English if key not found in current language.
	"""
	import streamlit as st
	lang = get_language()
	
	# Get translation from current language, fall back to English
	text = TRANSLATIONS.get(lang, {}).get(key)
	if text is None:
		text = TRANSLATIONS.get("en", {}).get(key, key)
	
	# Format text if arguments provided
	if args or kwargs:
		try:
			return text.format(*args, **kwargs)
		except (IndexError, KeyError):
			return text
	
	return text

def _(key: str, *args, **kwargs) -> str:
	"""Shorthand for translate()."""
	return translate(key, *args, **kwargs)
