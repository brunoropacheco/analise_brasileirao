#import urllib.request
#importe as funções BeautifulSoup para analisar os dados retornados do site
#from bs4 import BeautifulSoup
#import requests
import re
### importando bibliotecas
import pandas as pd
import warnings as wa
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
from operator import itemgetter
 
#'season', 'rodada', 'mandante', 'hg', 'visitante', 'ag', 'res', 'vencedor'
                                                                                                                
def getNumberWinner(data, clube ):
    df = data
    filter = df["vencedor"].str.lower() == clube
    return (data[filter]['vencedor'].count()).astype(np.int64)

def getNumberDepartures(data, clube ):
    df = data
    filter1 = df["mandante"].str.lower() == clube
    filter2 = df["visitante"].str.lower() == clube
    return (data[filter1]['mandante'].count() + data[filter2]['visitante'].count()).astype(np.int64)

def getPoints(data, clube ):
    df = data
    filter1 = df["mandante"].str.lower() == clube
    filter2 = df["visitante"].str.lower() == clube
    filter3 = df["vencedor"].str.lower() == clube
    filter4 = (df["mandante"].str.lower() == clube) | (df["visitante"].str.lower() == clube)
    filter5 = df["vencedor"].str.lower() == '_'
    
    v1 = data[(filter1) & (filter3)]
    v1 = v1['vencedor'].count()
    v2 = data[(filter2) & (filter3)]
    v2 = v2['vencedor'].count() 
    v3 = data[(filter4) & (filter5)]
    v3 = v3['vencedor'].count()
    return ((v2*3)+(v1*3)+v3).astype(np.int64)

def getDraw(data, clube ):
    df = data
    filter1 = (df["mandante"].str.lower() == clube) | (df["visitante"].str.lower() == clube)
    filter2 = df["vencedor"].str.lower() == '_'
    df = data[(filter1) & (filter2)]
    empates = df['vencedor'].count()
    return empates.astype(np.int64)

def getDefeats(data, clube ):
    df = data
    filter1 = (df["mandante"].str.lower() == clube) | (df["visitante"].str.lower() == clube)
    filter2 = (df["vencedor"].str.lower() != clube) & (df["vencedor"].str.lower() != '_')
    df = data[(filter1) & (filter2)]
    derrotas = df['vencedor'].count()
    return derrotas.astype(np.int64)

def getGP(data, clube ):
    df = data
    filter1  =  df["mandante"].str.lower() == clube # jogos onde o clube e mandante
    filter2  =  df["visitante"].str.lower() == clube # jogos onde o clube e visitante
    df1      =  data[(filter1)]
    #print(df1)
    df2      =  data[(filter2)]
    #print(df2)
    #placar1  =  [df1['hg'],df1['ag']] #coluna de
    #print(placar1, len(placar1))
    #print(placar1[0][0])
    #placar2  =  [df2['hg'],df2['ag']]
    
    gp       =  0
    gc       =  0
    
    gp = df1['hg'].sum() + df2['ag'].sum()
    gc = df1['ag'].sum() + df2['hg'].sum()
    '''
    for g1, g2 in placar1[0]:
        print(g1, g2)
        gp = (gp + pd.to_numeric( g1 ))
        gc = (gc + pd.to_numeric( g2 ))
            
    for g1, g2 in placar2[0]:
        gp = (gp + pd.to_numeric( g2 )) 
        gc = (gc + pd.to_numeric( g1 ))
    '''
    return gp, gc

def melhor(sea, rod, mand, vis, dados):
    
    if rod == 1:
        return mand
    else:        
        dados_mand = [getPoints(dados, mand), getNumberDepartures(dados, mand), getNumberWinner(dados, mand), getDraw(dados, mand), 
                    getDefeats(dados, mand), getGP(dados, mand)[0], getGP(dados, mand)[1], getGP(dados, mand)[0] - getGP(dados, mand)[1], mand]
        dados_vis = [getPoints(dados, vis), getNumberDepartures(dados, vis), getNumberWinner(dados, vis), getDraw(dados, vis), 
                    getDefeats(dados, vis), getGP(dados, vis)[0], getGP(dados, vis)[1], getGP(dados, vis)[0] - getGP(dados, vis)[1], vis]
        dados_total = [dados_mand, dados_vis]
        dados_total = sorted(dados_total, key=itemgetter(0,1,2,3,4,5))
        #dados_total = sorted(dados_total, key=lambda x: x[0,1,2,3,4,5])
        #return (dados_total[1][8]+' '+str(dados_total[1][0])+' '+str(dados_total[1][2])+ ' x ' +dados_total[0][8]+' '+str(dados_total[0][0])+' '+str(dados_total[0][2]))
        return (dados_total[1][8])

