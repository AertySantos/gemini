import csv
import re

def convert_to_days(time_str):
    """Converte um tempo no formato 'X anos, Y meses e Z dias' para dias totais."""
    anos = meses = dias = 0
    
    # Expressões regulares para capturar os valores
    anos_match = re.search(r"(\d+)\s*anos?", time_str)
    meses_match = re.search(r"(\d+)\s*meses?", time_str)
    dias_match = re.search(r"(\d+)\s*dias?", time_str)
    
    if anos_match:
        anos = int(anos_match.group(1))
    if meses_match:
        meses = int(meses_match.group(1))
    if dias_match:
        dias = int(dias_match.group(1))
    
    # Conversão: 1 ano = 365 dias, 1 mês ≈ 30 dias
    total_dias = (anos * 365) + (meses * 30) + dias
    return total_dias

# Ler e processar o arquivo CSV
input_file = "furtoSimples2.csv"
output_file = "dados_processados.csv"

with open(input_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    rows = []
    
    for row in reader:
        if len(row) >= 6:  # Garante que há pelo menos duas colunas de tempo
            row.append(convert_to_days(row[-2]))  # Converte penúltima coluna
            row.append(convert_to_days(row[-2]))  # Converte última coluna
            print(row)
        rows.append(row)

# Escrever o novo CSV com os tempos convertidos
with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    writer.writerows(rows)

print(f"Arquivo processado salvo como {output_file}")
