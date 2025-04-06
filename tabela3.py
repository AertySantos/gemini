import csv
import string

# Definir os arquivos de entrada e saída
csv_arquivo1 = "processos-furtoSimples.csv"
csv_arquivo2 = "furtoSimples2.csv"
csv_saida = "resultado.csv"

# Ler os valores da primeira coluna do primeiro CSV
valores_csv1 = set()
with open(csv_arquivo1, newline="", encoding="utf-8") as f1:
    reader = csv.reader(f1)
    next(reader)  # Pular cabeçalho, se houver
    for row in reader:
        valores_csv1.add(row[0])  # Assume-se que a primeira coluna contém os valores-chave

# Função para limpar texto: remove espaços e pontuações
def limpar_texto(texto):
    return texto.translate(str.maketrans('', '', string.punctuation)).replace(" ", "").lower()

# Limpar todos os valores do primeiro CSV
valores_csv1_limpos = set(limpar_texto(valor) for valor in valores_csv1)

# Abrir o segundo CSV e criar um novo CSV com as linhas correspondentes
with open(csv_arquivo2, newline="", encoding="utf-8") as f2, open(csv_saida, "w", newline="", encoding="utf-8") as f_out:
    reader = csv.reader(f2, delimiter=';')
    writer = csv.writer(f_out)

    header = next(reader)  # Ler cabeçalho do segundo CSV
    writer.writerow(header)  # Escrever cabeçalho no novo CSV
    linha = 0

    linhas_unicas = set()  # Armazena linhas já escritas
    linha_count = 0

    for row in reader:
        valor_limpo = limpar_texto(row[0])  # Limpar o valor da primeira coluna
        linha_str = ";".join(row)  # Criar uma string única para a linha
        
        if valor_limpo in valores_csv1_limpos and linha_str not in linhas_unicas:
            writer.writerow(row)
            linhas_unicas.add(linha_str)  # Adicionar a linha ao conjunto
            print(f"Linha adicionada: {linha_str}")
            linha_count += 1
    print(linha_count)
print(f"Arquivo '{csv_saida}' gerado com sucesso.")
