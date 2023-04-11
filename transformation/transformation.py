import shutil, os

def create_copy(pathFiles):
    
    for file in pathFiles:
        os.makedirs(os.path.dirname(file), exist_ok=True)
        shutil.copyfile("../" + file, file + " transformed")


#from .. import "results-20230411-114932-en_core_web_lg.csv"
import pandas as pd
file = "/home/ullyanne/ubuntu-manual-tests-smells-analysis/testcases/results-20230411-122218-en_core_web_lg.csv"
#f = open(file, "r")
#print(f)
df = pd.read_csv(file)
print(df)

mprecondition = df.loc[df['Smell'] == "Misplaced Precondition"]

pathFiles = mprecondition["Test file"].unique()
create_copy(pathFiles)

breakpoint()
for i in mprecondition.iterrows():
    print(i)
