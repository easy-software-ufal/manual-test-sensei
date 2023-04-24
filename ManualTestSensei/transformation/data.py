import shutil, os
import pandas as pd
from pathlib import Path, PureWindowsPath
import logging
log = logging.getLogger(__name__)
from transformation import SMELL_NAMES

def create_copy(df:pd.DataFrame, filteredDataFrame):
    def update_df_with_copy_location(df:pd.DataFrame,copied_paths:dict) -> pd.DataFrame:
        df['Copy Path'] = df['Test file'].map(copied_paths, 'ignore')
        # breakpoint()
        return df

    path_files = filteredDataFrame['Test file'].unique()
    copied_paths = {}
    for file in path_files:
        path = Path(file)
        # breakpoint()
        os.makedirs(os.path.dirname(file[3:]), exist_ok=True)
        new_file_path = shutil.copy(Path('../',file), file[3:] + ' - [COPY]')
        copied_paths[file] = Path(new_file_path)

    return update_df_with_copy_location(df, copied_paths)


#1. adicionar na linha que tenha o valor da coluna Test file igual ao valor file
#2. criar uma coluna vazia e popular ela com os valores do path-cópias
#3. fazer a transformação
#4. profit

def get_filtered_df_by_smell_name(df, smellName):
    filteredDataFrame = df.loc[df['Smell'] == smellName]
    return filteredDataFrame


def get_csv_path():
    '''Searches for .csv files and returns the first one that has 'results' on the name.'''
    csvs = sorted(Path('../').glob('*.csv'))
    csvs = [s for s, s in enumerate(csvs) if 'results' in str(s)]
    file = str(csvs[0].resolve())
    return file


def data_closure():
    def create_copy_from_smell_name(df, smell_name) -> pd.DataFrame:
        filtered_df = get_filtered_df_by_smell_name(df, smell_name)
        df = create_copy(df, filtered_df)
        return df

    log.debug('Searching CSV')
    file = get_csv_path()
    df = pd.read_csv(file)
    log.debug('CSV found')
    for smell_name in SMELL_NAMES:
        df = create_copy_from_smell_name(df, smell_name)
        breakpoint()

    # breakpoint()
    #maybe this gets troubled about the DF. check the DF.


if __name__ == '__main__':
    file = get_csv_path()
    df = pd.read_csv(file)
    log.info('CSV found')
    mprecondition = get_filtered_df_by_smell_name(df,'Misplaced Precondition')

    create_copy(df, mprecondition)
    # breakpoint()
    # for i in mprecondition.iterrows():
    #     print(i)
    breakpoint()
