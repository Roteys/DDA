import pandas as pd
import pyphen

# Função para contar o número de ACENTOS de cada palavra
def identificar_acentos(palavra_loop):
    acentos = ["á", "à", "â", "ã", "ä", "é", "è", "ê", "ë", "í", "ì", "î", "ï", "ó", "ò", "ô", "õ", "ö", "ú", "ù", "û", "ü", "ç", "Á", "À", "Â", "Ã", "Ä", "É", "È", "Ê", "Ë", "Í", "Ì", "Î", "Ï", "Ó", "Ò", "Ô", "Õ", "Ö", "Ú", "Ù", "Û", "Ü", "Ç"]
    soma = 0
    for caractere in palavra_loop:
        if caractere in acentos:
            soma += 1
    return soma

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
for i in range(len(df_palavras)):
    palavra_loop = df_palavras[i]
    quantidade_acentos = identificar_acentos(palavra_loop)
    df_resultados.loc[i, "acento"] = quantidade_acentos
    quantidade_silabas, tipo_palavra = contar_silabas(palavra_loop)
    df_resultados.loc[i, "número de sílabas"] = quantidade_silabas
    df_resultados.loc[i, "classificação por número de sílabas"] = tipo_palavra
    calculo_pesos = calcular_pesos(df_resultados.loc[i, "categoria"], quantidade_silabas, quantidade_acentos)
    df_resultados.loc[i, "peso palavra"] = calculo_pesos

# Separação dos conjuntos de palavras
conjuntos_palavras = ["muito fácil", "fácil", "médio", "difícil", "muito difícil"]
df_resultados["dificuldade"] = pd.qcut(df_resultados["peso palavra"], q=5, labels=conjuntos_palavras, duplicates="drop")
df_resultados.to_csv("palavra_completo.csv", mode="w", sep=";", index=False, encoding="utf-8")

print(df_resultados)