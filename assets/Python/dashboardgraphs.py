import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.animation as ani
import folium
import os
from folium.features import DivIcon
import matplotlib.pyplot as plt 



training_data =pd.read_excel(r"C:\Users\jake\Documents\AtlanticCampaignGitHub\Atlantic2025\assets\TrainingData\TrainingBlogTimeLapse.xlsx",sheet_name='Logs')
training_data['Week_of_year'] = training_data['Date'].dt.isocalendar().week
training_data['Year'] = training_data['Date'].dt.isocalendar().year
training_data['Epoch'] = (training_data['Year']-2022)*52 +training_data['Week_of_year'] -45
train_groupby = training_data.groupby('Epoch',as_index=False)[['ErgDistance / km','RiverDistance / km','OceanDistance / km']].sum()


fig, ax = plt.subplots()

x_value = train_groupby['Epoch'].to_numpy()
Erg = train_groupby['ErgDistance / km'].to_numpy()
River = train_groupby['RiverDistance / km'].to_numpy()
Ocean = train_groupby['OceanDistance / km'].to_numpy()


ax.bar(x_value, Erg, color = "#FF00FF", alpha = 0.8,label ='Erg Distance' )
ax.bar(x_value, River, bottom = Erg, color = "blue", alpha = 0.8,label = 'River Distance')
ax.bar(x_value, Ocean, bottom = River, color = "cyan", alpha = 0.8,label = 'Ocean Distance')

ax.vlines([4],0,105,colors='black',ls='--',label='Capsize')
ax.vlines([43],0,105,colors='red',ls='--',label='Great Ouse Marathon 2023')
ax.vlines([47],0,105,colors='green',ls='--',label='Ancholme Head Race 2023')

ax.legend(loc="upper center", 
           ncol=2,prop={'size': 6})
ax.set_xlabel('Week Number from $13^{th}$ Nov 2022')
ax.set_ylabel('Weekly Distance / km ')
plt.savefig(r'C:\Users\jake\Documents\AtlanticCampaignGitHub\Atlantic2025\assets\Python\Outputs\TrainingBarChart\BarChartDistance.png')
plt.show()



geo_location_data =pd.read_excel(r"C:\Users\jake\Documents\AtlanticCampaignGitHub\Atlantic2025\assets\TrainingData\TrainingBlogTimeLapse.xlsx",sheet_name='WeeklyTotalsCoords')
geo_location_data = gpd.GeoDataFrame(geo_location_data,geometry=gpd.points_from_xy(geo_location_data['Longitude'],geo_location_data['Latitude']),crs='epsg:4326')
geo_location_data



atlantic = folium.Map(location = [22.9619825306386, -41.243511983153894],
                                        zoom_start = 5)

tile = folium.TileLayer(
        tiles = 'https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
        attr = 'Google',
        name = 'Google Maps',
        overlay = True,
        control = True
       ).add_to(atlantic)
atlantic


from html2image import Html2Image
hti = Html2Image(output_path=r'C:\Users\jake\Documents\AtlanticCampaignGitHub\Atlantic2025\assets\Python\Outputs\RowingGeoPath',custom_flags=['--virtual-time-budget=100000', '--hide-scrollbars'])

coords = geo_location_data[['Latitude','Longitude']].to_numpy().tolist()
count = 0
frames = []
for i in np.arange(len(coords)):

    atlantic = folium.Map(location = [22.9619825306386, -41.243511983153894],
                                        zoom_start = 5)

    tile = folium.TileLayer(
            tiles = 'https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
            attr = 'Google',
            name = 'Google Maps',
            overlay = True,
            control = True
        ).add_to(atlantic)
    atlantic
    

    if i ==0:
        folium.Marker(coords[0],icon=folium.Icon(color='purple',icon_color='purple')).add_to(atlantic)
        folium.Marker([17.008242247569843, -61.76391832037273],icon=folium.Icon(color='black',icon_color='black')).add_to(atlantic)
    else:
        distance = np.sum(geo_location_data['Distance'].to_numpy()[0:i+1])
        folium.Marker(coords[0],icon=folium.Icon(color='purple',icon_color='purple')).add_to(atlantic)
        folium.Marker([17.008242247569843, -61.76391832037273],icon=folium.Icon(color='black',icon_color='black')).add_to(atlantic)
        folium.Marker(
            [33.25296265319919, -41.49012299347318],
                icon=DivIcon(
            
            
            html=f'<div style="font-size: 16pt">Distance:{np.round(distance)}km   Week:{i} </div>'
                )
                ).add_to(atlantic)
        folium.PolyLine(coords[0:i+1], color='black').add_to(atlantic)
        
    filepath = os.path.join(r"C:\Users\jake\Documents\AtlanticCampaignGitHub\Atlantic2025\assets\Python\Outputs\RowingGeoPath","Image"+str(count)+".html")
    atlantic.save(filepath)
    
    hti.screenshot(html_file=filepath,save_as="Image"+str(count)+".jpg").append(frames)
    count+=1


import glob
from PIL import Image
def number(filename):
    return int(filename[101:-4])

frames = [Image.open(image) for image in sorted(glob.glob(r"C:\Users\jake\Documents\AtlanticCampaignGitHub\Atlantic2025\assets\Python\Outputs\RowingGeoPath/*.jpg"),key=number)]


frame_one = frames[0]
frame_one.save(r'C:\Users\jake\Documents\AtlanticCampaignGitHub\Atlantic2025\assets\Python\Outputs\RowingGeoPath\Rowing.gif', format="GIF", append_images=frames,
                   save_all=True, duration=250, loop=0)