import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import csv
import pandas as pd
import requests

model_name = "Qwen/Qwen2.5-Coder-32B-Instruct-GPTQ-Int4"

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="cuda:1"
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

def enviar_msg(doc):

    prompt = doc
    contexto2 = """Extraia apenas os seguintes dados do texto fornecido para cada acusado (se houver mais de um):

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
                    O CSV não deve incluir o título das colunas."""

    messages = [
    {"role": "system", "content": "You are Qwen. You are a helpful assistant."},
    {"role": "user", "content": f"{contexto2} segue o texto: {prompt}"}
    ]

        
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    # Obter a quantidade de tokens
    num_tokens = len(model_inputs['input_ids'][0])  # Acessa os tokens tokenizados
    print(num_tokens)

    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=512
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return response

def leitura():
    directory_path ="sentencas"
    output_path = "resposta.txt"
    # Loop sobre os arquivos .txt no diretório especificado
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):  # Verifica se é um arquivo .txt
            file_path = os.path.join(directory_path, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            arquivo = file.read()
            print(f"Arquivo: {filename}")
            resp = enviar_msg(arquivo)
            print(resp)

            with open(output_path, 'a', encoding='utf-8') as output_file:
                output_file.write(f"{filename}, ")
                output_file.write(f"{resp}\n")

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
        #if contador >= 3:
        #    break
        res = result.split(',')
        with open("furtoSimples.csv", "a", newline="", encoding="utf-8") as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow(res)
        print(str(res))

leituraUrl()