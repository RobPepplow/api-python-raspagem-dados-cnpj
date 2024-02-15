from flask import Flask, request, jsonify
from flask_cors import CORS
from crawlerCnpj import crawler
import json

app = Flask(__name__)
CORS(app)

@app.route('/')
def resposta():
    return "Api Crawler Cnpj - Está no Ar"

@app.route('/api/crawler/cnpj', methods=['POST'])
def crawler_dados_cnpj():
    data = request.get_json()

    cnpj = data['cnpj']
    escritorio = data['escritorio']
    escritorioId = data['escritorioId']
    tributacao = data['tributacao']
    codigoEstabelecimento = data['codigoEstabelecimento']
    codigoInterno= data['codigoInterno']
    cfopRet= data['cfopRet']
    cfop= data['cfop']
    produto= data['produto']
    nfe= data['nfe']
    nfse= data['nfse']
    padrao= data['padrao']
    usuarioReceita= data['usuarioReceita']
    usuarioPrefeitura= data['usuarioPrefeitura']
    senhaReceita= data['senhaReceita']
    senhaPrefeitura= data['senhaPrefeitura']

    resultado = crawler(
        cnpj=cnpj,
        escritorio=escritorio,
        escritorioId=escritorioId,
        tributacao=tributacao,
        codigoEstabelecimento=codigoEstabelecimento,
        codigoInterno= codigoInterno,
        cfopRet= cfopRet,
        cfop= cfop,
        produto= produto,
        nfe= nfe,
        nfse= nfse,
        padrao= padrao,
        usuarioReceita= usuarioReceita,
        usuarioPrefeitura= usuarioPrefeitura,
        senhaReceita= senhaReceita,
        senhaPrefeitura= senhaPrefeitura,
    )

    if resultado:
        
        parsed_resultado = json.loads(resultado)
        response = {
            "message": "Dados extraídos com Sucesso!",
            "success": True,
            **parsed_resultado,  
            "errors": None
        }

        return jsonify(response)
    else:
        response = {
            "message": "Nenhum resultado encontrado.",
            "success": False,
            "result": {},
            "errors": None
        }
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True, port=3333)



#para executar uso python main.py e não flask run 