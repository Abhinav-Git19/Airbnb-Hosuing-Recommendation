import numpy as np
import pandas as pd

def knn_cos(features,query):
	features=features.as_matrix()
	cossim=np.dot(features,query)

	feat_norm=np.linalg.norm(features,axis=1)
	que_norm=np.linalg.norm(query)
	prod=feat_norm*que_norm
	prod=np.where(prod==0,-1,prod)

	result=cossim/prod
	ans=[]
	for i in range(len(result)):
		ans.append((result[i],i))
	return ans


if __name__ == '__main__':
	features=pd.read_csv("features.csv")
	#query=np.random.randint(0,2,features.shape[1])#This needs to be upgraded...
	query=np.array([1,1,0,0,0,1,0,0,0,0,1,1,1,0,1,1,0,1,0,1,0,0,1,1,0,1,0,1,1,0,1,0,0,0,0,0,1,1,1,0,0])
	names=pd.read_csv("listings.csv",usecols=['name'])

	k=int(input("Enter No. of Recommedations: "))
	temp=knn_cos(features,query)

	temp.sort()
	ans=temp[-k:]
	ans.reverse()
	for a,b in ans:
		print (names.loc[b,'name'])


