from flask import Flask, request
import pandas as pd
import json
import requests
import os

app = Flask(__name__)

# Dicionário para guardar o estado de cada cliente
clientes = {}

@app.route('/webhook', methods=['POST'])
def receber_mensagem():
    data = request.json
    print('Recebido webhook:', data)  # DEBUG para verificar as mensagens recebidas

    if not data or 'message' not in data:
        return 'OK'

    numero = data['message']['from']
    # Limpa o número para remover sufixos, deixando só os números
    numero = numero.split('@')[0]

    mensagem = data['message']['body'].strip()

    if numero not in clientes:
        clientes[numero] = {'etapa': 1, 'nome': '', 'servico': '', 'endereco': ''}
        enviar_mensagem(numero, 'Olá! Sou o assistente virtual do Renato Carvalho.\nQual o seu *nome completo*?')
        return 'OK'

    etapa = clientes[numero]['etapa']

    if etapa == 1:
        clientes[numero]['nome'] = mensagem
        clientes[numero]['etapa'] = 2
        enviar_mensagem(numero, 'Perfeito, obrigado.\nAgora, qual *serviço você deseja*?')

    elif etapa == 2:
        clientes[numero]['servico'] = mensagem
        clientes[numero]['etapa'] = 3
        enviar_mensagem(numero, 'Ótimo!\nAgora me informe o *endereço completo* com CEP, por favor.')

    elif etapa == 3:
        clientes[numero]['endereco'] = mensagem
        # salvar_dados(clientes[numero])  # Comentado para evitar erros no Railway
        enviar_mensagem(numero, '✅ Obrigado! Seus dados foram enviados. Em breve nossa equipe entrará em contato 😊')
        del clientes[numero]  # Limpa da memória

    return 'OK'

def enviar_mensagem(telefone, texto):
    url = 'https://api.z-api.io/instances/3E32A7C5E4BCD0A341925674B530B88A/token/BD8F59C666DC3053A0AEFFFB/send-text'
    payload = {
        "phone": telefone,
        "message": texto
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=json.dumps(payload), headers=headers)

# def salvar_dados(dados):
#     df = pd.DataFrame([dados])
#     try:
#         df_antigo = pd.read_csv('clientes.csv')
#         df = pd.concat([df_antigo, df], ignore_index=True)
#     except FileNotFoundError:
#         pass
#     df.to_csv('clientes.csv', index=False)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

