import pandas as pd
from datetime import datetime

# Função para processar e limpar a descrição do serviço
def descricao_servico(df):
    df_temp = []
    for linha in range(len(df)):
        if (df['SITUACAO_OSM'][linha] == "FECHADA") and (df['AVARIA'][linha] != "FUNCIONAMENTO ANORMAL DO EQUIPAMENTO"):
            if len(df['AVARIA'][linha]) >= 100:
                df['AVARIA'][linha] = quebra_linha(df['AVARIA'][linha])
            # Se a condição for atendida, mantém a avaria na lista
            df_temp.append(df['AVARIA'][linha])
        else:
            # Caso contrário, ajusta a descrição do serviço
            descricao = df['DESCR_SERVICO'][linha].replace(",,", ",").replace(f'({df["FORMACAO"][linha]})', '').replace(df["TREM"][linha], "").replace("REPARO DA ANORMALIDADE DO EQUIPAMENTO - ", "")
            if len(descricao) >= 100:
                descricao = quebra_linha(descricao)
            df_temp.append(descricao)
    return df_temp

def quebra_linha(string):
    i = 100
    while i < len(string):
        string = string[:i] + '\n' + string[i:]
        i += 100
    return string

# Função para ajustar o valor na coluna 'GRUPO_SISTEMA' para incluir apenas informações da frota
def frota(df):
    df.loc[df['GRUPO_SISTEMA'].str.contains("TRENS SÉRIE "), 'GRUPO_SISTEMA'] = ""
    return df['GRUPO_SISTEMA']

# Função principal que lê o arquivo Excel, processa os dados e retorna o DataFrame final
def main(df=pd.read_excel("DataBase/BasedeDados.xlsx")):
    # Montagem do novo DataFrame com colunas específicas e dados processados
    model_df = {
        'OSM': df['OSM'].astype(str),
        'FROTA': df['GRUPO_SISTEMA'].str[-4:],  # Extrai os últimos 4 caracteres para representar a frota
        'TREM': df['TREM'],
        'CARRO AVARIADO': df['CARRO_AVARIADO'],
        'SITUAÇÃO OSM': df['SITUACAO_OSM'],
        'DATA E HORA': pd.to_datetime(df['DATAHORA_OSM'], format='%d/%m/%Y %H:%M'),  # Converte para datetime
        'OCORRÊNCIA': df['NR_OCORRENCIA'],
        'SISTEMA': df['SISTEMA'],
        'DESCRIÇÃO DA ABERTURA': descricao_servico(df),  # Usa a função para gerar a coluna 'DESCRIÇÃO DA ABERTURA'
        'DESCRIÇÃO DO FECHAMENTO': df['ATUACAO_COMPLEMENTO']
    }

    # Cria o DataFrame final a partir do dicionário model_df
    model_df = pd.DataFrame(model_df)
    model_df.drop_duplicates(subset='OSM', keep='last', inplace=True)
    return model_df
