import os
import time
import math
import requests
import pandas as pd
from PIL import Image
from datetime import datetime
from bs4 import BeautifulSoup as soup

start_time = datetime.now()
start_time = start_time.strftime('%H:%M:%S')
print('Start Time:', start_time)
startTimerSec = time.time()
path = r'' #path of your spotify top tracks excel file
outputPath = '' #path where to output your spotify grid
imageFolderPath = '' #path for the folder that will store album cover images
data = pd.read_excel(path)
rankList = (data['Rank']).tolist()
trackList = (data['Track']).tolist()
streamList = (data['Streams']).tolist()
trackUriList = (data['URI']).tolist()
albumUriList = []

print('Total Tracks:', len(trackUriList))
for uri in range(len(trackUriList)):
	spotifyUrl = requests.get('https://open.spotify.com/track/' + str(trackUriList[uri]))
	spoifyHtmlData = soup(spotifyUrl.text, 'html.parser')
	divData = str(spoifyHtmlData.find('div', {'class': 'TS85Qkpioa31wR0p4kzT'}))
	if(divData != 'None'):
		divData = divData.split('=')
		albumUrl = divData[5]
		albumUrl = albumUrl.split('"')
		albumUriList.append(albumUrl[1].replace('/album/', ''))
		print(uri+1)

albumUriDf = pd.DataFrame(list(zip(rankList, trackList, streamList, albumUriList)), columns = ['Rank', 'Track', 'Streams', 'Album URI'])
albumUriDf.to_excel(f'{outputPath}/albumUriDf_test.xlsx', index = False)
albumUriDfPivot = albumUriDf.pivot_table(index = ['Album URI'], values = ['Streams'], aggfunc = 'sum').reset_index('Album URI')
albumUriDfPivot = albumUriDfPivot.sort_values(by = 'Streams', ascending = False)
rankList = []
for album in range(albumUriDfPivot.shape[0]):
	rankList.append(album+1)
albumUriDfPivot.insert(0, 'Rank', rankList)
uniqueAlbumUriList = albumUriDfPivot['Album URI'].tolist()

albumImageUrlList = []
for uri in range(49):
	spotifyUrl = requests.get('https://open.spotify.com/album/' + str(uniqueAlbumUriList[uri]))
	bodyText = str(soup(spotifyUrl.text, 'html.parser'))
	bodyTextInfo = bodyText.split('<')
	albumImageData = bodyTextInfo[24]
	albumImageData = albumImageData.split('"')
	albumImageUrlList.append(albumImageData[1])
	
for image in range(len(albumImageUrlList)):
	albumImageUrl = requests.get(albumImageUrlList[image])
	filename = 'album_' + str(image+1) + '.png'
	with open(os.path.join(imageFolderPath, filename), 'wb') as out:
		out.write(albumImageUrl.content)

spotifyAlbumGrid = Image.new('RGB', (1000, 1000))
for i in range(1, 2):
	imagePath = imageFolderPath + '/album_' + str(i) + '.png'
	albumImage = Image.open(imagePath)
	albumImage = albumImage.resize((400, 400))
	spotifyAlbumGrid.paste(albumImage, (300, 300))
for i in range(2, 6):
	imagePath = imageFolderPath + '/album_' + str(i) + '.png'
	albumImage = Image.open(imagePath)
	albumImage = albumImage.resize((200, 200))
	spotifyAlbumGrid.paste(albumImage, (-300+(i*200), 100))
for i in range(6, 9):
	imagePath = imageFolderPath + '/album_' + str(i) + '.png'
	albumImage = Image.open(imagePath)
	albumImage = albumImage.resize((200, 200))
	spotifyAlbumGrid.paste(albumImage, (700, -900+(i*200)))
for i in range(9, 12):
	imagePath = imageFolderPath + '/album_' + str(i) + '.png'
	albumImage = Image.open(imagePath)
	albumImage = albumImage.resize((200, 200))
	spotifyAlbumGrid.paste(albumImage, (2300-(i*200), 700))
for i in range(12, 14):
	imagePath = imageFolderPath + '/album_' + str(i) + '.png'
	albumImage = Image.open(imagePath)
	albumImage = albumImage.resize((200, 200))
	spotifyAlbumGrid.paste(albumImage, (100, 2900-(i*200)))
for i in range(14, 24):
	imagePath = imageFolderPath + '/album_' + str(i) + '.png'
	albumImage = Image.open(imagePath)
	albumImage = albumImage.resize((100, 100))
	spotifyAlbumGrid.paste(albumImage, (-1400+(i*100), 0))
for i in range(24, 33):
	imagePath = imageFolderPath + '/album_' + str(i) + '.png'
	albumImage = Image.open(imagePath)
	albumImage = albumImage.resize((100, 100))
	spotifyAlbumGrid.paste(albumImage, (900, -2300+(i*100)))
for i in range(33, 42):
	imagePath = imageFolderPath + '/album_' + str(i) + '.png'
	albumImage = Image.open(imagePath)
	albumImage = albumImage.resize((100, 100))
	spotifyAlbumGrid.paste(albumImage, (4100-(i*100), 900))
for i in range(42, 50):
	imagePath = imageFolderPath + '/album_' + str(i) + '.png'
	albumImage = Image.open(imagePath)
	albumImage = albumImage.resize((100, 100))
	spotifyAlbumGrid.paste(albumImage, (0, 5000-(i*100)))
spotifyAlbumGrid = spotifyAlbumGrid.save('spotifyAlbumGrid.png')

end_time = datetime.now()
end_time = end_time.strftime('%H:%M:%S')
print('Start Time:', start_time)
print('End Time:', end_time)