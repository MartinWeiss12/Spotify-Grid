import os
import json
import time
import math
import spotipy
import requests
import pandas as pd
from PIL import Image
import spotipy.util as util
from datetime import datetime
from bs4 import BeautifulSoup as soup
from spotipy.oauth2 import SpotifyClientCredentials

start_time = datetime.now()
start_time = start_time.strftime('%H:%M:%S')
print('Start Time:', start_time)
startTimerSec = time.time()
startTimerSec = time.time()
path = r'' #path of your spotify top tracks excel file
outputPath = '' #path where to output your spotify grid
imageFolderPath = '' #path for the folder that will store artist images
data = pd.read_excel(path)
rankList = (data['Rank']).tolist()
trackList = (data['Track']).tolist()
streamList = (data['Streams']).tolist()
trackUriList = (data['URI']).tolist()

artistUriList = []
print('Total Tracks:', len(trackUriList))
for uri in range(len(trackUriList)):
	goodLink = False
	while not goodLink:
		spotifyUrl = requests.get('https://open.spotify.com/track/' + str(trackUriList[uri]))
		if('200' in str(spotifyUrl)):
			goodLink = True
		else:
			goodLink = False
			print('Webpage Error. URI:', uri+1, spotifyUrl)
	bodyText = str(soup(spotifyUrl.text, 'html.parser'))
	bodyTextInfo = bodyText.split('<')
	try:
		try:
			artistUriData = bodyTextInfo[39]
			artistUriData = artistUriData.split('/')
			artistUriData = artistUriData[4].split('"')
			artistUriList.append(artistUriData[0])
		except:
			artistUriData = bodyTextInfo[34]
			artistUriData = artistUriData.split('/')
			artistUriData = artistUriData[4].split('"')
			artistUriList.append(artistUriData[0])
		print(uri+1)
	except:
		print('Error: Song Deleted From Spotify. URI:', uri+1)
		artistUriList.append('Error')
		
artistUriDf = pd.DataFrame(list(zip(rankList, trackList, trackUriList, streamList, artistUriList)), columns = ['Rank', 'Track', 'Track URI', 'Streams', 'Artist URI'])
for row in artistUriDf.index:
	if(artistUriDf['Artist URI'][row] == 'Error'):
		artistUriDf.drop([row], axis = 0, inplace = True)
artistUriDfPivot = artistUriDf.pivot_table(index = ['Artist URI'], values = ['Streams'], aggfunc = 'sum').reset_index('Artist URI')
artistUriDfPivot = artistUriDfPivot.sort_values(by = 'Streams', ascending = False)
rankList = []
for artist in range(artistUriDfPivot.shape[0]):
	rankList.append(artist+1)
artistUriDfPivot.insert(0, 'Rank', rankList)
uniqueArtistUriList = artistUriDfPivot['Artist URI'].tolist()

cid = ''
secret = ''
username = ''
redirect_uri = 'http://localhost:8888/callback'
scope = 'user-top-read playlist-modify-public'
token = util.prompt_for_user_token(username, scope, client_id = cid, client_secret = secret, redirect_uri = redirect_uri)
if token:
	sp = spotipy.Spotify(auth = token)

artistImageUrlList = []
print('Total artists streamed:', len(uniqueArtistUriList))
for uri in range(49):
	spotifyUrl = requests.get('https://open.spotify.com/artist/' + str(uniqueArtistUriList[uri]))
	spoifyHtmlData = str(soup(spotifyUrl.text, 'html.parser'))
	spoifyHtmlData = spoifyHtmlData.split('<')
	artistName = spoifyHtmlData[5].split('>')
	artistName = artistName[1].split('|')
	artistApiResults = requests.get('https://api.spotify.com/v1/search', headers={ 'authorization': 'Bearer ' + token}, params={ 'q': artistName[0], 'type': 'artist' })
	artistSearchResults = str(soup(artistApiResults.text, 'html.parser'))
	artistInfoJson = json.loads(artistSearchResults)
	listFromDict = artistInfoJson['artists']['items']
	artistImageUrl = listFromDict[0]['images'][0]['url']
	for i in range(len(listFromDict)):
		if(artistName[0].strip() == listFromDict[i]['name']):
			artistImageUrlList.append(artistImageUrl)
			break

for image in range(len(artistImageUrlList)):
	artistImageUrl = requests.get(artistImageUrlList[image])
	filename = 'artist_' + str(image+1) + '.png'
	with open(os.path.join(imageFolderPath, filename), 'wb') as out:
		out.write(artistImageUrl.content)

spotifyArtistGrid = Image.new('RGB', (1000, 1000))
for i in range(1, 2):
	imagePath = imageFolderPath + '/artist_' + str(i) + '.png'
	artistImage = Image.open(imagePath)
	artistImage = artistImage.resize((400, 400))
	spotifyArtistGrid.paste(artistImage, (300, 300))
for i in range(2, 6):
	imagePath = imageFolderPath + '/artist_' + str(i) + '.png'
	artistImage = Image.open(imagePath)
	artistImage = artistImage.resize((200, 200))
	spotifyArtistGrid.paste(artistImage, (-300+(i*200), 100))
for i in range(6, 9):
	imagePath = imageFolderPath + '/artist_' + str(i) + '.png'
	artistImage = Image.open(imagePath)
	artistImage = artistImage.resize((200, 200))
	spotifyArtistGrid.paste(artistImage, (700, -900+(i*200)))
for i in range(9, 12):
	imagePath = imageFolderPath + '/artist_' + str(i) + '.png'
	artistImage = Image.open(imagePath)
	artistImage = artistImage.resize((200, 200))
	spotifyArtistGrid.paste(artistImage, (2300-(i*200), 700))
for i in range(12, 14):
	imagePath = imageFolderPath + '/artist_' + str(i) + '.png'
	artistImage = Image.open(imagePath)
	artistImage = artistImage.resize((200, 200))
	spotifyArtistGrid.paste(artistImage, (100, 2900-(i*200)))
for i in range(14, 24):
	imagePath = imageFolderPath + '/artist_' + str(i) + '.png'
	artistImage = Image.open(imagePath)
	artistImage = artistImage.resize((100, 100))
	spotifyArtistGrid.paste(artistImage, (-1400+(i*100), 0))
for i in range(24, 33):
	imagePath = imageFolderPath + '/artist_' + str(i) + '.png'
	artistImage = Image.open(imagePath)
	artistImage = artistImage.resize((100, 100))
	spotifyArtistGrid.paste(artistImage, (900, -2300+(i*100)))
for i in range(33, 42):
	imagePath = imageFolderPath + '/artist_' + str(i) + '.png'
	artistImage = Image.open(imagePath)
	artistImage = artistImage.resize((100, 100))
	spotifyArtistGrid.paste(artistImage, (4100-(i*100), 900))
for i in range(42, 50):
	imagePath = imageFolderPath + '/artist_' + str(i) + '.png'
	artistImage = Image.open(imagePath)
	artistImage = artistImage.resize((100, 100))
	spotifyArtistGrid.paste(artistImage, (0, 5000-(i*100)))
spotifyArtistGrid = spotifyArtistGrid.save('spotifyArtistGrid.png')

end_time = datetime.now()
end_time = end_time.strftime('%H:%M:%S')
print('Start Time:', start_time)
print('End Time:', end_time)