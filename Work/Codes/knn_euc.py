import numpy as np
import pandas as pd


def knn_euc(features,query,priorities,k):
	features=features.as_matrix()
	result=((features-query)**2)**priorities**3
	result=np.sqrt(np.sum(result,axis=1))

	ans=[]
	for i in range(len(result)):
		ans.append((result[i],i))
	ans.sort()
	ans=ans[:k]
	return ans

def disp(temp):
	nafram=[]
	prfram=[]
	amfram=[]
	for a,b in temp:
	    nafram.append(names.loc[b,"name"])
	    prfram.append(names.loc[b,'price'])
	    amfram.append(names.loc[b,'amenities'])
	    
	ansframe=pd.DataFrame(data={'NAME':nafram ,'PRICE':prfram,'facilites':amfram})
	#pd.options.display.max_rows
	#pd.set_option('display.max_colwidth', -1)
	print(ansframe)

if __name__ == '__main__':
	features=pd.read_csv("features.csv")
	fet=features
	query=np.random.randint(0,2,features.shape[1])#This needs to be upgraded...

	a=list(features.columns.values)
	qulist=[]
	for i in range(query.shape[0]):
	    if query[i]==1:
	        qulist.append(a[i])
	print("Input features:\n",qulist)
	##The initial priority assingment is all 1...makes calculation easier
	priorities=np.ones(query.shape)
	for i in range(query.shape[0]):
		if query[i]==1:
			priorities[i]=np.random.randint(1,10)#10 corresponds to higher priority constraint while 1 is the lowest


	names=pd.read_csv("listings.csv",usecols=['name','price','amenities'])
	k=int(input("Enter No. of Recommedations: "))

	temp=knn_euc(fet,query,priorities,k)
	disp(temp)

	#Now for price check...recalibrating priorities
	print("\n*******")
	for i in range(len(priorities)):
		if priorities[i]<5:
			priorities[i]=0#Should this assigned as 1 or 0?

	temp=knn_euc(fet,query,priorities,k)
	disp(temp)


	print("\n*******")
	for i in range(len(priorities)):
		if priorities[i]<8:
			priorities[i]=0

	temp=knn_euc(fet,query,priorities,k)
	disp(temp)