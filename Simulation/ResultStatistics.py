import pandas as pd



data = pd.read_csv('Results/MasterDataSet_Old.csv')

print data.describe().iloc[[1,2,3,-1], -4:]