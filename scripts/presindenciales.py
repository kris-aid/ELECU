#%%
import elecu.restructure_results
import elecu.extract_values
import elecu.visualize_results
from elecu.extract_values import extract_eleccion, extract_votacion
import pandas as pd
from elecu.restructure_results import Standarized_Results

import os
print(os.getcwd())
#%%
def test_standarized_registro(year=2023):
    input_folder = f"../data/data_csv/generales/{year}"
    standarized_folder = None#"data/Codigos_estandar/"
    standarized_results = Standarized_Results(input_folder, standarized_folder)

    #print(standarized_results.df_registro)
    standarized_results.change_registro()
    #print(standarized_results.df_registro)
    test_registro = standarized_results.put_standar_geo_codes_registro_canton(drop_old=True,year=year)
    if "ELECTORES MENORES A 18" not in test_registro.columns:
        test_registro["ELECTORES MENORES A 18"]=0
    return test_registro


def test_standarized_resultados(year=2023):
    input_folder = f"../data/data_csv/generales/{year}"
    standarized_folder = None #"data/Codigos_estandar/"
    standarized_results = Standarized_Results(input_folder, standarized_folder)
    #print(standarized_results.df_resultados)
    standarized_results.change_resultados()
    #print(standarized_results.df_resultados)
    test = standarized_results.put_standar_geo_codes_results_cantones(drop_old=True,year=year)
    test_year_votacion, test_year_eleccion = standarized_results.divide_resultados()
    return test_year_votacion, test_year_eleccion,test
#%%
from elecu.extract_values import extract_eleccion, extract_votacion

year=2025
test_year_votacion,test_year_eleccion,_=test_standarized_resultados(year)

test_year_votacion_extract=extract_votacion(test_year_votacion,territorio_codigo="EC09",agrupar_por_territorio="CANTON",sexo="AGRUPAR",vuelta="1")


test_year_votacion_EC0901=test_year_votacion[test_year_votacion["CANTON_CODIGO"]=="EC0901"]
test_year_votacion_EC0901=test_year_votacion_EC0901[test_year_votacion_EC0901["VUELTA"]=="1"]
test_year_votacion_EC0901=test_year_votacion_EC0901[test_year_votacion_EC0901["DIGNIDAD_CODIGO"]==1]
test_year_votacion_EC0901.loc["TOTAL"]=test_year_votacion_EC0901.sum()


#%%
year_2023=pd.read_csv("../../data_csv/generales/2023/resultados/resultados_2023_v_1.csv")
#%%
year_2023=year_2023[year_2023["CANTON_CODIGO"]==390.0]
year_2023["DIGNIDAD_CODIGO"]=year_2023["DIGNIDAD_CODIGO"].astype(str)
#%% filter if there is a dignidad_codigo that contains 11

year_2023=year_2023[year_2023["DIGNIDAD_CODIGO"].str.contains("11")]

#duplicated=year_2023[year_2023.duplicated(subset=["PARROQUIA_CODIGO","JUNTA_SEXO"],keep=False)]
year_2023.drop_duplicates(subset=["PARROQUIA_CODIGO","JUNTA_SEXO"],keep="first",inplace=True)
#%%
year_2023.loc["TOTAL"]=year_2023.sum()
#%%
dict_sexo={"MASCULINO":"S0","FEMENINO":"S1"}
year_2023["JUNTA_SEXO"]=year_2023["JUNTA_SEXO"].map(dict_sexo)
#%%
year_2023=year_2023.rename(columns={"JUNTA_SEXO":"SEXO"})
#%%
year_2023.loc["TOTAL"]=year_2023.sum()

#%%
comparative=pd.merge(year_2023[["PARROQUIA_CODIGO","SEXO","BLANCOS","NULOS"]],
                     test_year_votacion_EC0901[["PARROQUIA_CODIGO","SEXO","BLANCOS","NULOS"]],
                     on=["PARROQUIA_CODIGO","SEXO"],how="right",suffixes=("_me","_base"))



#%% put a row of total
comparative.loc["TOTAL"]=comparative.sum()


#%%
def test_extract_eleccion(year=2023,df_resultados=None,vuelta="1",agrupar_por_territorio="PROVINCIA",territorio_codigo="EC01"):

    # test with the 2023 results that are in the test folder
    if df_resultados is None:
        df_resultados = pd.read_csv(f"../../tests/test_results/test_{year}_eleccion.csv")
    # Test 1: extract values for a specific dignidad
    df_resultados_filtered = extract_eleccion(df_resultados, dignidad_codigo=1, territorio_codigo=territorio_codigo,agrupar_por_territorio=agrupar_por_territorio, sexo="AGRUPAR", vuelta=vuelta)
    #print(df_resultados_filtered)
    #print(df_resultados_filtered.columns)
    return df_resultados_filtered

#%%
test_year_eleccion=extract_eleccion(test_year_eleccion,territorio_codigo="EC09",agrupar_por_territorio="CANTON",sexo="AGRUPAR",vuelta="1")