def ajusta_caracteres(coluna):
    coluna = coluna.str.replace('á', 'a')
    coluna = coluna.str.replace('ã', 'a')
    coluna = coluna.str.replace('é', 'e')
    coluna = coluna.str.replace('ê', 'e')
    coluna = coluna.str.replace('í', 'i')
    coluna = coluna.str.replace('ó', 'o')
    coluna = coluna.str.replace('õ', 'o')
    coluna = coluna.str.replace('ú', 'u')
    coluna = coluna.str.lower()
    coluna = coluna.str.replace('-', '_')
    coluna = coluna.str.replace(' ', '_')
    coluna = coluna.str.replace('flamengo_rj', 'flamengo')
    coluna = coluna.str.replace('atletico_pr', 'athletico_pr')
    coluna = coluna.str.replace('sport_recife', 'sport')
    coluna = coluna.str.replace('chapecoense_sc', 'chapecoense')
    return coluna

def ultimo_jogo_vencedor_mandante(row):
    mandante = row['mandante']
    
    ultimos_jogos_mandante = df_jogos_periodo[(df_jogos_periodo['mandante'] == mandante) | (df_jogos_periodo['visitante'] == mandante)]
    ultimos_jogos_mandante_vencedor = ultimos_jogos_mandante[ultimos_jogos_mandante['vencedor'] != '_']
    
    if ultimos_jogos_mandante_vencedor.empty:
        return '_'
    else:
        ultima_vitoria = ultimos_jogos_mandante_vencedor.iloc[-1]
        if ultima_vitoria['mandante'] == mandante:
            return ultima_vitoria['visitante']
        else:
            return ultima_vitoria['mandante']

if __name__ == '__main__':
    ### ignorando warnings do tipo FutureWarning
    wa.simplefilter( action='ignore', category= FutureWarning)
    pd.options.mode.chained_assignment = None

    df_periodo = pd.read_csv('.\periodos.csv', delimiter=";")
    df_jogos   = pd.read_csv('.\jogos2003_2020.csv'  , delimiter=";")
    df_odds   = pd.read_csv('.\BRA.csv'  , delimiter=",")


    df_periodo.columns = df_periodo.columns.str.lower()
    df_jogos.columns   = df_jogos.columns.str.lower()
    df_odds.columns   = df_odds.columns.str.lower()

    df_periodo['inicio' ] = pd.to_datetime(df_periodo['inicio'  ], format="%d/%m/%Y")
    df_periodo['fim'    ] = pd.to_datetime(df_periodo['fim'     ], format="%d/%m/%Y")
    df_jogos['data'     ] = pd.to_datetime(df_jogos['data'      ], format="%d/%m/%Y")
    df_odds['date'      ] = pd.to_datetime(df_odds['date'       ], format="%d/%m/%Y")

    df_periodo['key'] = 1
    df_jogos['key'] = 1

    df_jogos_periodo = pd.merge(df_periodo, df_jogos, on ='key').drop("key", 1)

    df_jogos_periodo = df_jogos_periodo.query('data >= inicio & data <= fim')

    df_jogos_periodo.columns =  df_jogos_periodo.columns.str.replace(' ', '_')
    df_odds.columns = df_odds.columns.str.replace(' ', '_')

    df_jogos_periodo['mandante'] = ajusta_caracteres(df_jogos_periodo['mandante'])
    df_jogos_periodo['visitante'] = ajusta_caracteres(df_jogos_periodo['visitante'])
    df_jogos_periodo['vencedor'] = ajusta_caracteres(df_jogos_periodo['vencedor'])
    df_odds['home'] = ajusta_caracteres(df_odds['home'])
    df_odds['away'] = ajusta_caracteres(df_odds['away'])

    teste = datetime.date(2012,1,1)
    df_jogos_periodo = df_jogos_periodo.query('inicio >= @teste')
    df_odds = df_odds.query('season <= 2020')

    df_odds = df_odds.rename(columns={'date': 'data', 'home': 'mandante', 'away': 'visitante'})

    df_jogos_periodo['season'] = df_jogos_periodo.apply(lambda row: int(row.torneio[3:]), axis = 1)

    #df_jogos_periodo['vencedor_anterior'] = df_jogos_periodo.apply(ultimo_jogo_vencedor_mandante, axis=1)
    
    values = []
    for index, row in df_jogos_periodo.iterrows():
    
        season = row['season']
        rodada = row['rodada']
        mandante = row['mandante']
        
        if rodada == 1:
            values.append("_")    
        else:
            rodada_anterior = rodada - 1
            print(season, rodada, mandante)
            filtro = (df_jogos_periodo['season'] == season) & (df_jogos_periodo['rodada'] == rodada_anterior) & ((df_jogos_periodo['mandante'] == mandante) | (df_jogos_periodo['visitante'] == mandante))
            jogo_anterior = df_jogos_periodo.loc[filtro].iloc[0]
            print(jogo_anterior)            
            if jogo_anterior['vencedor'] == mandante:
                values.append(mandante)
            elif jogo_anterior['vencedor'] == jogo_anterior['visitante']:
                values.append("_")
            else:
                values.append("_")

