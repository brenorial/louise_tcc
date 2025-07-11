#Importando as bibliotecas
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr

#Importando o dataset
file = xr.open_dataset(r'temp_gp\data\temp_gb.grib')

file_1 = file.metpy.parse_cf().sel(time=slice('2014-01-01T00:00:00',
                                              '2014-03-01T03:00:00'))

file_1['longitude'] = (((file_1.longitude + 180) % 360) - 180
                       ).sortby('longitude')

#Definindo o intervalo espacial
lon_slice = slice(-90., -20., 1)
lat_slice = slice(10., -60., 1)

lats = file_1.latitude.sel(latitude=lat_slice).values
lons = file_1.longitude.sel(longitude=lon_slice).values

for i in range(len(file_1.variables['time'])):
    
    u = file_1['u10'].metpy.sel(
        time=file_1.time[i], latitude=lat_slice, longitude=lon_slice
        ).metpy.unit_array.squeeze()
    
    v = file_1['v10'].metpy.sel(
        time=file_1.time[i], latitude=lat_slice, longitude=lon_slice
        ).metpy.unit_array.squeeze()
    
    T = file_1['t2m'].metpy.sel(
        time=file_1.time[i], latitude=lat_slice, longitude=lon_slice
        ).metpy.unit_array.squeeze().to('degC')
    
    plt.figure(figsize=(25, 25)) #Criando a figura
    
    #Definindo a projeção da Coordenada Cilíndrica Equidistante
    ax = plt.axes(projection=ccrs.PlateCarree())
    
    #Adicionando contornos políticos
    shp = list(
        shpreader.Reader(
            r'shapes\BR_UF_2022.shp'
        ).geometries()
    )

    ax.add_geometries(
        shp, ccrs.PlateCarree(),
        edgecolor='black',
        facecolor='none',
        linewidth=0.5
    )
    
    #Adicionando limites e bordas
    ax.coastlines(resolution='50m', color='black', linewidth=1)
    ax.add_feature(cfeature.BORDERS, edgecolor='black', linewidth=1)
    gl = ax.gridlines(crs=ccrs.PlateCarree(),
                      color='gray',
                      alpha=1.0,
                      linestyle='--',
                      linewidth=0.5,
                      xlocs=np.arange(-180, 180, 10),
                      ylocs=np.arange(-90, 90, 10),
                      draw_labels=True
                      )
    gl.top_labels = False; gl.right_labels = False
    gl.xlabel_style = {'size': 30}; gl.ylabel_style = {'size': 30}
    
    #Adicionando a máscara de terra
    ax.add_feature(cfeature.LAND)
    
    #Intervalos de temperatura
    intervalo_min = 0
    intervalo_max = 34
    interval = 1
    levels = np.arange(intervalo_min, intervalo_max, interval)
    
    #Plotando temperatura em 2m
    sombreado = ax.contourf(lons,
                            lats,
                            T,
                            cmap='RdYlBu_r',
                            linewidth=1.0,
                            levels=levels,
                            extend='both'
                            )
    
    #Plotando temperatura em 2m
    vetor = ax.streamplot(lons,
                          lats, 
                          u.magnitude, 
                          v.magnitude,
                          density=[1,1],
                          color='black', 
                          linewidth=1.5, 
                          arrowsize=3
                          )
    
    #Adicionando a barra de cores
    barra_de_cores = plt.colorbar(sombreado,
                                  orientation='horizontal',
                                  pad=0.04,
                                  fraction=0.03
                                  )
    barra_de_cores.ax.tick_params(labelsize=25)
    
    #Extraindo a data e hora do elemento
    data_hora = file_1.time[i].values
    data = pd.to_datetime(data_hora)
    data_formatada = data.strftime('%Y-%m-%d %H')
    
    #Adicionado o título
    plt.title('Temperatura [ºC] em 2 m — Sombreado\n'
              + 'Vento [m/s] em 10 m — Linha de corrente',
              fontweight='bold', 
              fontsize=30, 
              loc='left'
              )
    
    plt.title(f'{data_formatada}Z',
              fontweight='bold', 
              fontsize=30, 
              loc='right'
              )
    #Salvando a figura
    data_formatada2 = data.strftime('%m-%d-%H')
    plt.savefig(f'temp_gp\output\geopotencial_{data_formatada2}Z.png', 
                bbox_inches='tight')
    
    plt.close()