#%%
def extract_presidentes_names_and_votos(year=2023,vuelta="1",territorio="PROVINCIA",territorio_codigo=None,sexo="AGRUPAR"):

    test_registro=test_standarized_registro(year)
    test_year_votacion,test_year_eleccion,_=test_standarized_resultados(year)
    presidentes_year=extract_eleccion(test_year_eleccion,dignidad_codigo=1,territorio_codigo=territorio_codigo,agrupar_por_territorio=territorio,sexo=sexo,vuelta=vuelta)

    #print(presidentes_year.head())
    candidato_nombre_opciones=["CANDIDATO_NOMBRE","CANDIDATO_NOMBRE_RESULTADOS"]
    if "CANDIDATO_CODIGO" in presidentes_year.columns:
        candidatos_path=f"../../data_csv/generales/{year}/organizaciones_politicas/candidatos_{year}.csv"
        candidatos_df=pd.read_csv(candidatos_path)

        for candidato_nombre_opcion in candidato_nombre_opciones:
            if candidato_nombre_opcion in candidatos_df.columns:
                candidato_codigo_nombre=candidatos_df[["CANDIDATO_CODIGO",candidato_nombre_opcion]]
                break
        presidentes_year=pd.merge(presidentes_year,candidato_codigo_nombre,on="CANDIDATO_CODIGO",how="inner")
        presidentes_year=presidentes_year.rename(columns={candidato_nombre_opcion: "CANDIDATO_NOMBRE"})
        presidentes_year.drop(columns=["CANDIDATO_CODIGO"],inplace=True)
    else:
        print("CANDIDATO_NOMBRE already in the dataframe")

    if "OP_CODIGO" in presidentes_year.columns:
        organizaciones_path=f"../../data_csv/generales/{year}/organizaciones_politicas/organizaciones_politicas_{year}.csv"
        organizaciones_df=pd.read_csv(organizaciones_path)
        #organizaciones_df=organizaciones_df.rename(columns={"OP_CODIGO":"OP_CODIGO_ORG"})
        organizaciones_df=organizaciones_df[["OP_CODIGO","OP_NOMBRE"]]
        presidentes_year=pd.merge(presidentes_year,organizaciones_df,on="OP_CODIGO",how="inner")
        presidentes_year.drop(columns=["OP_CODIGO"],inplace=True)

    if territorio== "PROVINCIA":
        provincias_path="data/Codigos_estandar/provincias/std_provincias.csv"
        provincias_df=pd.read_csv(provincias_path)
        provincias_df=provincias_df[["PROVINCIA_CODIGO","PROVINCIA_NOMBRE"]]
        presidentes_year=pd.merge(presidentes_year,provincias_df,on="PROVINCIA_CODIGO",how="inner")
        columns_territorio=["PROVINCIA_CODIGO","PROVINCIA_NOMBRE"]

    if territorio== "CANTON":
        cantones_path="data/Codigos_estandar/cantones/std_cantones.csv"
        cantones_df=pd.read_csv(cantones_path)
        cantones_df=cantones_df[["CANTON_CODIGO","CANTON_NOMBRE"]]
        presidentes_year=pd.merge(presidentes_year,cantones_df,on="CANTON_CODIGO",how="inner")
        columns_territorio=["CANTON_CODIGO","CANTON_NOMBRE"]

    df_presidentes = pd.read_csv("data/Codigos_estandar/dignidades/presidentes_equivalencias.csv")
    input_folder = f"../../data_csv/generales/{year}"
    standarized_folder = "data/Codigos_estandar/"
    standarized_results = Standarized_Results(input_folder, standarized_folder)
    dict = standarized_results.create_dict_mapping(df_presidentes)
    presidentes_year["CANDIDATO_NOMBRE"] = presidentes_year["CANDIDATO_NOMBRE"].map(dict)

    # do a pivot table to get the candidatos as columns
    presidentes_year=presidentes_year.pivot_table(index=columns_territorio,columns="CANDIDATO_NOMBRE",values="VOTOS",aggfunc="sum").reset_index()

    #cast DIGNIDAD_CODIGO to string
    test_year_votacion["DIGNIDAD_CODIGO"]=test_year_votacion["DIGNIDAD_CODIGO"].astype(str)
    test_year_votacion_presidentes=test_year_votacion[test_year_votacion["DIGNIDAD_CODIGO"]=="1"]

    territorio_codigo=columns_territorio[0]
    territorio_nombre=columns_territorio[1]

    test_year_votacion_presidentes=test_year_votacion_presidentes[[territorio_codigo,"SEXO","BLANCOS","NULOS","VUELTA"]]




    test_year_votacion_presidentes=test_year_votacion_presidentes[test_year_votacion_presidentes["VUELTA"]==vuelta]
    columnas_agrupar_votacion = ['SEXO', territorio_codigo]
    if sexo is not None:
        if sexo == 'S0' or sexo == "S1":
            test_year_votacion_presidentes = test_year_votacion_presidentes[test_year_votacion_presidentes['SEXO'] == sexo]
        if sexo == "AMBOS":
            pass
        if sexo == "AGRUPAR":
            # delete the "SEXO" column in columnas_agrupar
            columnas_agrupar_votacion.remove('SEXO')
        test_year_votacion_presidentes = test_year_votacion_presidentes.groupby(columnas_agrupar_votacion).agg({"BLANCOS": "sum", "NULOS": "sum"}).reset_index()


    #test_year_votacion_presidentes=test_year_votacion_presidentes.groupby(territorio_codigo).agg({"BLANCOS":"sum","NULOS":"sum"}).reset_index()
    
    presidentes_year=pd.merge(presidentes_year,test_year_votacion_presidentes[[territorio_codigo,"BLANCOS","NULOS"]],on=territorio_codigo,how="inner")

    columnas_agrupar = ['SEXO',territorio_codigo]
    if sexo is not None:
        if sexo == 'S0' or sexo=="S1":
            test_registro = test_registro[test_registro['SEXO'] == sexo]
        if sexo== "AMBOS":
            pass
        if sexo== "AGRUPAR":
            #delete the "SEXO" column in columnas_agrupar
            columnas_agrupar.remove('SEXO')
        test_registro_year = test_registro.groupby(columnas_agrupar)['TOTAL ELECTORES'].sum().reset_index()


    # columnas_agrupar = [territorio_codigo]
    #
    # test_registro_year=test_registro.groupby(columnas_agrupar)['TOTAL ELECTORES'].sum().reset_index()
    #cast total electores to int
    test_registro_year["TOTAL ELECTORES"]=test_registro_year["TOTAL ELECTORES"].astype(int)
    presidentes_year=pd.merge(presidentes_year,test_registro_year[[territorio_codigo,"TOTAL ELECTORES"]],on=territorio_codigo,how="inner")

    presidentes_year.rename(columns={"TOTAL ELECTORES":"ELECTORES"},inplace=True)
    # add a column with the count of votos validos. That are the sum of the columns since the columns are the votos after territorio_nombre until before blancos and nulos and total electores
    presidentes_year["VOTOS VALIDOS"]=presidentes_year.iloc[:,2:-3].sum(axis=1)

    # put votos validos before blancos and nulos
    columns= presidentes_year.columns.tolist()
    columns=columns[:2]+columns[2:-4]+["VOTOS VALIDOS"]+columns[-4:-1]
    presidentes_year=presidentes_year[columns]
    # add a column with the sufragantes
    presidentes_year["SUFRAGANTES"]=presidentes_year["VOTOS VALIDOS"]+presidentes_year["BLANCOS"]+presidentes_year["NULOS"]

    # df_presidentes = pd.read_csv("data/Codigos_estandar/dignidades/presidentes_equivalencias.csv")
    # input_folder = f"../../data_csv/generales/{year}"
    # standarized_folder = "data/Codigos_estandar/"
    # standarized_results = Standarized_Results(input_folder, standarized_folder)
    # dict = standarized_results.create_dict_mapping(df_presidentes)
    # presidentes_year["CANDIDATO_NOMBRE"] = presidentes_year["CANDIDATO_NOMBRE"].map(dict)

    presidentes_year.drop_duplicates(subset=[territorio_codigo],keep="first",inplace=True)
    return presidentes_year




