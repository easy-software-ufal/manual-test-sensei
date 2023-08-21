import sys
import shutil, os
import pandas as pd
from pathlib import Path, PureWindowsPath
import logging

#SMELL_NAMES = ['Conditional Test Logic', 'Eager Action', 'Misplaced Action',
       #'Ambiguous Test', 'Unverified Action', 'Misplaced Verification',
       #'Misplaced Precondition']

SMELL_NAMES = ['Ambiguous Test']

def create_copy(df:pd.DataFrame, filteredDataFrame):
    def update_df_with_copy_location(df:pd.DataFrame,copied_paths:dict) -> pd.DataFrame:
        df_zero = df
        #breakpoint()
        try:
            df['Test file'] = df['Test file'].str.replace(r'\\', '/', regex=True)
            df['Copy Path'] = df['Test file'].map(copied_paths, 'ignore')
        except:
            df['Copy Path'] = df['Test file'].map(copied_paths, 'ignore')
        return df

    path_files = filteredDataFrame['Test file'].unique()
    copied_paths = {}
    for file in path_files:
        path = Path(file)
        if __name__ == 'main': #rodando dentro da pasta transforamtio
            os.makedirs(os.path.dirname(file[3:]), exist_ok=True)
            new_file_path = shutil.copy(Path('../',file), file[3:] + ' - [COPY]')
        else:
            if sys.platform.startswith('linux'):
                file = file.replace('\\', '/')
                os.makedirs(os.path.dirname(Path('transformation//transformed_testcases//',file[3:])), exist_ok=True)
                new_file_path = shutil.copy(src=file, dst='transformation/transformed_testcases/' + file[3:] + ' - [COPY]')
            else:
                os.makedirs(os.path.dirname(Path('transformed_testcases\\',file[3:])), exist_ok=True)
                # breakpoint()
                new_file_path = shutil.copy(src=Path('..',file), dst=(Path('.\\transformed_testcases',file[3:] + ' - [COPY]')))
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
    try:
        csvs = sorted(Path('../').glob('*.csv'))
        # breakpoint()
        csvs = [s for s, s in enumerate(csvs) if 'results' in str(s)][-1:]
        file = str(csvs[0].resolve())
    except IndexError:
        csvs = sorted(Path('.').glob('*.csv'))
        csvs = [s for s, s in enumerate(csvs) if 'results' in str(s)][-1:]
        file = str(csvs[0].resolve())
    return file


def data_closure() -> pd.DataFrame:
    log = logging.getLogger(__name__)
    def create_copy_from_smell_name(df, smell_name) -> pd.DataFrame:
        filtered_df = get_filtered_df_by_smell_name(df, smell_name)
        df = create_copy(df, filtered_df)
        return df
    def remove_duplicates(df):
        return df.drop_duplicates(subset=['Test file', 'Smell', 'Sentence' ], keep='first')
    def remove_NaN_values(df):
        index_to_drop = df.loc[~df['Sentence'].apply(lambda x: isinstance(x, str))].index
        return df.drop(index_to_drop)

    log.info('Searching CSV')
    file = get_csv_path()
    df = pd.read_csv(file)
    log.info(f'CSV found: {file}')
    for smell_name in SMELL_NAMES:
        df = create_copy_from_smell_name(df, smell_name)
    df = remove_duplicates(df)
    df = remove_NaN_values(df)
    log.info('CSV Data loaded.')
    return df


# if __name__ == '__main__':
#     file = get_csv_path()
#     df = pd.read_csv(file)
#     mprecondition = get_filtered_df_by_smell_name(df,'Misplaced Precondition')

#     create_copy(df, mprecondition)
#     breakpoint()
