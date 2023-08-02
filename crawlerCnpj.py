import requests
from bs4 import BeautifulSoup
import json

def crawler(
    cnpj: str, 
    escritorio: str, 
    escritorioId: str,
    tributacao: str,
    codigoEstabelecimento: str
    ) -> str:
    link = f'https://cnpj.biz/{cnpj}'
    resposta = requests.get(link)

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
        
        dados_Formatados_front = {
            "inscEstadual": "Não Tem",
            "msg": "Não tem",
            "cidade": "",
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
            "uf": "Pr",
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
            "active": False,
            "foneFixo": "4199999999",
            "nfe": False,
            "certification": False,
            "tributacao": tributacao,
            "foneCelResp": "41999999999",
            "codigoEstabelecimento": codigoEstabelecimento,
            "razaoSocial": dados.get("Razão Social", ""),
            "nomeResponsavel": "Não Tem"
        }

        dados = json.dumps({"result": dados_Formatados_front}, ensure_ascii=False, indent=4)
        return dados
    else:
        return f'Erro na requisição: {resposta.status_code}'