#%%

#%%
presidentes_votacion=extract_presidentes_names_and_votos(2023,"1",territorio="CANTON",territorio_codigo="EC09",sexo="AGRUPAR")
#%%
#%%
# sexo="S0"
# test_registro=test_standarized_registro(2023)
# columnas_agrupar = ['SEXO', 'PROVINCIA_CODIGO']
# if sexo is not None:
#     if sexo == 'S0' or sexo == "S1":
#         test_registro = test_registro[test_registro['SEXO'] == sexo]
#     if sexo == "AMBOS":
#         pass
#     if sexo == "AGRUPAR":
#         # delete the "SEXO" column in columnas_agrupar
#         columnas_agrupar.remove('SEXO')
#     test_registro_year = test_registro.groupby(columnas_agrupar)['TOTAL ELECTORES'].sum().reset_index()

#%%
presidentes_votacion.head()
#%% retrieve the years on the folder of the data_csv/generales exists
import os
years=os.listdir("../../data_csv/generales")
years=[int(year) for year in years]
years.sort()
provincias_path="data/Codigos_estandar/provincias/std_provincias.csv"
provincias_df=pd.read_csv(provincias_path)
# extract as a dictionary the PROVINCIAS_CODIGO and PROVINCIA_NOMBRE
provincias_dict=provincias_df[["PROVINCIA_CODIGO","PROVINCIA_NOMBRE"]].set_index("PROVINCIA_CODIGO").to_dict()["PROVINCIA_NOMBRE"]
# delete the P00 key and value, and the P25 key and value
del provincias_dict["EC00"]
del provincias_dict["EC25"]


#%%
def apply_suffix(df, sexo):
    columns = df.columns.tolist()
    suffix = "_M" if sexo == "S0" else "_F" if sexo == "S1" else "_T"
    # Retain the first three columns, add suffix to candidate columns, retain last non-candidate columns
    columns = columns[:2] + [col + suffix for col in columns[2:]]
    df.columns = columns
    return df


def merge_presidentes_votes_by_rounds(year, territorio, territorio_codigo):
    combined_dfs = []
    election_rounds = ["1", "2"]

    for vuelta in election_rounds:
        # Skip specified conditions for certain rounds and years
        if vuelta == "2" and (year == 2009 or year == 2013):
            continue
        if year == 2007:
            continue

        # Generate the three dataframes for each round and gender/total
        df_masc = extract_presidentes_names_and_votos(year, vuelta, territorio=territorio,
                                                      territorio_codigo=territorio_codigo, sexo="S0")
        df_fem = extract_presidentes_names_and_votos(year, vuelta, territorio=territorio,
                                                     territorio_codigo=territorio_codigo, sexo="S1")
        df_total = extract_presidentes_names_and_votos(year, vuelta, territorio=territorio,
                                                       territorio_codigo=territorio_codigo, sexo="AGRUPAR")

        # Apply suffixes to each dataframe
        df_masc = apply_suffix(df_masc, "S0")
        df_fem = apply_suffix(df_fem, "S1")
        df_total = apply_suffix(df_total, "AGRUPAR")

        # Merge the dataframes on 'CANTON_CODIGO' and 'CANTON_NOMBRE'
        df_merged = df_masc.merge(df_fem, on=['CANTON_CODIGO', 'CANTON_NOMBRE'], how='outer') \
            .merge(df_total, on=['CANTON_CODIGO', 'CANTON_NOMBRE'], how='outer')

        # Dynamically identify candidate columns
        candidate_columns = df_masc.columns[
                            2:-5]  # Assumes candidate columns are between first two and last five columns
        print(candidate_columns)

        all_candidates = set(
            candidate.replace('_M', '').replace('_F', '').replace('_T', '') for candidate in candidate_columns)

        # Create the ordered list of candidate columns with suffixes
        ordered_candidate_columns = []
        for candidate in sorted(all_candidates):  # Sort for consistency
            if f"{candidate}_F" in df_merged.columns:
                ordered_candidate_columns.append(f"{candidate}_F")
            if f"{candidate}_M" in df_merged.columns:
                ordered_candidate_columns.append(f"{candidate}_M")
            if f"{candidate}_T" in df_merged.columns:
                ordered_candidate_columns.append(f"{candidate}_T")

        # Construct the ordered list of columns
        ordered_columns = ['CANTON_CODIGO', 'CANTON_NOMBRE'] + ordered_candidate_columns + \
                          ['VOTOS VALIDOS_F', 'VOTOS VALIDOS_M', 'VOTOS VALIDOS_T',
                           'BLANCOS_F', 'BLANCOS_M', 'BLANCOS_T',
                           'NULOS_F', 'NULOS_M', 'NULOS_T',
                           'ELECTORES_F', 'ELECTORES_M', 'ELECTORES_T',
                           'SUFRAGANTES_F', 'SUFRAGANTES_M', 'SUFRAGANTES_T']

        # Reorder the dataframe based on the ordered list
        df_merged = df_merged.reindex(columns=[col for col in ordered_columns if col in df_merged.columns])

        # Add `year`, `vuelta`, and `territorio_codigo` as new columns
        df_merged.insert(0, 'ANIO', year)
        df_merged.insert(1, 'VUELTA', vuelta)
        df_merged.insert(2, 'PROVINCIA_CODIGO', territorio_codigo)

        province_name = provincias_dict[territorio_codigo]
        df_merged.insert(3, 'PROVINCIA_NOMBRE', province_name)

        # Append this round's merged dataframe to the list
        combined_dfs.append(df_merged)

    # Concatenate all dataframes for each round into a single dataframe
    final_df = pd.concat(combined_dfs, ignore_index=True)

    return final_df


