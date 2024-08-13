# Python libraries for web scraping (https://proxiesapi.com/articles/web-scraping-in-python-the-complete-guide)
#
# Beautifulsoup: https://pypi.org/project/beautifulsoup4/, https://www.crummy.com/software/BeautifulSoup/bs4/doc/
# Requests: https://pypi.org/project/requests/
# Scrapy: https://scrapy.org/

import requests
import re
import sys
import csv
from bs4 import BeautifulSoup
from datetime import datetime
import click

USERID = ''
PWD = ''
DEFAULT_CLUB_NUMBER = '000000'

__version__ = "1.0.0"

def extract_club_number(session):
	club_number = DEFAULT_CLUB_NUMBER
	r = session.post('https://club.givav.fr/givav.php/gvsmart/main/bureau?sessid=1&assoc=000000')
	if (r.status_code == 200):
		soup = BeautifulSoup(r.text, 'html.parser')
		row = soup.find('h1')
		match = re.search(r"(?<=assoc=)(\d+)", str(row.a))
		if  match:
			club_number = match.group(0)
	else:
		click.echo(click.style('Unbale to get club number, default to {} (error code is {})'.format(club_number,r.status_code),fg='red'))
	return club_number

def surrounded(tag):
	return tag.name == 'tr' and tag.parent.name == 'tbody'

def scrappe_logbook_byyear(session, year, club_number):
	logbook_byyear = list()
	# get the logbook for the season of the year
	click.echo(click.style('Year {}'.format(year), fg='blue'))

	url = 'https://club.givav.fr/givav.php/gvsmart/vol/carnet?sessid=1&assoc={}&saison={}&categorie=P'.format(club_number, year)
	click.echo(click.style('  Scrapping url: {}'.format(url), fg='white'))

	r = session.get(url)
	if (r.status_code == 200):
		soup = BeautifulSoup(r.text, 'html.parser')

		rows = soup.find_all(surrounded)
		click.echo(click.style('  Found {} rows in the HTML table'.format(len(rows)), fg='white'))

		if (len(rows) > 1):
			# Found entries, decode them
			with click.progressbar(rows, label='  Extract flight data', show_pos=True, show_eta=False, show_percent=False, width=len(rows)) as bar:
				for row in bar:
					row.contents = list(filter(lambda a: a != '\n', row.contents))
					# print('row content is {}, type is {}'.format(row.contents, type(row.contents)))
					if (len(row.contents)>=8):
						date = row.contents[0].string + '/' + year
						immat = row.contents[1].string
						glider_type = row.contents[2].string
						category = row.contents[3].string
						pilote_type = row.contents[4].string
						loc = row.contents[5].string
						launch_type = row.contents[6].string
						takeoff = row.contents[7].string
						duration = row.contents[8].string
						montain = row.contents[9].string
						location = row.contents[10].string
						comment = row.contents[11].string
						club_id = row.contents[12].string
						club_short_name = row.contents[13].string
						club_name = row.contents[14].string

						# click.echo('row [{}, {}, {}, {}, {}, {}, {}, {}]'.format(date,immat,glider_type,category,pilote_type,launch_type,duration, comment))
						logbook_byyear.append({
							'Date': date,
							'Immat.': immat,
							'Type': glider_type,
							'Catégorie': category,
							'Fonc.': pilote_type,
							'Nat.': loc,
							'Lanc.': launch_type,
							'Décol.' : takeoff,
							'Durée': duration,
							'Montagne': montain,
							'Lieu': location,
							'Commentaire': comment,
							'Club': club_id,
							'Abréviation': club_short_name,
							'Nom': club_name
							})
			
			# And try to scrappe previous year
			logbook_byyear.extend(scrappe_logbook_byyear(session, str(int(year)-1), club_number))
		else:
			click.echo(click.style('  No entry !!',fg='yellow'))
	else:
		click.echo(click.style(print('Error scrapping url {}, error code is {}'.format(url, r.status_code)),fg='red'))
	return logbook_byyear

def scrappe_logbook(userid=USERID, pwd=PWD ):
	logbook = list()
	with requests.Session() as session:
		r = session.get('https://club.givav.fr/givav.php/gvsmart')
		if (r.status_code == 200):
			# Try to login to Smart'Glide web site
			r = session.post('https://club.givav.fr/givav.php/gvsmart/main/connect?sessid=1&assoc=000000', data={'no_national': userid, 'mot_de_passe': pwd})
			if (r.text == 'OK') and (r.status_code == 200):
				click.echo('Connected to Givav Smart\'Glide website: get logbook...')

				# extrcat the club number from the main web page after logging
				club_number = extract_club_number(session)

				# first year is current year
				year = str(datetime.now().year)

				# scrappe logbook
				logbook = scrappe_logbook_byyear(session, year, club_number)

			else:
				click.echo(click.style('Error when connected to Givav Smart\'Glide website, verify your userid and/or password',fg='red'))
		else:
			click.echo(click.style(' Smart Glide web site not responding, error is {}'.format(r.status_code),fg='red'))
	return logbook

# def export_to_csv(logbook, filename = 'givav-export.csv'):
# 	fieldnames = ['Date', 'Immat.', 'Type', 'Catégorie', 'Fonc.', 'Nat.', 'Lanc.', 'Décol.', 'Durée', 'Montagne', 'Lieu', 'Commentaire', 'Club', 'Abréviation', 'Nom']
# 	with click as csvfile:
# 		csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
# 		csv_writer.writeheader()
# 		csv_writer.writerows(logbook)

def export_to_csv(logbook, file):
	fieldnames = ['Date', 'Immat.', 'Type', 'Catégorie', 'Fonc.', 'Nat.', 'Lanc.', 'Décol.', 'Durée', 'Montagne', 'Lieu', 'Commentaire', 'Club', 'Abréviation', 'Nom']
	csv_writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';')
	csv_writer.writeheader()
	csv_writer.writerows(logbook)

@click.command()
@click.option('-u', '--user', required=True, prompt=True, type=str)
@click.password_option('-p', '--password')
# @click.option('-o', '--output', default='givav-export.csv', show_default=True,  type=click.File('w', encoding='utf8'), help='Specified the filename for output file.')
@click.option('-o', '--output', default='-', show_default=True,  type=click.File('w', encoding='utf8'), help='The filename where to output the result.')
@click.version_option(__version__ , '-v', '--version')
def cli(user, password, output):
	"""
		Scrape flight data from Givav Smart'Glide website.\n
		You need to pass your userdid/password to login.
	"""

	click.clear()
	click.echo('Extracting givav logbook for user {}'.format(user))
	logbook = scrappe_logbook(user,password)

	print('\nScrapping done, exporting result to csv file \'{}\''.format(output))
	export_to_csv(logbook, output)

	print('File saved successfully')
	return 0 # successful

if __name__ == '__main__':
	cli()

