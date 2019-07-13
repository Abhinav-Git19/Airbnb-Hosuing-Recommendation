import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt


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

def dispf(temp,names):
	idfram=[]
	nafram=[]
	prfram=[]
	amfram=[]
	dist=[]
	for a,b in temp:
		idfram.append(names.loc[b,'id'])
		nafram.append(names.loc[b,"name"])
		prfram.append(names.loc[b,'price'])
		amfram.append(names.loc[b,'amenities'])
	    #dist.append(a)
	    
	ansframe=pd.DataFrame(data={'ID':idfram,'NAME':nafram ,'PRICE':prfram,'facilities':amfram})
	#pd.options.display.max_rows
	#pd.set_option('display.max_colwidth', -1)
	return ansframe


def price_filter(ansframe,price_limit):
	priceframe=ansframe[ansframe['PRICE']<=price_limit]
	return priceframe


def priority_filter(ansframe,ansfeatures,priorities,query):
	temp=knn_euc(ansfeatures,query,priorities,20)
	idfram=[]
	nafram=[]
	prfram=[]
	amfram=[]
	dist=[]
	for a,b in temp:
		idfram.append(ansframe.iloc[b,0])
		nafram.append(ansframe.iloc[b,1])
		prfram.append(ansframe.iloc[b,2])
		amfram.append(ansframe.iloc[b,3])
	    #dist.append(a)
	    
	pfilter_out=pd.DataFrame(data={'ID':idfram,'NAME':nafram ,'PRICE':prfram,'facilities':amfram})
	#pd.options.display.max_rows
	#pd.set_option('display.max_colwidth', -1)
	return pfilter_out

def price_plot(ID,calendar,price_limit):
	dates=calendar[calendar['listing_id']==ID] #For sapmle you may use id:4760472 and price=83

	dates=dates[dates['available']==True]
	datum=dates['date']
	datum=datum.tolist()

	datel = matplotlib.dates.datestr2num(datum)
	plt.plot_date(datel, dates['price'].tolist(),'k')

	horiz_line_data = np.array([price_limit for i in range(len(datel))])
	plt.plot(datel,horiz_line_data,'r--')
	plt.show()

if __name__ == '__main__':
	features=pd.read_csv("features.csv")
	query=np.random.randint(0,2,features.shape[1])
	#uery=np.array([1,1,0,0,0,1,0,0,0,0,1,1,1,0,1,1,0,1,0,1,0,0,1,1,0,1,0,1,1,0,1,0,0,0,0,0,1,1,1,0,0])
	a=list(features.columns.values)
	qulist=[]
	for i in range(query.shape[0]):
	    if query[i]==1:
	        qulist.append(a[i])
	print("Input features:\n",qulist)
	##The initial priority assingment is all 0...this excludes out features which are not in the query
	priorities=np.zeros(query.shape)

	for i in range(query.shape[0]):
		if query[i]==1:
			priorities[i]=np.random.randint(1,10)#10 corresponds to higher priority constraint while 1 is the lowest

	priority_threshold=np.nanmax(priorities)/2

	names=pd.read_csv("listings.csv",usecols=['id','name','price','amenities'])
	k=int(input("\nEnter No. of Recommedations: "))

	temp=knn_euc(features,query,priorities,k)

	##Creating new ansfeatures
	lt=[]
	for a,b in temp:
		lt.append(b)
	ansfeatures=features.iloc[lt]

	ansframe=dispf(temp,names)
	print(ansframe.iloc[:,:3]) #I have excluded out the amneties  column for now

	print("Maximum Price: $%d"%(np.nanmax(ansframe.loc[:,'PRICE'])))
	print("Average Price: $%d"%(np.average(ansframe.loc[:,'PRICE'])))
	print("Minimum Price: $%d"%(np.nanmin(ansframe.loc[:,'PRICE'])))


	#***Price filter**#
	price_limit=int(input("\nDo you want price filtering?..If no input 0 else please specify your budget: "))
	if price_limit !=0:
		priceframe=price_filter(ansframe,price_limit)
		print(priceframe.iloc[:,:3])


	#**Priority Filter**#
	choicep=input("\nDo you want to include only your high priority_features: ")
	if choicep=='Y' or choicep =='y':
		priorities=np.where(priorities < priority_threshold ,0,priorities)
		prframe=priority_filter(ansframe,ansfeatures,priorities,query)
		print(prframe.iloc[:,:3])
		choicepr=input("\nDo you want price filter on these Recommedations:")

		if choicepr=='Y' or choicepr =='y':
			price_limit2=int(input("\nRenter your budget: "))
			print(price_filter(prframe,price_limit2).iloc[:,:3])

	#**Price Plot**#
	calendar=pd.read_csv("calendar.csv")
	id1=int(input("\nEnter the id of the house for price variation analysis:"))
	price_plot(id1,calendar,max(price_limit,price_limit2))