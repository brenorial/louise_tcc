# 📡 Geração de Mapas Meteorológicos a partir de Arquivo GRIB (.grib)

Este projeto foi desenvolvido como parte de um **trabalho de Meteorologia** para minha noiva, com o objetivo de gerar mapas de **geopotencial em 500 hPa** e **linhas de corrente do vento** a partir de um arquivo meteorológico no formato **GRIB**, utilizando bibliotecas científicas em Python como `xarray`, `metpy`, `cartopy` e `matplotlib`.

## 🛰️ Objetivo

- Ler e processar dados meteorológicos (vento e geopotencial) a partir de um arquivo `.grib`.
- Selecionar um intervalo temporal e espacial.
- Gerar mapas com:
  - Sombreamento do campo de **geopotencial em 500 hPa**
  - Linhas de corrente do campo de **vento em 500 hPa**
  - Contornos políticos (UFs do Brasil)

## 🗂️ Estrutura

```

LOUISE\_TCC/
│
├── data/
│   ├── grib/                # Arquivo .grib meteorológico
│   └── shapefiles/          # Shapefile do Brasil (BR\_UF\_2022.\*)
│
├── output/
│   └── geradas/                # Imagens geradas pelo script
├── venv/                    # Ambiente virtual (não versionado)
├── geo_gb.py                # Arquivo python gerador das imagens
├── requirements.txt         # Dependências do projeto
├── README.md                # Este arquivo
└── .gitignore               # Itens a ignorar no controle de versão

````

## ▶️ Como executar

1. Clone este repositório:

```bash
git clone https://github.com/brenorial/LOUISE_TCC.git
cd LOUISE_TCC
````

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Execute o script:

```bash
python scripts/run_geo_plot.py
```

> As imagens serão salvas na pasta `output/geradas/`.

## 🧩 Dependências principais

* [`xarray`](https://docs.xarray.dev/)
* [`metpy`](https://unidata.github.io/MetPy/)
* [`cartopy`](https://scitools.org.uk/cartopy/docs/latest/)
* [`matplotlib`](https://matplotlib.org/)
* [`cfgrib`](https://github.com/ecmwf/cfgrib)

## 🧠 Observações

* O shapefile `BR_UF_2022.*` deve estar completo (com `.shp`, `.shx`, `.dbf`, `.prj`).

* O GRIB precisa conter variáveis `u`, `v`, `z` e tempo no nível de 500 hPa.

* O arquivo GRIB utilizado (GEOGB.grib) já contém os dados em um único nível de pressão (500 hPa), portanto não é necessário fazer seleção de níveis com .sel(isobaricInhPa=500).

* A coordenada de nível (isobaricInhPa) pode ser omitida na leitura, pois os dados já estão nesse nível por padrão.

* Os dados foram processados entre 02/02/2014 e 01/03/2014, e cada imagem gerada representa uma análise meteorológica daquele instante.

* O shapefile BR_UF_2022 precisa estar completo, contendo .shp, .shx, .dbf, e .prj.

* As imagens de saída estão no formato .png e nomeadas com base na data/hora (geo_MM-DD-HHZ.png).



