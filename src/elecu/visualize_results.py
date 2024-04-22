import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
#get the current directory
current_directory = os.path.dirname(os.path.abspath(__file__))
# establishes it as the current directory
os.chdir(current_directory)

def visualize_results_presidentes(df_resultados, bar_plot=False, pie_plot=False):
    """
    Visualiza los resultados de la elección
    
    Parameters
    ----------
    df_resultados : DataFrame
        DataFrame con los resultados de la elección
    bar_plot : bool
        Generar un gráfico de barras
    pie_plot : bool
        Generar un gráfico de pastel
    
    Returns
    -------
    None
    """

    if bar_plot:
        #graficar cada fila
        # si hay sexo, colocar un color diferente
        if 'SEXO' in df_resultados.columns:
            plt.figure(figsize=(10, 6))
            sns.barplot(data=df_resultados, x='CANDIDATO_NOMBRE', y='VOTOS', hue='SEXO')
            plt.title('Votos por Candidato y Sexo')
            plt.xlabel('Candidato')
            plt.ylabel('Votos')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.show()
        else:
            plt.figure(figsize=(10, 6))
            sns.barplot(data=df_resultados, x='CANDIDATO_NOMBRE', y='VOTOS')
            plt.title('Votos por Candidato')
            plt.xlabel('Candidato')
            plt.ylabel('Votos')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.show()
        
              
    if pie_plot:
       # Check if 'SEXO' column exists in the DataFrame
        if 'SEXO' in df_resultados.columns:
            for sexo in df_resultados['SEXO'].unique():
                df_sexo = df_resultados[df_resultados['SEXO'] == sexo]
                plt.figure(figsize=(10, 6))
                plt.pie(df_sexo['VOTOS'], labels=df_sexo['CANDIDATO_NOMBRE'], autopct='%1.1f%%', startangle=140, labeldistance=1.1)
                plt.axis('equal')
                plt.title(f'Votos por Candidato y Sexo: {sexo}')
                plt.show()
            
        else:
            plt.figure(figsize=(10, 6))
            plt.pie(df_resultados['VOTOS'], labels=df_resultados['CANDIDATO_NOMBRE'], autopct='%1.1f%%', startangle=140, labeldistance=1.1)
            plt.axis('equal')
            plt.title('Votos por Candidato')
            plt.show()
        
    return None

