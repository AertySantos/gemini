from google import genai
from google.genai import types
import time
import os

client = genai.Client(api_key="your key")
tempo_inicial = time.time()

def enviar_msg(doc):

    contexto = f"""A partir do texto fornecido, extraia apenas as informações que estiverem explicitamente presentes, sem interpretar ou inferir nada.

                    Informações a serem extraídas:
                    1. Todos os títulos ou assuntos mencionados no texto.
                    2. A data presente no documento.
                    3. O nome da empresa.
                    4. O nome e o registro do contador.

                    Texto:
                    {doc}"""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction="Voce é um contador"),
        contents = contexto
    )

    print(response.text)
    return response.text

def leitura():
    global tempo_inicial
   
    directory_path = "contabil"
   
    # Loop sobre os arquivos .pdf no diretório especificado
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):  # Verifica se é um arquivo .txt
            file_path = os.path.join(directory_path, filename)
            
            # Lendo o conteúdo do arquivo TXT
            with open(file_path, "r", encoding="utf-8") as file:
                arquivo = file.read()
            resp = enviar_msg(arquivo)
           
            #print(resp)
           
            if resp is None:
                print("Erro: result é None. Verifique a função que retorna este valor.")
            else:
                file_path2 = os.path.join("contabil_extracao", filename)
                
                with open(file_path2, "a", newline="", encoding="utf-8") as arquivo:
                    arquivo.write(resp)
                

            if contador >= 10:
                tempoEspera = 61 - (time.time() - tempo_inicial)
                print(tempoEspera)
                time.sleep(tempoEspera)
                contador = 0
                tempo_inicial = time.time()


leitura()