#%% Example usage
final_df = merge_presidentes_votes_by_rounds(2002, territorio="CANTON", territorio_codigo="EC17")
final_df.head()

#%% now we will iterate over all years and all provinces to generate the dataframes and concatenate them
years = [2002, 2006, 2007]
df_votaciones_total = pd.DataFrame()
for year in years:
    for codigo, provincia in provincias_dict.items():
        print(f"Year: {year}, Provincia: {provincia}")
        df_provincia = merge_presidentes_votes_by_rounds(year, territorio="CANTON", territorio_codigo=codigo)
        df_votaciones_total = pd.concat([df_votaciones_total, df_provincia], ignore_index=True)
#%%
df_votaciones_total_2=df_votaciones_total.copy()
years = [2009, 2013,2017,2021,2023]
for year in years:
    for codigo, provincia in provincias_dict.items():
        print(f"Year: {year}, Provincia: {provincia}")
        df_provincia = merge_presidentes_votes_by_rounds(year, territorio="CANTON", territorio_codigo=codigo)
        df_votaciones_total_2 = pd.concat([df_votaciones_total_2, df_provincia], ignore_index=True)




#%% electores is missing
def add_electores_column(df_votaciones_total_2, year, territorio_codigo, sexo=None):
    test_registro = test_standarized_registro(year)
    columnas_agrupar = ['SEXO', territorio_codigo]
    if sexo is not None:
        if sexo == 'S0' or sexo == "S1":
            test_registro = test_registro[test_registro['SEXO'] == sexo]
        if sexo == "AMBOS":
            pass
        if sexo == "AGRUPAR":
            # delete the "SEXO" column in columnas_agrupar
            columnas_agrupar.remove('SEXO')
        test_registro_year = test_registro.groupby(columnas_agrupar)['TOTAL ELECTORES'].sum().reset_index()

    test_registro_year["TOTAL ELECTORES"] = test_registro_year["TOTAL ELECTORES"].astype(int)
    presidentes_year = pd.merge(presidentes_year, test_registro_year[[territorio_codigo, "TOTAL ELECTORES"]],
                                on=territorio_codigo, how="inner")

    return df_votaciones_total_2
#%%
def add_electores_column_with_suffixes(year, territorio_codigo):
    """
    Adds the 'TOTAL ELECTORES' columns with suffixes (_F, _M, _T) to the main dataframe by year and territory code,
    merging results into a single row per canton.
    """
    # Initialize an empty DataFrame to store results with suffixes
    registro_total = pd.DataFrame()
    test_registro = test_standarized_registro(year)
    suffixes = {"S0": "_M", "S1": "_F", "AGRUPAR": "_T"}


    for sexo, suffix in suffixes.items():
        # Filter test_registro for each sexo or leave unfiltered for AGRUPAR
        test_registro_filtered = test_registro.copy()
        columnas_agrupar = [territorio_codigo]

        if sexo in ["S0", "S1"]:
            test_registro_filtered = test_registro[test_registro['SEXO'] == sexo]
            columnas_agrupar.append('SEXO')
        elif sexo == "AGRUPAR":
            # No filtering on 'SEXO' for "AGRUPAR" (total), don't add 'SEXO' to groupby columns
            test_registro_filtered = test_registro.copy()

        # Group and sum 'TOTAL ELECTORES' by the specified columns
        test_registro_year = test_registro_filtered.groupby(columnas_agrupar)['TOTAL ELECTORES'].sum().reset_index()
        test_registro_year["TOTAL ELECTORES"] = test_registro_year["TOTAL ELECTORES"].astype(int)

        # Apply suffix to 'TOTAL ELECTORES' and territory code columns
        test_registro_year.rename(columns={"TOTAL ELECTORES": f"TOTAL ELECTORES{suffix}"}, inplace=True)

        # Merge each suffixed 'TOTAL ELECTORES' back to registro_total on territorio_codigo
        if registro_total.empty:
            registro_total = test_registro_year  # Initialize with the first result
        else:
            registro_total = pd.merge(registro_total, test_registro_year, on=territorio_codigo, how="outer")

    registro_total.drop(columns=['SEXO_x','SEXO_y'], inplace=True, errors='ignore')
    registro_total["ANIO"] = year
    registro_total.rename(columns={"TOTAL ELECTORES_T": "ELECTORES_T",
                                      "TOTAL ELECTORES_F": "ELECTORES_F",
                                        "TOTAL ELECTORES_M": "ELECTORES_M"
                                   }, inplace=True)
    return registro_total


def add_electores_column_with_suffixes_not_agregated(year, territorio_codigo):
    """
    Adds the 'TOTAL ELECTORES' columns with suffixes (_F, _M, _T) to the main dataframe by year and territory code,
    aggregating results into a single row per canton.
    """
    # Initialize an empty dictionary to store results with suffixes
    results = {}
    test_registro = test_standarized_registro(year)
    suffixes = {"S0": "_M", "S1": "_F", "AGRUPAR": "_T"}

    # Loop through each suffix to calculate totals
    for sexo, suffix in suffixes.items():
        # Copy the dataframe and filter by sexo if needed
        test_registro_filtered = test_registro.copy()
        columnas_agrupar = [territorio_codigo]
        age_group_columns = ['ELECTORES DE 18 A 65', 'ELECTORES MAYORES A 65', 'ELECTORES MENORES A 18']

        if sexo in ["S0", "S1"]:
            test_registro_filtered = test_registro[test_registro['SEXO'] == sexo]
        elif sexo == "AGRUPAR":
            test_registro_filtered = test_registro.copy()

        # Group by territory code and sum all relevant columns
        test_registro_year = test_registro_filtered.groupby(territorio_codigo)[
            age_group_columns + ['TOTAL ELECTORES']].sum().reset_index()

        # Apply suffix to the columns
        for col in age_group_columns:
            test_registro_year.rename(columns={col: f"{col}{suffix}"}, inplace=True)

        test_registro_year.rename(columns={"TOTAL ELECTORES": f"TOTAL ELECTORES{suffix}"}, inplace=True)

        # Set the `territorio_codigo` column as the index to align properly during concatenation
        test_registro_year.set_index(territorio_codigo, inplace=True)

        # Store the suffixed results in the dictionary
        results[suffix] = test_registro_year

    # Combine all suffixed results horizontally (column-wise)
    registro_total = pd.concat(results.values(), axis=1)

    # Reset the index to include the `territorio_codigo` column again
    registro_total.reset_index(inplace=True)

    # Add the year to the resulting dataframe
    registro_total["ANIO"] = year

    # Rename columns for clarity
    registro_total.rename(columns={
        "TOTAL ELECTORES_T": "ELECTORES_T",
        "TOTAL ELECTORES_F": "ELECTORES_F",
        "TOTAL ELECTORES_M": "ELECTORES_M"
    }, inplace=True)

    registro_total.drop(columns=['ELECTORES DE 18 A 65_T', 'ELECTORES MAYORES A 65_T', 'ELECTORES MENORES A 18_T','ELECTORES_T','ELECTORES_F','ELECTORES_M'],inplace=True)

    # put it in int
    columns_to_int = ['ELECTORES DE 18 A 65_F', 'ELECTORES DE 18 A 65_M', 'ELECTORES MAYORES A 65_F', 'ELECTORES MAYORES A 65_M','ELECTORES MENORES A 18_F', 'ELECTORES MENORES A 18_M']

    #registro_total[columns_to_int] = registro_total[columns_to_int].astype(int)
    return registro_total


