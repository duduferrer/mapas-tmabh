import folium
import branca
import mapPlotting
from folium.plugins import MousePosition, Draw



gray_tile = branca.utilities.image_to_url(image="")

attr_sat_map = (
    'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
)
sat_map = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'


m = folium.Map(location=(-19.62444444,-43.97194444,),
               tiles=None,
               zoom_start=9,
               )
	
sm_gray = folium.TileLayer(tiles=gray_tile, attr="Eduardo Ferrer - 2023 - Cartas TMA BH", name="Padrão Cinza").add_to(m)
sm_map = folium.TileLayer('openstreetmap', name="Mapa").add_to(m)
sm_sat = folium.TileLayer(tiles=sat_map, attr=attr_sat_map, name="Satélite").add_to(m)
mapPlotting.createGroups(m)

fmtr_lat = ("function(num) { var str = num.toString(); var splitted = str.split('.'); var dgr = parseInt(splitted[0]); var i=1; var multi = 10; while (i< splitted[1].length){ multi = multi*10; i++; }; var min = parseFloat(splitted[1])/multi*60; str = min.toString(); splitted = str.split('.'); min = parseInt(splitted[0]); i=1; multi = 10; while (i< splitted[1].length){ multi = multi*10; i++; }; var sec = parseFloat(splitted[1])/multi*60; str = sec.toString(); splitted = str.split('.'); sec = parseInt(splitted[0]); var dir = 's'; if(dgr<0){ dir = 's'; dgr=dgr*-1; }else{ dir='n'; }; return dir+dgr+'º'+min.toString().padStart(2, 0)+`'`+sec.toString().padStart(2, 0)+'\"';};")                                      
fmtr_lng = ("function(num) { var str = num.toString(); var splitted = str.split('.'); var dgr = parseInt(splitted[0]); var i=1; var multi = 10; while (i< splitted[1].length){ multi = multi*10; i++; }; var min = parseFloat(splitted[1])/multi*60; str = min.toString(); splitted = str.split('.'); min = parseInt(splitted[0]); i=1; multi = 10; while (i< splitted[1].length){ multi = multi*10; i++; }; var sec = parseFloat(splitted[1])/multi*60; str = sec.toString(); splitted = str.split('.'); sec = parseInt(splitted[0]); var dir = 'w'; if(dgr<0){ dir = 'w'; dgr=dgr*-1; }else{ dir='e'; }; return dir+dgr.toString().padStart(3, 0)+'º'+min.toString().padStart(2, 0)+`'`+sec.toString().padStart(2, 0)+'\"';};")                                      

MousePosition(lat_formatter=fmtr_lat,
              lng_formatter=fmtr_lng).add_to(m)

Draw(export=True, draw_options={"polyline": {"nautic": True, "metric": False, "feet":False}}).add_to(m)
folium.LayerControl(collapsed=True).add_to(m)
m.save("index.html")


