from elecu import *
print("getting current working directory", os.getcwd())
input_folder="data/sav_files/consultas_y_referendums/2024"
output_folder="data/csv_files/consultas_y_referendums/2024"
convert_sav_to_csv(input_folder, output_folder)