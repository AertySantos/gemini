import google.generativeai as genai

genai.configure(api_key="AIzaSyDRqsqYIknTr8_zdN6WyCyyJqduDgDYdns")

for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)

model = genai.GenerativeModel('gemini-pro')

response = model.generate_content("Quem descobriu o Brasil?")

print(response.text)