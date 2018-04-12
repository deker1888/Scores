import urllib.request
from bs4 import BeautifulSoup
import csv
import re
from datetime import datetime

#specify the url
bbc_sport_scores = 'http://www.bbc.co.uk/sport/football/scores-fixtures'
scores_file = open('C:/Users/deker/Desktop/BBCSportResultScraper/results.csv','a',newline='')
#for aDay in range(15,29):
#bbc_sport_scores = 'http://www.bbc.co.uk/sport/football/scores-fixtures/2018-03-' + str(aDay)

#query the website and return the html to the variable 'full_scores_page'
full_scores_page = urllib.request.urlopen(bbc_sport_scores)

#parse the html using beautiful soup and store in the variable 'scores_soup'
soup = BeautifulSoup(full_scores_page,'html.parser')

#from the 'full_scores_page', extract the list of scores to the 'scores_list' variable
fixture_list = soup.find_all('div',attrs={'class': 'sp-c-fixture__wrapper'})

datePattern = '[A-Z]+[a-z]+\-[0-9a-z]+\-+[A-Za-z]+'  	#Date  string pattern regEx
compPattern = '[A-Z]+[a-z\s]+[A-Z]+[a-z]+'				#Competition string pattern regEx

#loop through each of the fixtures in the fixture list and add to a dictionary
#fixtures = {}

#fixture_date = str(aDay) + '/3/2018'
fixture_date = input("Enter the date: ")
for aFixture in fixture_list:
	aHomeTeamScore = None
	aHomeData = aFixture.find('span',attrs={'class': 'sp-c-fixture__team sp-c-fixture__team--home'})
	if aHomeData is not None:
		aHomeTeamScore = aHomeData.find('span',attrs={'class': 'sp-c-fixture__number sp-c-fixture__number--home sp-c-fixture__number--ft'})
	if aHomeTeamScore is not None:
		compAndDateString = aFixture['data-reactid']							#extract the string from the 'data-reactid' attribute that holds the competition and the date
		competition = re.search(compPattern, compAndDateString)					#extract the competition from the extracted attribute string
		theDate = re.search(datePattern, compAndDateString)
		aAwayData = aFixture.find('span',attrs={'class':'sp-c-fixture__team sp-c-fixture__team--away'})
		aHomeTeam = aHomeData.find('span',attrs={'class': 'gs-u-display-none gs-u-display-block@m qa-full-team-name sp-c-fixture__team-name-trunc'}).text
		aHomeTeamScore = aHomeData.find('span',attrs={'class': 'sp-c-fixture__number sp-c-fixture__number--home sp-c-fixture__number--ft'}).text
		aAwayTeam = aAwayData.find('span',attrs={'class':'gs-u-display-none gs-u-display-block@m qa-full-team-name sp-c-fixture__team-name-trunc'}).text
		aAwayTeamScore = aAwayData.find('span',attrs={'class':'sp-c-fixture__number sp-c-fixture__number--away sp-c-fixture__number--ft'}).text
		result = ""
		if aHomeTeamScore > aAwayTeamScore:
			result = "H"
		elif aAwayTeamScore > aHomeTeamScore:
			result = "A"
		else:
			result = "D"
		# output the result to the scores file
		writer = csv.writer(scores_file)
		writer.writerow([fixture_date,aHomeTeam,aHomeTeamScore,aAwayTeam,aAwayTeamScore,result,competition.group(0),theDate.group(0)])



		#fixtures[fixture]
