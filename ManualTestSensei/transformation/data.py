import shutil, os
import pandas as pd
from pathlib import Path, PureWindowsPath


def create_copy(filteredDataFrame):
    def update_df_with_copy_location(copied_paths:dict):
        df

    
    path_files = filteredDataFrame["Test file"].unique()
    copied_paths = {}
    for file in path_files:
        path = Path(file)
        breakpoint()
        os.makedirs(os.path.dirname(file[3:]), exist_ok=True)
        new_file_path = shutil.copy(Path("../",file), file[3:] + " - [COPY]")
        copied_paths[path] = Path(new_file_path)

        #df.insert(df.loc[1],"Copy path", new_file_path) INSERT NAO FUNCIONA


#1. adicionar na linha que tenha o valor da coluna Test file igual ao valor file
#2. criar uma coluna vazia e popular ela com os valores do path-cópias
#3. fazer a transformação
#4. profit

def get_filtered_df_by_smell_name(smellName):
    filteredDataFrame = df.loc[df['Smell'] == smellName]
    return filteredDataFrame


def get_csv_path():
    """Searches for .csv files and returns the first one that has 'results' on the name."""
    csvs = sorted(Path('../').glob('*.csv'))
    csvs = [s for s, s in enumerate(csvs) if 'results' in str(s)]
    file = str(csvs[0].resolve())
    return file

if __name__ == "__main__":
    file = get_csv_path()
    df = pd.read_csv(file)
    mprecondition = get_filtered_df_by_smell_name("Misplaced Precondition")

    create_copy(mprecondition)
    # breakpoint()
    # for i in mprecondition.iterrows():
    #     print(i)
