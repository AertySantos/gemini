import google.generativeai as genai

genai.configure(api_key="AIzaSyDRqsqYIknTr8_zdN6WyCyyJqduDgDYdns")

instruction = (
    "Você é um especialista em codificação que se especializa em XML. "
    "Quando eu descrever um componente de um site que quero construir, "
    "retorne o XML correspondente. Não forneça uma explicação para este código."
)

for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)

model = genai.GenerativeModel('gemini-1.5-pro-latest', system_instruction=instruction)

chat = model.start_chat(history=[])

bem_vindo = "# Bem Vindo ao Assistente Gemini #"
print(len(bem_vindo) * "#")
print(bem_vindo)
print(len(bem_vindo) * "#")
print("###   Digite 'sair' para encerrar    ###")
print("")

while True:
    texto = input("Escreva sua mensagem: ")

    if texto == "sair":
        break

    response = model.generate_content(
                texto,
                generation_config=genai.types.GenerationConfig(
                    # Only one candidate for now.
                    candidate_count=1,
                    stop_sequences=["x"],
                    max_output_tokens=20,
                    temperature=1.0,
                ),
    )
    print("Gemini:", response.text, "\n")

print("Encerrando Chat")