#%%

test_registro=test_standarized_registro(2017)
#%%
test_add_electores_column_with_suffixes_not_agregated = add_electores_column_with_suffixes_not_agregated(2017, "CANTON_CODIGO")
#%%
test_add_electores_column_with_suffixes= add_electores_column_with_suffixes(2017, "CANTON_CODIGO")

#%%
df_votaciones_total_2 = pd.read_csv("../../tests/Presidenciales/presidentes_votacion_cantonal_complete.csv")

#%%
# Example usage to add TOTAL ELECTORES columns with suffixes to df_votaciones_total_2
years = [2002, 2006,2009, 2013, 2017, 2021, 2023]
test_total_electores =pd.DataFrame()
for year in years:
    print(f"Year: {year}")
    test_total_electores = pd.concat([test_total_electores, add_electores_column_with_suffixes_not_agregated(year, "CANTON_CODIGO")], ignore_index=True)

#%%
df_test_join = pd.merge(df_votaciones_total_2, test_total_electores, on=["ANIO", "CANTON_CODIGO"], how="inner")


#%%
ordered_columns = ['ANIO', 'VUELTA', 'PROVINCIA_CODIGO', 'PROVINCIA_NOMBRE', 'CANTON_CODIGO', 'CANTON_NOMBRE'] + \
                    [col for col in df_test_join.columns if col not in
                        ['ANIO', 'VUELTA', 'PROVINCIA_CODIGO', 'PROVINCIA_NOMBRE', 'CANTON_CODIGO', 'CANTON_NOMBRE','VOTOS VALIDOS_F', 'VOTOS VALIDOS_M', 'VOTOS VALIDOS_T',
                           'BLANCOS_F', 'BLANCOS_M', 'BLANCOS_T',
                           'NULOS_F', 'NULOS_M', 'NULOS_T','ELECTORES MENORES A 18_F', 'ELECTORES DE 18 A 65_F', 'ELECTORES MAYORES A 65_F',
                            'ELECTORES MENORES A 18_M', 'ELECTORES DE 18 A 65_M', 'ELECTORES MAYORES A 65_M',
                           'ELECTORES_F', 'ELECTORES_M', 'ELECTORES_T',

                           'SUFRAGANTES_F', 'SUFRAGANTES_M', 'SUFRAGANTES_T']]+\
                    ['VOTOS VALIDOS_F', 'VOTOS VALIDOS_M', 'VOTOS VALIDOS_T',
                            'BLANCOS_F', 'BLANCOS_M', 'BLANCOS_T',
                            'NULOS_F', 'NULOS_M', 'NULOS_T',
                            'ELECTORES MENORES A 18_F', 'ELECTORES DE 18 A 65_F', 'ELECTORES MAYORES A 65_F','ELECTORES_F',
                            'ELECTORES MENORES A 18_M', 'ELECTORES DE 18 A 65_M', 'ELECTORES MAYORES A 65_M',
                             'ELECTORES_M', 'ELECTORES_T',
                            'SUFRAGANTES_F', 'SUFRAGANTES_M', 'SUFRAGANTES_T']


#%%
df_votaciones_final=df_test_join[ordered_columns]

#%% sort it
df_votaciones_final.sort_values(by=["ANIO","VUELTA","PROVINCIA_CODIGO","CANTON_CODIGO","VUELTA"],inplace=True)

#%%
df_votaciones_final.fillna(0,inplace=True)

#%% put as int all the columns that are not the first 6
df_votaciones_final.iloc[:,6:]=df_votaciones_final.iloc[:,6:].astype(int)
# it doesnt changed fixed the issue

columns_to_int=[
                    [col for col in df_votaciones_total_2.columns if col not in
                        ['ANIO', 'VUELTA', 'PROVINCIA_CODIGO', 'PROVINCIA_NOMBRE', 'CANTON_CODIGO', 'CANTON_NOMBRE','VOTOS VALIDOS_F', 'VOTOS VALIDOS_M', 'VOTOS VALIDOS_T',
                           'BLANCOS_F', 'BLANCOS_M', 'BLANCOS_T',
                           'NULOS_F', 'NULOS_M', 'NULOS_T',
                           'ELECTORES_F', 'ELECTORES_M', 'ELECTORES_T',
                           'SUFRAGANTES_F', 'SUFRAGANTES_M', 'SUFRAGANTES_T']]+\
                    ['VOTOS VALIDOS_F', 'VOTOS VALIDOS_M', 'VOTOS VALIDOS_T',
                            'BLANCOS_F', 'BLANCOS_M', 'BLANCOS_T',
                            'NULOS_F', 'NULOS_M', 'NULOS_T',
'ELECTORES MENORES A 18_F', 'ELECTORES DE 18 A 65_F', 'ELECTORES MAYORES A 65_F',
                            'ELECTORES MENORES A 18_M', 'ELECTORES DE 18 A 65_M', 'ELECTORES MAYORES A 65_M',
                            'ELECTORES_F', 'ELECTORES_M', 'ELECTORES_T',
                            'SUFRAGANTES_F', 'SUFRAGANTES_M', 'SUFRAGANTES_T']]

