from src.open_elec.standarize_data.create_std_dicts import Standard_Dictionaries

def test_create_std_dicts():
    input_folder = "data_csv/seccionales/2023/diccionarios"
    std_dicts = Standard_Dictionaries(input_folder)
    print(std_dicts.df_provincias)
    std_dicts.change_to_std_provincias()