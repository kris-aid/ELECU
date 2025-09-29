from elecu import *

input_folder = "data/csv_files/generales/2025"
std_dicts = Standard_Dictionaries(input_folder)
print(std_dicts.df_dignidades)
std_dicts.change_to_std_dignidades()
print(std_dicts.df_dignidades)

print(std_dicts.df_provincias)
std_dicts.change_to_std_provincias()
print(std_dicts.df_provincias)
print(std_dicts.df_cantones)
std_dicts.change_to_std_cantones()
print(std_dicts.df_cantones)
print(std_dicts.df_parroquias)
std_dicts.change_to_std_parroquias()
print(std_dicts.df_parroquias)