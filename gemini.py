from google import genai
from google.genai import types
import csv
import pandas as pd
import requests
import time

client = genai.Client(api_key="AIzaSyDSa7weo4h2_Z2EU4jS4lMUxYYSp6OtuTE")
tempo_inicial = time.time()

def enviar_msg(doc):

    contexto = f"""Extraia apenas os seguintes dados do texto fornecido para cada acusado (se houver mais de um):

                        Número do processo

                        Assunto

                        Comarca

                        Vara

                        Juiz

                        Pena-base: [tempo de reclusão inicial], quando não tiver coloque N/A, sem o tempo de multa;

                        Pena Definitiva: [tempo de reclusão final], quando não tiver coloque N/A, sem o tempo de multa;
                        Não informe o tempo de multa.
                        Não inclua explicações ou detalhes adicionais.
                        colunas separadas por ";"

                        Formate os resultados em CSV, onde cada linha representa um processo.
                        O CSV não deve incluir o título das colunas.
                        segue o texto: {doc}"""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction="Voce é um advogado"),
        contents = contexto
    )

    print(response.text)
    return response.text

def extracao(texto):         
    # Baixa o conteúdo do arquivo TXT
    url = texto.strip()  # remove espaços em branco extras, se houver
    if not url:
        return "URL vazia"
    try:
        response = requests.get(url)
        response.raise_for_status()  # dispara um erro se o status não for 200
        texto =  response.text
        
    except requests.RequestException as e:
        return f"Erro ao acessar {url}: {e}"
    
    return texto

def leituraUrl():
    global tempo_inicial
    df = pd.read_csv('processos-furtoSimples.csv', encoding='utf-8', delimiter=",")
    contador = 1
    
    for index, row in df.iterrows():
        #print("Linha:", row)
        link = f"http://200.137.66.21/tjsp/law-tjsp/decisoes/dados/{str(row.iloc[0].strip())}.txt"
        linhas = len(df)
        por = round((contador/linhas)*100,2)
        print(f"\r{link} {por}%",end='',flush=True)
        contador += 1
        
        texto = extracao(link)
        
        result = enviar_msg(texto)

        print(result)
        #if contador >= 4:
        #   break
        if result is None:
            print("Erro: result é None. Verifique a função que retorna este valor.")
        else:
            res = res = result.replace('"', '').replace("'", "").replace("\n", "").strip().split(',')
            with open("furtoSimples2.csv", "a", newline="", encoding="utf-8") as arquivo:
                escritor = csv.writer(arquivo)
                escritor.writerow(res)
            print(str(res))

        if contador >= 10:
            tempoEspera = 61 - (time.time() - tempo_inicial)
            print(tempoEspera)
            time.sleep(tempoEspera)
            contador = 0
            tempo_inicial = time.time()

leituraUrl()


