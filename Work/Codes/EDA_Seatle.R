library(tidyverse)
library(readr)
library(corrplot)
listings2 <- read_csv("/media/yagami/7D6AC415329F64DB/Study Material/4-1 Final Sem/Data Mining/Airbnb Recommendation Systems/Seattle/listings2.csv", 
                      col_types = cols(last_review = col_date(format = "%Y-%m-%d")))
View(listings2)
#Here filtering is done because we have non-sensical data min_nights be as great as 1000
listings2 %>% filter(minimum_nights<=15) %>% ggplot(mapping = aes(x=minimum_nights,y=price))+geom_point()+ggtitle("Price Vs Min_Nights")
cor.test(listings2$price,listings2$minimum_nights,na.rm=TRUE)

ggplot(listings2,mapping = aes(x=availability_365,y=price))+geom_point()
sub<-select(listings2,price:number_of_reviews,reviews_per_month:availability_365)
View(cor(sub,use = "pairwise.complete.obs")) #pairwise correlation while igonring na values

corrplot(cor(sub),method ="circle")
#Price and BoxPlot
listings2 %>% filter(minimum_nights<=15) %>% ggplot(mapping = aes(x=room_type,y=price))+geom_boxplot(outlier.color = "red")+ggtitle("Price vs Roomtype")

listings2 %>% filter(minimum_nights<=15) %>% ggplot(mapping = aes(x=minimum_nights,y=price,group=minimum_nights))+geom_boxplot(outlier.color = "red")+ggtitle("Price vs minimum_nights")

count(listings2,neighbourhood_group)

not_otherneighbour<-listings2 %>% filter(neighbourhood_group !="Other neighborhoods")
ggplot(not_otherneighbour,mapping = aes(x=neighbourhood_group))+geom_bar(width = 0.61)


listings2 %>% group_by(neighbourhood_group) %>%
  summarise(max_price=max(price))

#Calendar data analysis
calendar <- read_csv("/media/yagami/7D6AC415329F64DB/Study Material/4-1 Final Sem/Data Mining/Airbnb Recommendation Systems/Seattle/calendar.csv", 
                     +     col_types = cols(available = col_logical(), 
                                            +         date = col_date(format = "%Y-%m-%d"), 
                                            +         listing_id = col_character(), price = col_number()))
subdat<-filter(calendar,available ==TRUE)
subdat %>% filter(listing_id =='6438099' | listing_id =='2493658') %>%
  ggplot(subdat,mapping = aes(x=date,y=price,color=listing_id))+geom_smooth()


#Detailed Listing analysis
#Import listings
cor_chartdf<-select_if(listings,is.numeric)
detailcorr<-cor(cor_chartdf,use = "pairwise.complete.obs")
    