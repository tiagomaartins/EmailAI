# EmailAI
Aplicação web simples que permite enviar um texto ou arquivo (.txt ou .pdf) contendo o corpo de um e-mail para análise automática. A API utiliza Flask e integração com a OpenAI para classificar os e-mails em Produtivo, Improdutivo ou Erro, além de sugerir uma resposta curta e adequada.

O que dá pra fazer aqui:
Enviar texto direto ou subir um arquivo .txt ou .pdf.
Descobrir se o e-mail é Produtivo, Improdutivo ou se não faz sentido (Erro).
Receber uma resposta curta já pronta pra usar.

Tecnologias que usei
Flask - pra rodar a aplicação web.
PyMuPDF - pra ler PDFs.
OpenAI API - pra dar inteligência na classificação e na resposta.

Como rodar: 
1. Clone o projeto
   
3. Crie e ative um ambiente virtual:
     python -m venv venv
     venv\Scripts\activate
   
5. Instale as dependências:
     pip install -r requirements.txt
   
7. Configure a variável de ambiente da sua API Key da OpenAI:
     setx OPENAI_API_KEY "sua_chave_aqui"
   
9. Execute a aplicação:
     flask run
   
11. Acesse no seu navegador: 
    http://127.0.0.1:5000

