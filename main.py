import pandas as pd
import unicodedata
import pyphen

# Função para identificar e contar o número de ACENTOS de cada palavra
def extrair_tipo_acento(palavra_loop):
    if not isinstance(palavra_loop, str):
        return None, 0
    palavra_nfd = unicodedata.normalize("NFD", palavra_loop)

    diacriticos = {
        "\u0301": "agudo (´)",
        "\u0302": "circunflexo (^)",
        "\u0303": "til (~)",
        "\u0300": "crase (`)",
        "\u0327": "cedilha (ç)",
        "\u0308": "trema (¨)",
    }

    acentos_encontrados = []
    soma = 0

    for char in palavra_nfd:
        if unicodedata.category(char) == "Mn" and char in diacriticos:
            soma += 1
            acento = diacriticos[char]
            if acento not in acentos_encontrados:
                acentos_encontrados.append(acento)
    tipo_final = (", ".join(acentos_encontrados) if acentos_encontrados else None)
    return tipo_final, soma

# Função para contar o número de SÍLABAS e identificar a classificação das palavras
def contar_silabas(palavra_loop):
    dic = pyphen.Pyphen(lang="pt_BR")
    separado = dic.inserted(str(palavra_loop))
    numero_silabas = len(separado.split("-"))

    if numero_silabas == 1:
        classificacao = "Monossílaba"
    elif numero_silabas == 2:
        classificacao = "Dissílaba"
    elif numero_silabas == 3:
        classificacao = "Trissílaba"
    else:
        classificacao = "Polissílaba"
    return numero_silabas, classificacao
    
# Função para calcular o PESO de cada palavra
def calcular_pesos(categoria, qtd_silabas, qtd_acentos):
    if categoria == "regulares":
        calculo = (1) + qtd_silabas + qtd_acentos
        return calculo
    elif categoria == "irregulares":
        calculo = (2) + qtd_silabas + qtd_acentos
        return calculo
    elif categoria == "dígrafo consonantal":
        calculo = (3) + qtd_silabas + qtd_acentos
        return calculo
    elif categoria == "sílabas CVC" or categoria == "sílabas CCV":
        calculo = (4) + qtd_silabas + qtd_acentos
        return calculo

# Manipulação dos .csv
df_resultados = pd.read_csv("palavra.csv", sep=";")
df_palavras = df_resultados["palavra"]

df_resultados["tipo de acento"] = None
df_resultados["classificação por número de sílabas"] = None

df_resultados["tipo de acento"] = df_resultados["tipo de acento"].astype(object)
df_resultados["classificação por número de sílabas"] = df_resultados[
    "classificação por número de sílabas"
].astype(object)

for i in range(len(df_palavras)):
    palavra_loop = df_palavras[i]

    tipo_acentos, quantidade_acentos = extrair_tipo_acento(palavra_loop)
    df_resultados.loc[i, "tipo de acento"] = tipo_acentos
    df_resultados.loc[i, "acento"] = quantidade_acentos


    quantidade_silabas, tipo_palavra = contar_silabas(palavra_loop)
    df_resultados.loc[i, "número de sílabas"] = quantidade_silabas
    df_resultados.loc[i, "classificação por número de sílabas"] = tipo_palavra
    calculo_pesos = calcular_pesos(df_resultados.loc[i, "categoria"], quantidade_silabas, quantidade_acentos)
    df_resultados.loc[i, "peso palavra"] = calculo_pesos

# Separação dos conjuntos de palavras
conjuntos_palavras = ["muito fácil", "fácil", "médio", "difícil", "muito difícil"]
df_resultados["dificuldade"] = pd.qcut(df_resultados["peso palavra"].rank(method="first"), q=5, labels=conjuntos_palavras, duplicates="drop")
df_resultados.to_csv("palavra_completo.csv", mode="w", sep=";", index=False, encoding="utf-8")

print(df_resultados)

print(unicodedata.name("`"))