for column in columns_to_int:
    df_votaciones_final[column]=df_votaciones_final[column].astype(int)

#%%
df_votaciones_final.rename(columns={"ELECTORES_F":"ELECTORES_F_T","ELECTORES_M":"ELECTORES_M_T"},inplace=True)
#%%
df_votaciones_final.to_csv("../../tests/Presidenciales/presidentes_votacion_cantonal_complete_with_electores_F_M.csv",index=False)
#%%
years=[2013,2017]
vuelta="2"
sexo="S1"
for year in years :
    if vuelta=="2" and (year==2009 or year==2013):
        continue
    if year==2007:
        continue
    print(f"Year: {year}")
    #if in the path tests/Presidenciales/ not exist the folder for the year, create it, if it exists, the folder is not created
    if not os.path.exists(f"../../tests/Presidenciales/{year}"):
        os.makedirs(f"../../tests/Presidenciales/{year}")
    else:
        print(f"Folder for the year {year} already exists")


    # if im the path tests/Presidenciales/year not exist the folder for the vuelta, create it, if it exists, the folder is not created
    if not os.path.exists(f"../../tests/Presidenciales/{year}/{vuelta}_vuelta"):
        os.makedirs(f"../../tests/Presidenciales/{year}/{vuelta}_vuelta")
    else:
        print(f"Folder for the vuelta {vuelta} already exists")


    for codigo,provincia in provincias_dict.items():
        print(f"Provincia: {provincia}")
        presidentes_votacion=extract_presidentes_names_and_votos(year,vuelta,territorio="CANTON",territorio_codigo=codigo,sexo=sexo)
        presidentes_votacion["PROVINCIA_NOMBRE"]=provincia
        presidentes_votacion["PROVINCIA_CODIGO"]=codigo
        # put provincia_codigo and provincia_nombre as the first columns
        columns= presidentes_votacion.columns.tolist()
        columns=columns[-2:]+columns[:-2]
        presidentes_votacion=presidentes_votacion[columns]
        presidentes_votacion["SEXO"]=sexo
        if sexo=="S0":
            # add a M at the end of the columns after the CANTON_NOMBRE
            columns= presidentes_votacion.columns.tolist()
            columns=columns[:3]+[column+"_M" for column in columns[3:]]
        if sexo=="S1":
            # add a F at the end of the columns after the CANTON_NOMBRE
            columns= presidentes_votacion.columns.tolist()
            columns=columns[:3]+[column+"_F" for column in columns[3:]]
        if sexo=="AMBOS":
            # add a T at the end of the columns after the CANTON_NOMBRE
            columns= presidentes_votacion.columns.tolist()
            columns=columns[:3]+[column+"_T" for column in columns[3:]]

        presidentes_votacion.columns=columns



        #print(columns)
        presidentes_votacion.to_csv(f"../../tests/Presidenciales/{year}/{vuelta}_vuelta/presidentes_votacion_cantonal_{provincia}_{year}_{vuelta}.csv",index=False)

#%%
vuelta="2"
for year in years :
    if vuelta=="2" and (year==2009 or year==2013):
        continue
    if year==2007:
        continue
    print(f"Year: {year}")
    #if in the path tests/Presidenciales/ not exist the folder for the year, create it, if it exists, the folder is not created
    if not os.path.exists(f"../../tests/Presidenciales/{year}"):
        os.makedirs(f"../../tests/Presidenciales/{year}")
    else:
        print(f"Folder for the year {year} already exists")


    # if im the path tests/Presidenciales/year not exist the folder for the vuelta, create it, if it exists, the folder is not created
    if not os.path.exists(f"../../tests/Presidenciales/{year}/{vuelta}_vuelta"):
        os.makedirs(f"../../tests/Presidenciales/{year}/{vuelta}_vuelta")
    else:
        print(f"Folder for the vuelta {vuelta} already exists")


    presidentes_votacion=extract_presidentes_names_and_votos(year,vuelta,territorio="PROVINCIA",territorio_codigo=None)
    presidentes_votacion.to_csv(f"../../tests/Presidenciales/{year}/{vuelta}_vuelta/presidentes_votacion_provincial_{year}_{vuelta}.csv",index=False)
#%%
anio=2002
vuelta=1
columna="_T"
votacion=df_votaciones_total_2[(df_votaciones_total_2["ANIO"]==anio) & (df_votaciones_total_2["VUELTA"]==vuelta)]

#%%
candidatos_presidenciales={
    2002: ["RODRIGO BORJA","JACINTO VELAZQUEZ","ANTONIO VARGAS","OSVALDO HURTADO",
           "ALVARO NOBOA","XAVIER NEIRA","CESAR ALARCON","IVONNE BAKI","JACOBO BUCARAM","LUCIO GUTIERREZ"],
    2006: ["JAIME DEMERVAL","RAFAEL CORREA","ALVARO NOBOA","GILMAR GUTIERREZ","LEON ROLDOS","LUIS VILLACIS",
           "LUIS MACAS","LENIN TORRES","MARCO PROANO","MARCELO LARREA","CYNTHIA VITERI","CARLOS SAGNAY","FERNANDO ROSERO"],
    2009: ["RAFAEL CORREA","LUCIO GUTIERREZ","ALVARO NOBOA","MARTHA ROLDOS","MELBA JACOME",
    "CARLOS GONZALEZ","DIEGO DELGADO JARA","CARLOS SAGNAY"],
    2013: ["RAFAEL CORREA","GUILLERMO LASSO","ALBERTO ACOSTA","MAURICIO RODAS","LUCIO GUTIERREZ",
    "ALVARO NOBOA","NORMAN WRAY","NELSON ZAVALA"],
    2017: ["PATRICIO ZUQUILANDA","IVAN ESPINEL","CYNTHIA VITERI","JAIME BUCARAM",
           "PACO MONCAYO","WASHINGTON PESANTEZ","GUILLERMO LASSO","LENIN MORENO"],
    2021: ["ANDRES ARAUZ","LUCIO GUTIERREZ","GERSON ALMEIDA","ISIDRO ROMERO","CARLOS SAGNAY",
            "XAVIER HERVAS","PEDRO FREILE","CESAR MONTUFAR","YAKU PEREZ","GIOVANNY ANDRADE","GUSTAVO LARREA",
            "GUILLERMO LASSO","GUILLERMO CELI","JUAN FERNANDO VELASCO","PAUL CARRASCO","XIMENA PENA"],
    2023: ["YAKU PEREZ","DANIEL NOBOA","LUISA GONZALEZ","JAN TOPIC","OTTO SONNENHOLZNER","BOLIVAR ARMIJOS","FERNANDO VILLAVICENCIO",
            "XAVIER HERVAS"]

}
#%%
import pandas as pd

