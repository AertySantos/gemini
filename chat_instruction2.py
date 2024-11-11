import google.generativeai as genai
import xml.etree.ElementTree as ET

genai.configure(api_key="")

def extract_xml(xml_path):
    # Carrega o XML
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    extracted_text = ""
    
    # Itera sobre todas as tags e extrai o texto
    for elem in root.iter():
        if elem.text:
            extracted_text += elem.text.strip() + " "
    
    return extracted_text.strip()
    
instruction = (
    "Você é um especialista em codificação que se especializa em XML. "
    "Quando eu descrever um componente de um site que quero construir, "
    "retorne o XML correspondente. Não forneça uma explicação para este código."
)

sample_file = extract_xml('ead_0000000571_balancetes-das-financas-municipais.xml')

for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)

model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=instruction)

chat = model.start_chat(history=sample_file)

#while True:
#texto = input("Escreva sua mensagem: ")
texto = ("Crie um novo xml do tipo <ead>, conforme as instruções abaixo e o exemplos anteriores com as especificidades das instruções, preencha o máximo de campos possíveis baseado nas instruções, sem informações fictícias:"
            "Nível 0 contém o Nó Raiz Institution"
            "Nível 1 contém o Nó Other docs e nó Newspaper"
            "Nível 2 contém os Nós filhos de Newspaper (Folio_1, Folio_2)"
            "Nível 3 Folio 1 contém os nós filhos (A, B)" 
            "Nível 3 Folio 2 contém o nó filho (Z)"
            )
#if texto == "sair":
    #break

response = model.generate_content(
                texto,
                generation_config=genai.types.GenerationConfig(
                    # Only one candidate for now.
                    candidate_count=1,
                    max_output_tokens=700,
                    temperature=0.2,
                ),
    )
print(response.text, "\n")

print("Encerrando Chat")
