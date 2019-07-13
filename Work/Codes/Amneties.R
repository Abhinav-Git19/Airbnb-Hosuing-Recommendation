library(readr)
library(tidyverse)

listings <- read_csv("/media/yagami/7D6AC415329F64DB/Study Material/4-1 Final Sem/Data Mining/Airbnb Recommendation Systems/Seattle/listings.csv")
amneties <-listings$amenities

tmp<-amneties
library(stringr)
tmp<-str_replace_all(tmp,"\\{","")
tmp<-str_replace_all(tmp,"\\}","")
tmp<-str_replace_all(tmp,'\\"',"")

tmp1<-str_split(tmp,",")

options(stringsAsFactors = FALSE)
#This is just a sample script from line 17 to 34
#dat <- data.frame(id = c("R1", "R2", "R3", "R4"),
 #                 col1 = c(3, 4, 1, 2),
  #                col2 = c(4, 6, 5, 6),
   #               col3 = c(5, 7, NA, 7),
    #              col4 = c(8, NA, NA, 9)
#)

# Melt it down
#dat.melt <- melt(dat, id.var = "id")

# Cast it back out, with the row IDs remaining the row IDs
# and the values of the columns becoming the columns themselves.
# dcast() will default to length to aggregate records - which means
# that the values in this data.frame are a count of how many times
# each value occurs in each row's columns (which, based on this data,
# seems to be capped at just once).
#dat.cast <- dcast(dat.melt, id ~ value)

library(qdapTools)
room_features <- mtabulate(tmp1)
room_features$V1<-NULL
new_listings <-cbind(listings['name'],room_features)

new_listings <- data.frame(new_listings[,-1], row.names = new_listings[,1])

library(FNN)
get.knn(room_features, k=5)
#Getting random querry for now ....can be made interactive
query<-matrix(round(runif(41)), 1, 41)
nnresult<-get.knnx(room_features,query,k=7)
for(i in 1:7) {
  print (new_listings[nnresult$nn.index[1,i],'name'])
}