# Sample dataset structure
columns = [
    'ANIO', 'VUELTA', 'PROVINCIA_CODIGO', 'PROVINCIA_NOMBRE', 'CANTON_CODIGO', 'CANTON_NOMBRE',
    'VOTOS VALIDOS_F', 'VOTOS VALIDOS_M', 'VOTOS VALIDOS_T',
    'BLANCOS_F', 'BLANCOS_M', 'BLANCOS_T',
    'NULOS_F', 'NULOS_M', 'NULOS_T',
    'SUFRAGANTES_F', 'SUFRAGANTES_M', 'SUFRAGANTES_T',
    'ELECTORES MENORES A 18_F', 'ELECTORES DE 18 A 65_F', 'ELECTORES MAYORES A 65_F',
    'ELECTORES MENORES A 18_M', 'ELECTORES DE 18 A 65_M', 'ELECTORES MAYORES A 65_M',
    'ELECTORES_F_T', 'ELECTORES_M_T', 'ELECTORES_T'
]

# Dummy data to match columns
data_path="tests/Presidenciales/presidentes_votacion_cantonal_complete_with_electores_F_M.csv"

df = pd.read_csv(data_path)
#%%
# df=df[df["ANIO"]==2023]
# df=df[df["VUELTA"]==1]
# df=df[df["CANTON_CODIGO"]=="EC0101"]
#%%
# Candidate dictionary
candidatos_presidenciales={
    2002: ["RODRIGO BORJA","JACINTO VELAZQUEZ","ANTONIO VARGAS","OSVALDO HURTADO",
           "ALVARO NOBOA","XAVIER NEIRA","CESAR ALARCON","IVONNE BAKI","JACOBO BUCARAM","LUCIO GUTIERREZ"],
    2006: ["JAIME DEMERVAL","RAFAEL CORREA","ALVARO NOBOA","GILMAR GUTIERREZ","LEON ROLDOS","LUIS VILLACIS",
           "LUIS MACAS","LENIN TORRES","MARCO PROANO","MARCELO LARREA","CYNTHIA VITERI","CARLOS SAGNAY","FERNANDO ROSERO"],
    2009: ["RAFAEL CORREA","LUCIO GUTIERREZ","ALVARO NOBOA","MARTHA ROLDOS","MELBA JACOME",
    "CARLOS GONZALEZ","DIEGO DELGADO JARA","CARLOS SAGNAY"],
    2013: ["RAFAEL CORREA","GUILLERMO LASSO","ALBERTO ACOSTA","MAURICIO RODAS","LUCIO GUTIERREZ",
    "ALVARO NOBOA","NORMAN WRAY","NELSON ZAVALA"],
    2017: ["PATRICIO ZUQUILANDA","IVAN ESPINEL","CYNTHIA VITERI","JAIME BUCARAM",
           "PACO MONCAYO","WASHINGTON PESANTEZ","GUILLERMO LASSO","LENIN MORENO"],
    2021: ["ANDRES ARAUZ","LUCIO GUTIERREZ","GERSON ALMEIDA","ISIDRO ROMERO","CARLOS SAGNAY",
            "XAVIER HERVAS","PEDRO FREILE","CESAR MONTUFAR","YAKU PEREZ","GIOVANNY ANDRADE","GUSTAVO LARREA",
            "GUILLERMO LASSO","GUILLERMO CELI","JUAN FERNANDO VELASCO","PAUL CARRASCO","XIMENA PENA"],
    2023: ["YAKU PEREZ","DANIEL NOBOA","LUISA GONZALEZ","JAN TOPIC","OTTO SONNENHOLZNER","BOLIVAR ARMIJOS","FERNANDO VILLAVICENCIO",
            "XAVIER HERVAS"]

}
#%% Function to process votes dynamically
# Function to process votes dynamically for each ANIO and VUELTA
def process_votes(df, candidates, year):
    # Filter for relevant columns: candidates + blancos + nulos
    relevant_columns = [
        col for col in df.columns
        if any(candidate in col for candidate in candidates) or "BLANCOS" in col or "NULOS" in col
    ]

    # Melt dataframe to long format
    df_votes = df.melt(
        id_vars=['ANIO', 'VUELTA', 'PROVINCIA_CODIGO', 'PROVINCIA_NOMBRE', 'CANTON_CODIGO', 'CANTON_NOMBRE'],
        value_vars=relevant_columns,
        var_name='CANDIDATE_GROUP',
        value_name='VOTE_COUNT'
    )

    # Extract candidate names and groupings
    def extract_candidate_info(row):
        # Split the group name (e.g., "YAKU_PEREZ_F")
        parts = row['CANDIDATE_GROUP'].rsplit('_', 1)
        if len(parts) == 2:
            return pd.Series({'CANDIDATO_NOMBRE': parts[0], 'AGRUPACION': parts[1]})
        return pd.Series({'CANDIDATO_NOMBRE': row['CANDIDATE_GROUP'], 'AGRUPACION': None})

    # Apply the extraction logic
    candidate_info = df_votes.apply(extract_candidate_info, axis=1)
    df_votes = pd.concat([df_votes, candidate_info], axis=1)

    # Filter candidates based on the year
    valid_candidates = candidates + ["BLANCOS", "NULOS"]
    df_votes = df_votes[df_votes['CANDIDATO_NOMBRE'].isin(valid_candidates)]

    # Clean up and return
    df_votes_final = df_votes[
        ['ANIO', 'VUELTA', 'PROVINCIA_CODIGO', 'PROVINCIA_NOMBRE', 'CANTON_CODIGO', 'CANTON_NOMBRE',
         'CANDIDATO_NOMBRE', 'AGRUPACION', 'VOTE_COUNT']
    ].reset_index(drop=True)

    return df_votes_final

