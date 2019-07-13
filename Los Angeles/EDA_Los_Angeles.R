library(tidyverse)
library(readr)
library(corrplot)

listings2<-listings

listings2 %>% ggplot(mapping = aes(x=minimum_nights,y=price))+geom_point()+ggtitle("Price Vs Min_Nights")

ggplot(listings2,mapping = aes(x=availability_365,y=price))+geom_point()

sub<-select(listings2,price:number_of_reviews,reviews_per_month:availability_365)
View(cor(sub,use = "pairwise.complete.obs"))

listings2 %>% filter(minimum_nights<=15) %>% ggplot(mapping = aes(x=minimum_nights,y=price,group=minimum_nights))+geom_boxplot(outlier.color = "red")+ggtitle("Price vs minimum_nights")

count(listings2,neighbourhood_group)

subdat<-filter(calendar,available =='t')
subdat %>% filter(listing_id =='16228948' | listing_id =='6749145') %>%
  ggplot(subdat,mapping = aes(x=date,y=price,color=listing_id))+geom_smooth()
