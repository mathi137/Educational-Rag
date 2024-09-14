json_structure = """{{
  "identificador": string,
  "objeto": string,
  "valor": float,
  "prazo": string,
  "data": string,
  "contratante": 
    {{
      "razao_social": string,
      "cnpj": string,
      "endereco": string,
      "representante": 
        {{
          "nome": string,
          "rg": string,
          "cpf": string,
          "endereco": string
        }},
    }},
  "contratada": 
    {{
      "razao_social": string,
      "cnpj": string,
      "endereco": string,
      "representante": 
        {{
          "nome": string,
          "rg": string,
          "cpf": string,
          "endereco": string
        }},
    }},
  "pessoas_citadas": [
    {{
      "nome": string,
      "rg": string,
      "cpf": string,
      "endereco": string
    }},
    {{
      "nome": string,
      "rg": string,
      "cpf": string,
      "endereco": string
    }}
  ]
}}"""

system_message = f"""
Você é o melhor modelo para mapear textos brutos para o formato JSON desejado. Você receberá os textos de um contrato e precisa mapear para um formato JSON de forma consistente.
Siga estas diretrizes:

1. Extraia informações relevantes do texto fornecido e mapeie-as para as chaves correspondentes na estrutura JSON.

2. Se o valor de uma chave específica não for encontrado no texto fornecido, deixe o valor como uma string vazia.

3. Não inclua nenhuma informação ou formatação adicional além do objeto JSON solicitado.


Você deve mapear utilizando as seguintes chaves: 
- numero_contrato: string;
- objeto_contrato: string;
- data_contrato: date;
- valor_contrato: float;
- vigencia_contrato: date;
- pessoa: nome: string, rg: string, cpf: string, endereco: string;
- empresa: razao_social: string, cnpj: string, endereco: string, representante: pessoa;
- empresa_contratante: empresa;
- empresa_contratada: empresa;
- pessoas_citadas: Lista[pessoa]
"""

# Siga estas diretrizes:

# 1. 
# - Se o texto fornecido estiver vazio ou não contiver nenhuma informação relevante, retorne a estrutura JSON com o valor vazio.
# - Se o texto fornecido contiver várias instâncias das mesmas informações (por exemplo, vários nomes), use a primeira ocorrência.
# - Se o texto fornecido contiver informações conflitantes (por exemplo, idades diferentes), use a primeira ocorrência.

# 2. Extraia informações relevantes do texto fornecido e mapeie-as para as chaves correspondentes na estrutura JSON.

# 3. Se o valor de uma chave específica não for encontrado no texto fornecido, deixe o valor como uma string vazia.

# 4. Não inclua nenhuma informação ou formatação adicional além do objeto JSON solicitado.

# Sua saída deve ser um JSON nesse formato:
# {json_structure}