# Análise de Ventos com Dados Meteorológicos – Projeto TCC

Este projeto tem como objetivo gerar visualizações animadas da magnitude e direção dos ventos em altos níveis da atmosfera sobre a América do Sul, utilizando dados meteorológicos em formato GRIB (do ECMWF/ERA5). O código foi desenvolvido como parte de um Trabalho de Conclusão de Curso (TCC) da UFRJ, para minha noiva Louise.

## 📁 Estrutura do Projeto

```
louise_tcc/
│
├── geo_jet_gb/              # Análises e visualizações com dados de Jato
│   ├── geo_jet_gb.py        # Script principal de análise
│   └── src/
│       ├── animacao.gif     # GIF gerado com os vetores de vento
│       └── png_to_gif.py    # Script que converte PNGs em GIF
│
├── geo_gb/                  # Outro conjunto de análise semelhante
│   ├── geo_gb.py            # Script alternativo
│   └── src/
│       ├── animacao.gif
│       └── png_to_gif.py
│
├── shapes/                  # Arquivos vetoriais para contorno político
│   └── BR_UF_2022.*         # Shapefiles do Brasil (estados)
│
└── temp_gp/                 # Pasta temporária com testes
    └── temp_gb.py
```

---

## ⚙️ Requisitos

Instale as bibliotecas com o seguinte comando:

```bash
pip install -r requirements.txt
```

### `requirements.txt` inclui:

* `xarray`
* `numpy`
* `pandas`
* `matplotlib`
* `cartopy`
* `metpy`
* `Pillow`

---

## 📊 O que o script faz 

1. **Carrega dados meteorológicos** em formato GRIB (`geo_era5.grib`), contendo componentes zonal (u) e meridional (v) do vento.
2. **Seleciona uma janela temporal** entre janeiro e março de 2014.
3. **Recorta espacialmente** para América do Sul com latitude de 10°N a 60°S e longitude de 170°W a 20°W.
4. **Calcula o módulo do vetor vento**:
   $\text{magnitude} = \sqrt{u^2 + v^2}$
5. **Gera mapas vetoriais de vento** com Cartopy (projeção `PlateCarree`) e contorno dos estados do Brasil.
6. **Salva os mapas como imagens**.
7. **Cria uma animação em GIF** com os vetores de vento ao longo do tempo.

---

## 🗺️ Observações Técnicas

* Divido o código em três pastas principais, onde `geo_gb` desenvolve mapas relacionados a geopotencial, `geo_jet_gb`, ao jato de ar, e por fim, a temperatura em `temp_gb`
* O shapefile `BR_UF_2022.shp` é utilizado para desenhar os contornos dos estados brasileiros.
* O GRIB usado já está **pré-processado para o nível de pressão desejado** (ex: 250 hPa), facilitando a análise do jato.
* Os scripts estão prontos para ser usados em ambiente local com os dados correspondentes,independente do usuário local. Basta subir os dados retirados do ERA5 para a pasta `data`.

---

## 🖼️ Resultado Esperado

O resultado final é um GIF com vetores de vento animados mostrando a evolução temporal do jato subtropical sobre a América do Sul.

---

## ▶️ Como executar

1. Coloque o arquivo `geo_era5.grib` dentro de `geo_jet_gb/data/`.
2. Execute:

```bash
python geo_jet_gb.py
```

3. Depois, rode o script para gerar o GIF:

```bash
python src/png_to_gif.py
```

---
