import folium
import os
import pandas as pd
import numpy as np
from folium.plugins import GroupedLayerControl, FeatureGroupSubGroup


SIZE = 100

def plotTMA(m):  
    tma=[]
    tma_df = pd.DataFrame(pd.read_excel('MAPAS TMA.xlsx', sheet_name='TERMINAL'), columns=['COORD LAT', 'COORD LONG'])
    print(tma_df)
    for index, row in tma_df.iterrows():
        tma.append([row['COORD LAT'], row['COORD LONG']])
    folium.Polygon(
        locations=tma,
        color="black",
        weight=1,
        fill=False,
    ).add_to(m)
    
def plotAD(m, fg):
    airdrome_df = pd.DataFrame(pd.read_excel('MAPAS TMA.xlsx', sheet_name='AERODROMOS'), columns=['NOME', 'COORD LAT', 'COORD LONG'])
    print(airdrome_df)
    for index, row in airdrome_df.iterrows():
        icon = selectIcon("airdrome.png",5, 0, 0)
        location = [row['COORD LAT'], row['COORD LONG']]
        folium.Marker(
        location=location, icon=icon, popup=row['NOME']
        ).add_to(fg)
        

def plotCharts(m, fg_list):
    charts_df = pd.DataFrame(pd.read_excel('MAPAS TMA.xlsx', sheet_name='CARTA_COORD'))
    points_df = pd.DataFrame(pd.read_excel('MAPAS TMA.xlsx', sheet_name='PONTOS')).set_index(['ID'])
    print(points_df)
    for index, row in charts_df.iterrows():
        line = []
        file = row['COR'] + '.png'
        fg= next(
            (obj for obj in fg_list if obj.layer_name == row['NOME']),
            None
        )
        for col in row:
            icon = selectIcon(file, 6, 10, 10)
            try:
                point = points_df.loc[col]
                num_col = str(row[row==col].index[0])
                restriction = str(row["RESTRIÇÃO "+num_col[1:]])
                location = (point.iloc[2], point.iloc[3])
            # add points to line
                line.append([point.iloc[2], point.iloc[3]])
            #plot points
                if "RWY" in point.iloc[0] or "DER" in point.iloc[0]: #if is a rwy, then dont plot or put label
                    print("RWY is plotted in another way")
                    continue
                plotLabel(m, location, point.iloc[0], restriction, fg, row["POSIÇÃO TEXTO"], row['NOME'])
                folium.Marker(
                location=location, icon=icon
                ).add_to(fg)
            except Exception as e:
                print("Excep: "+ str(e))
                
        #plot lines     
        folium.PolyLine(
        locations=line,
        color=row['COR'],
        weight=2,
        tooltip=row.iloc[0],
        ).add_to(fg)

    


def selectIcon(file_name:str, ratio:int|float, anchor_x:int, anchor_y:int):
    os.chdir("./assets")
    icon_image = file_name
    icon = folium.CustomIcon(
    icon_image,
    icon_size=(SIZE/ratio, SIZE/ratio),
    icon_anchor=(anchor_x, anchor_y),
    popup_anchor=(15, 10),
    )
    os.chdir("../")
    return icon

def plotLabel(m, location, name, res, fg_chart, position,chart):
    location_res = [location[0]-.015*position, location[1]+.005*position]
    location_name = [location[0]-.0060, location[1]+.01]
    folium.Marker(location=location_name,
                  popup=chart,
                  icon=folium.DivIcon(html=name,
                  class_name="mapText"),
                  ).add_to(fg_chart)
    if res == 'nan':
        pass
    else:
        folium.Marker(location=location_res,
                      popup=chart,
                      icon=folium.DivIcon(html=res,
                      class_name="mapText"),
                      ).add_to(fg_chart)
    
def createGroups(m):
    #create groups
    charts_df = pd.DataFrame(pd.read_excel('MAPAS TMA.xlsx', sheet_name='CARTA_COORD'))
    rwy_df = pd.DataFrame(pd.read_excel('MAPAS TMA.xlsx', sheet_name='PISTAS'))
    submaps_name = []
    submaps_rwy = []
    submapsFG = []
    charts_dic = {}
    rwyFG = {}
    
    #iterates over charts dataframe and update values of variables
    for index, row in charts_df.iterrows():
        submaps_name.append(row.iloc[0])
        charts_dic.update({row.iloc[0]: row.iloc[1]})
    print(submaps_name)
    #iterates over rwys dataframe and update values of rwys available
    for index, row in rwy_df.iterrows():
        submaps_rwy.append(row.iloc[0])
    print(submaps_rwy)
        
    #create map for ADs
    rwyFG.update({"Aerodromos":folium.FeatureGroup(name='Aeródromos', show=True)}) 
    m.add_child(rwyFG.get("Aerodromos"))
    
    #create map for RWYs
    for rwy in submaps_rwy:
        if rwy == "SBCF 16" or rwy == "SBBH 13":
            isVisible = True
        else:
            isVisible = False
        group = folium.FeatureGroup(name=rwy, show=isVisible)
        rwyFG.update({rwy: group})
        m.add_child(group)
    print(submaps_rwy)
    
    #create submap for charts
    for submap in submaps_name:
        subgroup = FeatureGroupSubGroup(group=rwyFG.get(charts_dic.get(submap)),name=submap, show=True)
        submapsFG.append(subgroup) 
        m.add_child(subgroup)
    print(submapsFG)
    

    #populate groups
    plotTMA(m)
    plotAD(m, rwyFG.get("Aerodromos"))
    plotCharts(m, submapsFG)
