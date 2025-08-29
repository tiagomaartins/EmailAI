from flask import Flask, render_template, request, jsonify
import fitz  
import os
import json
import re
from openai import OpenAI  

app = Flask(__name__)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def extrair_texto(file):
    """Extrai texto de arquivos .txt ou .pdf"""
    if file.filename.endswith(".txt"):
        return file.read().decode("utf-8")
    elif file.filename.endswith(".pdf"):
        pdf = fitz.open(stream=file.read(), filetype="pdf")
        texto = ""
        for page in pdf:
            texto += page.get_text()
        return texto
    else:
        return None

def classificar_e_responder(email_texto: str):
    """Classifica o email e sugere uma resposta curta em JSON válido"""
    system_prompt = (
        "Você é um assistente especializado em análise de emails corporativos.\n"
        "Sua tarefa é:\n"
        "1. Classificar o email recebido em uma das categorias:\n"
        "   - 'Produtivo' quando o email contém solicitação, informação relevante, pedido de ação, dúvida "
        "ou qualquer conteúdo que exija resposta ou acompanhamento.\n"
        "   - 'Improdutivo' quando o email não demanda ação, contém apenas saudações, mensagens automáticas, "
        "propagandas irrelevantes ou conteúdos sem utilidade prática.\n"
        "   - 'Erro' se o conteúdo não puder ser interpretado ou estiver vazio.\n\n"
        "2. Sugerir uma resposta curta, clara, educada e adequada ao conteúdo do email.\n\n"
        "Instruções importantes:\n"
        "- Retorne exclusivamente JSON válido, sem texto adicional.\n"
        "- O JSON deve sempre seguir este formato:\n\n"
        "{\n"
        '  "categoria": "Produtivo" | "Improdutivo" | "Erro",\n'
        '  "resposta": "Texto da resposta sugerida"\n'
        "}\n"
    )

    user_prompt = f"Email:\n\"\"\"{email_texto}\"\"\""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0,
            max_tokens=150
        )

        content = response.choices[0].message.content.strip()

        match = re.search(r'\{.*\}', content, re.DOTALL)
        if match:
            resultado = json.loads(match.group())
        else:
            resultado = {
                "categoria": "Erro",
                "resposta": "Não foi possível gerar uma resposta válida do modelo."
            }

    except Exception as e:
        print("Erro na API OpenAI:", e)
        resultado = {
            "categoria": "Erro",
            "resposta": "Não foi possível processar o email."
        }

    return resultado

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/processar", methods=["POST"])
def processar():
    texto_email = ""
 
    if "arquivo" in request.files and request.files["arquivo"].filename != "":
        arquivo = request.files["arquivo"]
        texto_email = extrair_texto(arquivo)
        if texto_email is None:
            return jsonify({
                "categoria": "Erro",
                "resposta": "Formato de arquivo não suportado."
            })
    elif "texto_email" in request.form and request.form["texto_email"].strip() != "":
        texto_email = request.form["texto_email"]
    else:
        return jsonify({
            "categoria": "Erro",
            "resposta": "Nenhum arquivo ou texto enviado."
        })

    resultado = classificar_e_responder(texto_email)
    return jsonify(resultado)

if __name__ == "__main__":
    app.run(debug=True)
