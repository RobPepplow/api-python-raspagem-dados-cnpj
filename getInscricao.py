import requests

def getInscricao(cnpj: str) -> str:
    url = 'https://bot-busca-im-ctba-l3cizs4bqa-uc.a.run.app/api/crawler/insc-municipal/pr/ctba'
    #url = 'http://127.0.0.1:5000/api/crawler/insc-municipal/pr/ctba'
    dados = {'cnpj': cnpj}
    resposta = requests.post(url, json=dados)
    
    if resposta.status_code == 200:
      
        dados_json = resposta.json()
        inscricao_municipal = dados_json.get('inscMunicipal', '')
        return inscricao_municipal
    else:
       
        print('Erro ao buscar inscrição municipal')
        return ''
