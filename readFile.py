import pandas as pd

def ReadFile(pathToFile):

    file = pd.read_csv(pathToFile)
    file = pd.DataFrame(file)

    return file
    

ReadFile('files/inflationSheet.csv')