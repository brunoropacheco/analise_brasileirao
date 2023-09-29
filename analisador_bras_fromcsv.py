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
import statistics
 
#'season', 'rodada', 'mandante', 'hg', 'visitante', 'ag', 'res', 'vencedor'

if __name__ == '__main__':
    ### ignorando warnings do tipo FutureWarning
    wa.simplefilter( action='ignore', category= FutureWarning)
    pd.options.mode.chained_assignment = None
    
    df_j_p_d_res = pd.read_csv('.\\analisev6.csv', delimiter=",")
    
    
    figure, axis = plt.subplots(9, 1)
    
    temporadas = [2012,2013,2014,2015,2016,2017,2018,2019,2020]
    eficiencias = []
    for temporada in temporadas:
        df_aposta = df_j_p_d_res.query('season == @temporada & mandante == melhor')
        df_ganhei = df_aposta.query('vencedor == mandante')
        df_contagem_ganhei = pd.DataFrame
        df_contagem_ganhei = df_ganhei['rodada'].value_counts().to_frame().reset_index()
        print(temporada, len(df_aposta), len(df_ganhei), round(df_ganhei['avgh'].sum(),2),
              'eficiencia: '+str(round(float((df_ganhei['avgh'].sum() - len(df_aposta))/len(df_aposta))*100,2)), 
              'acuracia :' +str(round((len(df_ganhei)/len(df_aposta))*100,2)))
        eficiencias.append(round((len(df_ganhei)/len(df_aposta))*100,2))
    
    media = statistics.mean(eficiencias)/100
    odd_base = (1/media) + 0.1
    
    print(odd_base)
    
    for temporada in temporadas:
        df_aposta = df_j_p_d_res.query('season == @temporada & mandante == melhor & avgh > @odd_base')
        df_ganhei = df_aposta.query('vencedor == mandante')
        df_contagem_ganhei = pd.DataFrame
        df_contagem_ganhei = df_ganhei['rodada'].value_counts().to_frame().reset_index()
        print(temporada, len(df_aposta), len(df_ganhei), round(df_ganhei['avgh'].sum(),2),
              'eficiencia: '+str(round(float((df_ganhei['avgh'].sum() - len(df_aposta))/len(df_aposta))*100,2)), 
              'acuracia :' +str(round((len(df_ganhei)/len(df_aposta))*100,2)))