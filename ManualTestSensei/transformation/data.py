import shutil, os
import pandas as pd
from pathlib import Path, PureWindowsPath


def create_copy(filteredDataFrame):
    pathFiles = filteredDataFrame["Test file"].unique()
    for file in pathFiles:
        path = Path(file)
        os.makedirs(os.path.dirname(file[3:]), exist_ok=True)
        # breakpoint()
        new_file_path = shutil.copy(Path("../",file), file[3:] + " - [COPY]")
        #df.insert(df.loc[1],"Copy path", new_file_path) INSERT NAO FUNCIONA


#1. adicionar na linha que tenha o valor da coluna Test file igual ao valor file
#2. criar uma coluna vazia e popular ela com os valores do path-cópias
#3. fazer a transformação
#4. profit

def getFilteredDataframe(smellName):
    filteredDataFrame = df.loc[df['Smell'] == smellName]
    return filteredDataFrame

def refactorMisplacedPrecondition(testRow):
    #acessa o arquivo
    #encontra o erro
    #resolve o erro
    pass


def get_csv_path():
    csvs = sorted(Path('../').glob('*.csv'))
    csvs = [s for s, s in enumerate(csvs) if 'results' in str(s)]
    file = str(csvs[0].resolve())
    return file

if __name__ == "__main__":
    file = get_csv_path()
    df = pd.read_csv(file)
    mprecondition = getFilteredDataframe("Misplaced Precondition")

    create_copy(mprecondition)
    # breakpoint()
    # for i in mprecondition.iterrows():
    #     print(i)