# Process dynamically for each year in the dictionary
df_processed = pd.DataFrame()
for year, candidates in candidatos_presidenciales.items():
    if year in df['ANIO'].unique():
        # Filter data for the given year
        df_year = df[df['ANIO'] == year]

        # Process each vuelta within the year
        for vuelta in df_year['VUELTA'].unique():
            df_vuelta = df_year[df_year['VUELTA'] == vuelta]
            df_vuelta_processed = process_votes(df_vuelta, candidates, year)
            df_processed = pd.concat([df_processed, df_vuelta_processed])

# Reset index for the final dataframe
df_processed = df_processed.reset_index(drop=True)

# Display Results
print("Processed Votes DataFrame:")
print(df_processed)
#%% if vote count is 0 and vuelta is 2, remove the row
df_processed=df_processed[~((df_processed["VOTE_COUNT"]==0) & (df_processed["VUELTA"]==2))]
#%% sort by year, vuelta, provincia_codigo, canton_codigo,candidato_nombre
df_sorted=df_processed.sort_values(by=["ANIO","VUELTA","PROVINCIA_CODIGO","CANTON_CODIGO","CANDIDATO_NOMBRE"])


#%% just look df in 2002 vuelta 1 cuenca
df_2002_vuelta_1_cuenca=df[(df["ANIO"]==2021) & (df["VUELTA"]==1) & (df["CANTON_NOMBRE"]=="CUENCA")]
#%%
df_2002_vuelta_1_cuenca_sorted=df_sorted[(df_sorted["ANIO"]==2021) & (df_sorted["VUELTA"]==1) & (df_sorted["CANTON_NOMBRE"]=="CUENCA")]
#%% Function to process electors and sufragantes dynamically
# Function to process electors and sufragantes dynamically
def process_electors_and_sufragantes(df, year):
    # Identify elector and sufragantes columns
    elector_columns = [col for col in df.columns if "ELECTORES" in col]
    sufragantes_columns = [col for col in df.columns if "SUFRAGANTES" in col]

    # Process electors (only once per ANIO and CANTON_CODIGO)
    df_electors = df.drop_duplicates(subset=['ANIO', 'CANTON_CODIGO'])[  # Avoid duplicates
        ['ANIO', 'PROVINCIA_CODIGO', 'PROVINCIA_NOMBRE', 'CANTON_CODIGO', 'CANTON_NOMBRE'] + elector_columns
    ]
    df_electors_long = df_electors.melt(
        id_vars=['ANIO', 'PROVINCIA_CODIGO', 'PROVINCIA_NOMBRE', 'CANTON_CODIGO', 'CANTON_NOMBRE'],
        value_vars=elector_columns,
        var_name='GROUP_TYPE',
        value_name='COUNT'
    )
    df_electors_long['GROUP'] = 'ELECTORES'
    df_electors_long['GROUP_DETAIL'] = df_electors_long['GROUP_TYPE'].str.replace('ELECTORES_', '').replace('_', ' ')

    # Process sufragantes (changes per VUELTA)
    df_sufragantes = df[
        ['ANIO', 'VUELTA', 'PROVINCIA_CODIGO', 'PROVINCIA_NOMBRE', 'CANTON_CODIGO', 'CANTON_NOMBRE'] + sufragantes_columns
    ]
    df_sufragantes_long = df_sufragantes.melt(
        id_vars=['ANIO', 'VUELTA', 'PROVINCIA_CODIGO', 'PROVINCIA_NOMBRE', 'CANTON_CODIGO', 'CANTON_NOMBRE'],
        value_vars=sufragantes_columns,
        var_name='GROUP_TYPE',
        value_name='COUNT'
    )
    df_sufragantes_long['GROUP'] = 'SUFRAGANTES'
    df_sufragantes_long['GROUP_DETAIL'] = df_sufragantes_long['GROUP_TYPE'].str.replace('SUFRAGANTES_', '')

    # Combine electors and sufragantes
    df_combined = pd.concat([df_electors_long, df_sufragantes_long], ignore_index=True)

    # Final cleanup
    df_combined = df_combined[
        ['ANIO', 'VUELTA', 'PROVINCIA_CODIGO', 'PROVINCIA_NOMBRE', 'CANTON_CODIGO', 'CANTON_NOMBRE',
         'GROUP', 'GROUP_DETAIL', 'COUNT']
    ].reset_index(drop=True)

    return df_combined

# Process dynamically for each year in the dataframe
df_electors_sufragantes_processed = pd.DataFrame()
for year in df['ANIO'].unique():
    # Filter data for the given year
    df_year = df[df['ANIO'] == year]

    # Process the year data
    df_year_processed = process_electors_and_sufragantes(df_year, year)
    df_electors_sufragantes_processed = pd.concat([df_electors_sufragantes_processed, df_year_processed])

# Reset index for the final dataframe
df_electors_sufragantes_processed = df_electors_sufragantes_processed.reset_index(drop=True)

# Display Results
print("Processed Electors and Sufragantes DataFrame:")
print(df_electors_sufragantes_processed)
#%%
df_electors_sufragantes_processed["VUELTA"].fillna(1,inplace=True)
#%% put vuelta as int
df_electors_sufragantes_processed["VUELTA"]=df_electors_sufragantes_processed["VUELTA"].astype(int)
#%% in group detail, quit the ELECTORES word
df_electors_sufragantes_processed["GROUP_DETAIL"]=df_electors_sufragantes_processed["GROUP_DETAIL"].str.replace("ELECTORES ","")
#%% sort
df_electors_sufragantes_processed.sort_values(by=["ANIO","VUELTA","PROVINCIA_CODIGO","CANTON_CODIGO","GROUP"],inplace=True)
#%%
df_electors_sufragantes_processed.rename(columns={"GROUP_DETAIL":"AGRUPACION","GROUP":"CATEGORIA","COUNT":"CANTIDAD"},inplace=True)
#%%
df_electors_sufragantes_processed.to_csv("tests/Presidenciales/presidentes_electores_sufragantes_cantonal_formato_corto.csv",index=False)
#%%
df_sorted.rename(columns={"VOTE_COUNT":"VOTOS"},inplace=True)
#%%
df_sorted.to_csv("tests/Presidenciales/presidentes_votacion_cantonal_formato_corto.csv",index=False)