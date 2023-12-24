import streamlit as st
import pandas as pd
import datetime

from dateutil.relativedelta import relativedelta

from plotly.subplots import make_subplots
import plotly.graph_objects as go

def make_delta(entry):
	h, m = entry.split(':')
	return datetime.timedelta(hours=int(h), minutes=int(m))

@st.cache_data(show_spinner="Fetching data from CSV file...")
def load_data():
	#load flights logbook
	logbook = pd.read_csv('./db/glider-flights-tf-202312.csv', sep = ';', parse_dates = ['Date'], dayfirst=True, dtype=str)
	logbook.drop(columns=['Durée Compute', 'Année'],  inplace=True)
	logbook['Durée'] = logbook['Durée'].apply(lambda entry: make_delta(entry))
	return logbook

def graphic_type_subplot(df):
	max_colums = 3
	max_rows = (len(df['Year'].unique()) // max_colums) if (len(df['Year'].unique()) % max_colums == 0) else (len(df['Year'].unique()) // max_colums) +1 

	fig = make_subplots(rows=max_rows, cols=max_colums, shared_xaxes='all', shared_yaxes='all', subplot_titles=df['Year'].unique().tolist())
	# print(df['Year'].unique().tolist())

	for idx, year in enumerate(df['Year'].unique()):
		data_year = df.query('Year == {}'.format(year))
		ccol = (idx % max_colums) + 1
		crow = (idx // max_colums) + 1
		# print ('index = {}, year={}, row={}, colum={}'.format(idx, year, crow, ccol))
		fig.add_trace(go.Bar(name= 'data for {}'.format(year), x=data_year['Month'], y=data_year['ISO_Duration'] ), row=crow, col=ccol)
		fig.update_xaxes(showticklabels=True, tickvals=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],ticktext = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],row=crow, col=ccol )
		fig.update_yaxes(ticksuffix = 'h00s')

	for i in range(idx+1):
		fig['layout']['xaxis{}_tickangle'.format(i+1)] = -45
	fig.update_layout(height=800, showlegend=False, title_text="<b>Cumulative flight hours by year and month</b>")
	st.plotly_chart(fig,use_container_width=True)

def graphic_type_slider(logbook):
	# Insert missing months in the cumul of flying hours by year and month. 
	df_normalize = logbook.groupby([logbook['Date'].dt.year.rename('Year'), logbook['Date'].dt.month.rename('Month')])['Durée'].sum()
	df_normalize = df_normalize.reset_index()

	for year in df_normalize['Year'].unique():
		existing_months = df_normalize[df_normalize['Year'] == year]['Month'].unique()
		for month in range(1,13):
			if month not in existing_months:
				# print('month {} for year {} is not in the dataframe, add it. months existing are {}'.format(month,year,existing_months))
				# df_normalize = df_normalize.append({'Year': year, 'Month': month, 'Durée': datetime.timedelta(hours=0, minutes=0)}, ignore_index=True)
				df_normalize = pd.concat([df_normalize, pd.DataFrame([[year, month, datetime.timedelta(hours=0, minutes=0)]], columns=['Year', 'Month', 'Durée'])], ignore_index=True)

	df_normalize = df_normalize.sort_values(by=['Year','Month'],inplace = False, ascending = [True,True])

	df_normalize['Heures de vol'] = df_normalize['Durée'].apply(lambda x: '{}h {}m'.format(x.components.days*24 + x.components.hours, x.components.minutes))
	df_normalize['ISO_Duration']=df_normalize['Durée']/pd.Timedelta("1 hour")
	
	# Plot the figure with slider to filter years display
	years = df_normalize['Year'].unique()
	offset = 0.1

	fig = go.Figure()
	for year in years:
		data_year = df_normalize.query('Year == {}'.format(year))

		fig.add_trace(go.Bar(
			x=data_year['Month'],
			y=data_year['ISO_Duration'],
			name='{}'.format(year),
			visible= year<=2016,
			opacity=0.9,
			# marker=dict(line=dict(width=3, color='gray')),
			width=[0.6] * 12,
			offset=offset * (years.tolist().index(year) +1)
		))

	steps = list()
	for i in range(len(years)):
		step = dict(
			method='restyle',
			args=[ {"visible": [False] * len(years)}, {"offset": [0] * len(years)}, {"title": "Slider switched to year {} ".format(years[i])}],
			label='{}'.format(years[i])
		)
		step['args'][0]['visible'][i] = True
		step['args'][1]['offset'][i] = offset
		# if exist previous year visible also
		if i>0:
			step['args'][0]['visible'][i-1] = True

		# if exist next year visible also
		if i<(len(years)-1):
			step['args'][0]['visible'][i+1] = True
			step['args'][1]['offset'][i] = offset*2

		steps.append(step)

	sliders = [dict(
		active=0,
		currentvalue={"prefix": "Current year is "},
		pad={"t": 50},
		steps=steps
	)]

	fig.update_layout(barmode='overlay', xaxis_tickangle=-45, height=600, yaxis={ 'tickformat': '%X', 'ticksuffix': 'h00s'}, sliders = sliders )
	fig.update_xaxes(tickvals=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], ticktext = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
	st.plotly_chart(fig,use_container_width=True)

st.set_page_config(
	page_title="Glider logbook",
	page_icon="📔",
	layout="wide",
)

# Side bar
st.sidebar.header("Logbook")
st.sidebar.write("This is a logbook of all my glider flights since the begining.")
graphic_type_index = 0
if 'graphic_type' in st.session_state and st.session_state['graphic_type'] == 'Slider':
	graphic_type_index = 1
