#Importando as bibliotecas
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr

#Importando o dataset
file_a = xr.open_dataset(r'geo_jet_gb\data\geo_era5.grib')
file_b = xr.open_dataset(r'geo_jet_gb\data\geo_era5.grib')

file_1 = file_a.metpy.parse_cf().sel(time=slice('2014-01-03T00:00:00',
                                                    '2014-03-01T12:00:00'))

file_1['longitude'] = (((file_1.longitude + 180) % 360) - 180
                       ).sortby('longitude')

file_2 = file_a.metpy.parse_cf().sel(time=slice('2014-01-01T00:00:00',
                                                    '2014-03-01T12:00:00'))
file_2['longitude'] = (((file_1.longitude + 180) % 360) - 180
                       ).sortby('longitude')

print(file_2.data_vars)

#Definindo o intervalo espacial
lon_slice = slice(-170., -20., 1)
lat_slice = slice(10., -60., 1)

lats = file_1.latitude.sel(latitude=lat_slice).values
lons = file_1.longitude.sel(longitude=lon_slice).values


for i in range(len(file_1.variables['time'])):   

    u = file_2.u.metpy.sel(
        time=file_1.time[i],
        latitude=lat_slice,
        longitude=lon_slice
    ).metpy.unit_array.squeeze()

    v = file_2.v.metpy.sel(
        time=file_1.time[i],
        latitude=lat_slice,
        longitude=lon_slice
    ).metpy.unit_array.squeeze()

    
    mag = np.sqrt(u**2+v**2)
    
    plt.figure(figsize=(25, 25)) #Criando a figura
    
    #Definindo a projeção da Coordenada Cilíndrica Equidistante
    ax = plt.axes(projection=ccrs.PlateCarree())
    
    #Adicionando contornos políticos
    shp = list(
        shpreader.Reader(
            r'C:\Users\Breno\Documents\Códigos\projetos\louise_tcc\shapes\BR_UF_2022.shp'
        ).geometries()
    )

    ax.add_geometries(
        shp, ccrs.PlateCarree(),
        edgecolor='gray',
        facecolor='none',
        linewidth=0.5
    )
    
    #Adicionando limites e bordas
    ax.coastlines(resolution='50m', color='gray', linewidth=1)
    ax.add_feature(cfeature.BORDERS, edgecolor='gray', linewidth=1)
    gl = ax.gridlines(crs=ccrs.PlateCarree(),
                      color='gray',
                      alpha=1.0,
                      linestyle='--',
                      linewidth=0.5,
                      xlocs=np.arange(-180, 180, 20),
                      ylocs=np.arange(-90, 90, 10),
                      draw_labels=True
                      )
    gl.top_labels = False; gl.right_labels = False
    gl.xlabel_style = {'size': 30}; gl.ylabel_style = {'size': 30}
    
    #Adicionando a máscara de terra
    ax.add_feature(cfeature.LAND)

    #Intervalos
    intervalo_min_geo = 5000
    intervalo_max_geo = 5900
    interval_geo = 50
    levels_geo = np.arange(intervalo_min_geo, intervalo_max_geo, interval_geo)
    
    intervalo_min_pnmm = 960
    intervalo_max_pnmm = 1044
    interval_pnmm = 4
    levels_pnmm = np.arange(intervalo_min_pnmm, intervalo_max_pnmm, interval_pnmm)
    
    intervalo_min_mag = 30
    intervalo_max_mag = 80
    interval_mag = 2
    levels_mag = np.arange(intervalo_min_mag, intervalo_max_mag, interval_mag)
    
    #Plotando a água total da coluna atmosférica (ou água precipitável)
    sombreado = ax.contourf(lons,
                        lats,
                        mag,
                        cmap='twilight',
                        levels=levels_mag,
                        extend='max'
                        )
    
    # Linhas de corrente (streamlines) do vento
    ax.streamplot(
        lons,
        lats,
        u.magnitude,
        v.magnitude,
        density=2.2,
        color='black',
        linewidth=1.0,
        arrowsize=2.5
    )

    
    contorno = ax.contour(
        lons,
        lats,
        mag,
        colors='black',
        linewidths=2,
        levels=levels_pnmm,
        extend='none'
    )

    ax.clabel(contorno, inline_spacing=3, fontsize=17, colors= 'black')
    #Adicionando a barra de cores
    barra_de_cores = plt.colorbar(sombreado,
                                  orientation='horizontal',
                                  pad=0.04,
                                  fraction=0.03
                                  )
    barra_de_cores.ax.tick_params(labelsize=30)
    
    #Extraindo a data e hora do elemento
    data_hora = file_1.time[i].values
    data = pd.to_datetime(data_hora)
    data_formatada = data.strftime('%Y-%m-%d %H')
    
    #Adicionado o título
    plt.title(f'Vento [m/s] em {250} hPa',
              fontweight='bold', 
              fontsize=25, 
              loc='left'
              )
    
    plt.title(f'{data_formatada}Z',
              fontweight='bold', 
              fontsize=25, 
              loc='right'
              )
    
    #Salvando a figura
    data_formatada2 = data.strftime('%m-%d-%H')
    plt.savefig(f'C:/Users/Breno/Documents/Códigos/projetos/louise_tcc/geo_jet_gb/output/geo-jet_{data_formatada2}Z.png', 
                bbox_inches='tight')
    
    plt.close()