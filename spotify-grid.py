import os
import requests
import pandas as pd
from PIL import Image

# path for the excel file for your top albums
top_albums = pd.read_excel('')
# path for the excel file for your top artists
top_artists = pd.read_excel('')
# path for an empty folder named 'Album-Images' where the album images will be saved to
album_images = ''
# path for an empty folder named 'Artist-Images' where the artist images will be saved to
artist_images = ''

def download_images(folder, type):
	top_49 = folder[f'{type} Image URL'][:49]
	folder_path = os.path.abspath(f'{type}-Images')
	for i, url in enumerate(top_49):
		with open(os.path.join(folder_path, f'{type}-{i+1}.png'), 'wb') as file:
			file.write(requests.get(url).content)

download_images(top_albums, 'Album')
download_images(top_artists, 'Artist')

def make_grid(path, grid_type):
	
	grid = Image.new('RGB', (8000, 8000))
	list = [f'{path}/{grid_type}-{i}.png' for i in range(1, 50)]
	
	for i, img in enumerate(list, start=1):
		if i == 1:
			image = Image.open(img).resize((3200, 3200))
			grid.paste(image, (2400, 2400))
		if i >= 2 and i <= 4:
			image = Image.open(img).resize((1600, 1600))
			grid.paste(image, (-2400+(i*1600), 800))
		if i >= 5 and i <= 8:
			image = Image.open(img).resize((1600, 1600))
			grid.paste(image, (5600, -7200+(i*1600)))
		if i >= 9 and i <= 11:
			image = Image.open(img).resize((1600, 1600))
			grid.paste(image, (18400-(i*1600), 5600))
		if i >= 12 and i <= 13:
			image = Image.open(img).resize((1600, 1600))
			grid.paste(image, (800, 23200-(i*1600)))
		if i >= 14 and i <= 23:
			image = Image.open(img).resize((800, 800))
			grid.paste(image, (-11200+(i*800), 0))
		if i >= 24 and i <= 32:
			image = Image.open(img).resize((800, 800))
			grid.paste(image, (7200, -18400+(i*800)))
		if i >= 33 and i <= 41:
			image = Image.open(img).resize((800, 800))
			grid.paste(image, (32800-(i*800), 7200))
		if i >= 42 and i <= 49:
			image = Image.open(img).resize((800, 800))
			grid.paste(image, (0, 40000-(i*800)))
			
	grid.save(f'{grid_type}-grid.png')
	return grid

album_grid = make_grid(album_images, 'Album')
artist_grid = make_grid(artist_images, 'Artist')
