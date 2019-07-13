library(readr)
library(tidyverse)

ansframe <- commandArgs(trailingOnly = TRUE)

tmp<-ansframe$facilties
library(stringr)
tmp<-str_replace_all(tmp,"\\{","")
tmp<-str_replace_all(tmp,"\\}","")
tmp<-str_replace_all(tmp,'\\"',"")

tmp1<-str_split(tmp,",")

options(stringsAsFactors = FALSE)

library(qdapTools)
room_features <- mtabulate(tmp1)
room_features$V1<-NULL

cat(room_features)