#adicionando a nova coluna no dataframe
    df_jogos_periodo['vencedor_anterior'] = values
    
    df_jogos_per_odd = pd.merge(df_jogos_periodo, df_odds, on =['season', 'mandante', 'visitante'])
    
    df_j_p_d_res = df_jogos_per_odd.loc[:,['season', 'rodada', 'mandante', 'hg', 'visitante', 'ag', 'vencedor', 'vencedor_anterior', 'ph', 'avgh']]
    
    df_j_p_d_res['melhor'] = df_j_p_d_res.apply(lambda row: melhor(row.season, row.rodada, row.mandante, row.visitante ,
                                                                              df_j_p_d_res.query('season == @row.season & rodada < @row.rodada')), 
                                                         axis = 1)
    
    df_j_p_d_res.to_csv('analisev4.csv')

    #print(df_j_p_d_res.to_string())
    
    #df_j_p_d_res = pd.read_csv('.\\analise.csv', delimiter=",")
    
    
    figure, axis = plt.subplots(9, 1)
    
    temporadas = [2012,2013,2014,2015,2016,2017,2018,2019,2020]
    for temporada in temporadas:
        df_aposta = df_j_p_d_res.query('season == @temporada & mandante == melhor & mandante == vencedor_anterior')
        #print(df_aposta, len(df_aposta))
        #print(df_aposta.to_string())
        df_ganhei = df_aposta.query('vencedor == mandante')
        df_contagem_ganhei = pd.DataFrame
        df_contagem_ganhei = df_ganhei['rodada'].value_counts().to_frame().reset_index()
        #df_contagem_ganhei.columns = ['freq', 'rodada']
        #print(df_contagem_ganhei.columns)
        
        #print(df_ganhei)
        #print(df_ganhei.to_string())
        print(temporada, len(df_aposta), len(df_ganhei), round(df_ganhei['avgh'].sum(),2)) 
        #      'eficiencia: '+str(round(float((df_ganhei['avgh'].sum() - len(df_aposta))/len(df_aposta))*100,2)), 
        #      'acuracia :' +str(round((len(df_ganhei)/len(df_aposta))*100,2)))
        #print(df_contagem_ganhei)
        axis[int(temporadas.index(temporada))].bar(df_contagem_ganhei['index'], df_contagem_ganhei['rodada'])
        #axis[int(temporadas.index(temporada))].set_title('Acertos por Rodada')
        
    plt.show()