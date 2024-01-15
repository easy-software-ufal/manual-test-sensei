from transformation.transformation_data import SMELL_NAMES
from matplotlib import pyplot as plt
import seaborn as sns

if __name__ == '__main__':
    data = dict()
    for smell in SMELL_NAMES:
        with open(smell, 'r') as f:
            values = [float(value) for value in f.read().split('\n') if len(value) > 0]
        data[smell] = values
    sns.violinplot(data=data, fill=False)
    plt.show()