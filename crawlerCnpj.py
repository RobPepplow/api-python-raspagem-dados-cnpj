import requests
from bs4 import BeautifulSoup
import json
import re

def crawler(
    cnpj: str, 
    escritorio: str, 
    escritorioId: str,
    tributacao: str,
    codigoEstabelecimento: str
    ) -> str:
    link = f'https://cnpj.biz/{cnpj}'
    
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    resposta = requests.get(link, headers=headers)
    #resposta = requests.get(link)

    if resposta.status_code == 200:
        soup = BeautifulSoup(resposta.text, 'html.parser')
        dados = {}
        elementos_copy = soup.find_all('b', class_='copy')
        
        for elemento_b in elementos_copy:
            elemento_p = elemento_b.find_previous('p')

            if elemento_p:
                texto_p = elemento_p.get_text(strip=True).split(":")[0].strip()
                texto_b = elemento_b.get_text(strip=True)
                dados[texto_p] = texto_b
                
        nomeRua = dados.get("Logradouro", "").split(",")[0].strip() 
        numeroCasa = dados.get("Logradouro", "").split(",")[1].strip()  
        cep = dados.get("CEP", "")        
       
        # Remove caracteres não alfanuméricos, espaços e hífens do CEP
        cep = re.sub(r'[^a-zA-Z0-9\s-]', '', cep)

        # Faz a solicitação HTTP para a API do ViaCEP
        url = f"https://viacep.com.br/ws/{cep}/json/"
        response = requests.get(url)

        # Verifica se a solicitação foi bem-sucedida
        if response.status_code == 200:
            data = response.json()
            if 'erro' not in data:
                print("CEP encontrado:")
                print(f"CEP: {data['cep']}")
                print(f"Logradouro: {data['logradouro']}")
                print(f"Bairro: {data['bairro']}")
                print(f"Cidade: {data['localidade']}")
                print(f"Estado: {data['uf']}")
            else:
                print("CEP não encontrado.")
        else:
            print("Falha ao buscar o CEP. Verifique sua conexão ou tente novamente mais tarde.")     
            
        if 'localidade' in data:
            cidade = data['localidade']
        else:
            cidade = ""

        if 'uf' in data:
            uf = data['uf']
        else:
            uf = ""       
        
        dados_Formatados_front = {
            "inscEstadual": "Não Tem",
            "msg": "Não tem",
            "cidade": cidade,
            "uf": uf,
            "situacao": dados.get("Situação", "") ,
            "importaNfe": False,
            "escritorio": escritorio,
            "autFgts": False,
            "autMunicipal": False,
            "cnpj": cnpj,
            "numeroAlvara": "0",
            "capturaNfe": False,
            "inscMunicipal": "Não Tem",
            "escritorioId": escritorioId,
            "cep": dados.get("CEP", ""),           
            "nomeFantasia": dados.get("Razão Social", ""),
            "complemento": dados.get("Complemento", ""),
            "inscMunicipalAbreviado": "0",
            "autCertidao": False,
            "autTst": False,           
            "autFederal": False,
            "email": "naotem@naotem.com",
            "nomeRua": nomeRua,
            "bairro": dados.get("Bairro", ""),
            "numeroCasa": numeroCasa,
            "autEstadual": False,
            "active": True,
            "foneFixo": "4199999999",
            "nfe": True,
            "certification": False,
            "tributacao": tributacao,
            "foneCelResp": "41999999999",
            "codigoEstabelecimento": codigoEstabelecimento,
            "razaoSocial": dados.get("Razão Social", ""),
            "nomeResponsavel": "Não Tem"
        }

        return json.dumps({"result": dados_Formatados_front}, ensure_ascii=False, indent=4)
    else:
        error_message = f"Erro na requisição: {resposta.status_code}"
        return json.dumps({"error_message": error_message})

