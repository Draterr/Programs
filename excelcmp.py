import pandas as pd

A = pd.read_excel('s5.xlsx', index_col = None, na_values=['NA'], usecols="B,D,E,H")
B = pd.read_excel('a7.xls',sheet_name=9 ,index_col = None, na_values=['NA'], usecols="A,A:C,S")

len_A = len(A)
len_B = len(B)
 
for i in range(len_A):
	for k in range(len_B):
		# print(A.loc[i].values)
		# print(B.loc[k].values)
		#print("this is the " + str(i) + "iteration")
		if A.loc[i].values[1] == B.loc[k].values[0] and A.loc[i].values[2] == B.loc[k].values[1]:
			B.at[k,'Unnamed: 18'] = A.loc[i].values[0]
			#print(B.head())
			B.to_excel("S5AB2 ENG.xls")
			print(B.loc[k].values)
			#print("added regno")
# print(A.loc[0].values[1])
# print(B.columns)