st.session_state['graphic_type']= st.sidebar.radio("Type of graphic available for flight hours per year and month:", ['Subplot', 'Slider'],index=graphic_type_index)
# st.sidebar.write('The selection is {}'.format(st.session_state['graphic_type']))

# Main page
st.write("#  📔 Welcome to Glider logbook")

# Load the flights logbook data from csv file
logbook = load_data()

# Save the data in the session for the other pages
if 'logbook' not in st.session_state:
	st.session_state['logbook'] = logbook

# Display global statistic on flight hours
total_flights_duration = logbook['Durée'].sum()
total_flight_period = relativedelta(logbook.iloc[-1]['Date'], logbook.iloc[0]['Date'])

multi = '''The total number of flight hours is :green[{}] hours and :green[{}] minutes.  
In :green[{}] flights.  
Over a period of :green[{}] years, :green[{}] months and :green[{}] day(s).
'''. format(total_flights_duration.components.days*24 + total_flights_duration.components.hours, total_flights_duration.components.minutes, len(logbook.index),total_flight_period.years,total_flight_period.months,total_flight_period.days)
st.markdown(multi)

# Plot flight statistics by year
st.header('Flight statistics by year',divider=True)
df = logbook.groupby([logbook['Date'].dt.year.rename('Year')])['Durée'].describe()
for column in ['mean', 'std', 'min','25%','50%','75%','max']: df[column] = pd.to_timedelta(df[column])
df['count'] = df['count'].astype('int32')
df['Total'] = logbook.groupby([logbook['Date'].dt.year.rename('Year')])['Durée'].sum()
df = df.reset_index()
# print(df.info())

df_display = df.copy()
df_display['max'] = df_display['max'].apply(lambda x: '{}h {}m'.format(x.components.days*24 + x.components.hours, x.components.minutes))
df_display['min'] = df_display['min'].apply(lambda x: '{}h {}m'.format(x.components.days*24 + x.components.hours, x.components.minutes))
df_display['mean'] = df_display['mean'].apply(lambda x: '{}h {}m'.format(x.components.days*24 + x.components.hours, x.components.minutes))
df_display['std'] = df_display['std'].apply(lambda x: '{}h {}m'.format(x.components.days*24 + x.components.hours, x.components.minutes))
df_display['25%'] = df_display['25%'].apply(lambda x: '{}h {}m'.format(x.components.days*24 + x.components.hours, x.components.minutes))
df_display['50%'] = df_display['50%'].apply(lambda x: '{}h {}m'.format(x.components.days*24 + x.components.hours, x.components.minutes))
df_display['75%'] = df_display['75%'].apply(lambda x: '{}h {}m'.format(x.components.days*24 + x.components.hours, x.components.minutes))
df_display['Total'] = df_display['Total'].apply(lambda x: '{}h {}m'.format(x.components.days*24 + x.components.hours, x.components.minutes))

fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(
	go.Bar(x=df['Year'], y=df['count'], name="Flight number", marker=dict(color='PaleGreen') ), secondary_y=False
)
fig.add_trace(
	go.Scatter(x=df['Year'], y=df['Total'], name="Total per year", mode="lines+markers+text",
			text = df['Total'].apply(lambda x: '{}h {}m'.format(x.components.days*24 + x.components.hours, x.components.minutes)),
			textposition='top center', hoverinfo='skip',textfont=dict(color="DodgerBlue"),line= {"color": "DodgerBlue"},
	),
	secondary_y=True
)
fig.add_trace(
	go.Scatter(x=df['Year'], y=df['mean'], name='Mean per flight', mode='lines+markers+text', 
		text = df['mean'].apply(lambda x: '{}h {}m'.format(x.components.days*24 + x.components.hours, x.components.minutes)),
		textposition='top center', hoverinfo='skip' ,line= {"color": "Crimson", "width": 1, "dash": 'dash'}, textfont=dict(color="Crimson")),
	secondary_y=True
)
fig.update_layout(title_text="<b>Flight statistics by year.</b>")
fig.update_xaxes(title_text="Year")
fig.update_yaxes(title_text="Number of flights", secondary_y=False)
fig.update_yaxes(title_text="Flight hours", secondary_y=True)
st.plotly_chart(fig,use_container_width=True)

# Display the corresponding dataframe
st.write('All statistical data ')
st.dataframe(df_display,hide_index=True, use_container_width=True,
				column_config={
					'Year': st.column_config.NumberColumn('🗓 Year', format='%d'),
				}
			 )

# Plot cummulative flight hours, by year and by month
st.header('Flight hours per year and month',divider=True)
df = logbook.groupby([logbook['Date'].dt.year.rename('Year'), logbook['Date'].dt.month.rename('Month')])['Durée'].sum()
df = df.reset_index()
df['Heures de vol'] = df['Durée'].apply(lambda x: '{}h {}m'.format(x.components.days*24 + x.components.hours, x.components.minutes))
df['ISO_Duration']=df['Durée']/pd.Timedelta("1 hour")

# Display graphic, based on graphic type option
if st.session_state['graphic_type'] == 'Subplot':
	graphic_type_subplot(df)
elif st.session_state['graphic_type'] == 'Slider':
	graphic_type_slider(logbook)
else:
	st.write('Error: graphic type unknown')

# Logbook detail
st.header('Logbook detail',divider=True)
st.dataframe(logbook, hide_index=True, use_container_width=True)
