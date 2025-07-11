from PIL import Image
import os
import glob

# Caminho da pasta onde estão as imagens PNG
pasta = r'C:\Users\Breno\Documents\Códigos\projetos\louise_tcc\geo_jet_gb\output'

# Padrão para encontrar todas as imagens PNG
padrao_imagens = os.path.join(pasta, 'geo-jet_*.png')

# Lista e ordena os arquivos de imagem
lista_imagens = sorted(glob.glob(padrao_imagens))
print("Imagens encontradas:", lista_imagens)

# Verifica se encontrou imagens
if not lista_imagens:
    print("❌ Nenhuma imagem encontrada. Verifique o caminho ou padrão de nome dos arquivos.")
    exit()

# Abre todas as imagens usando PIL
imagens = [Image.open(img) for img in lista_imagens]

# Define caminho completo COM nome do arquivo .gif
saida_gif = r'C:\Users\Breno\Documents\Códigos\projetos\louise_tcc\geo_jet_gb\src\animacao.gif'

# Salva como GIF animado
imagens[0].save(
    saida_gif,
    save_all=True,
    append_images=imagens[1:],
    duration=300,
    loop=0
)

print(f'✅ GIF criado com sucesso: {saida_gif}')
