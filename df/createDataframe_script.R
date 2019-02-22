library(readxl)
library(readr)
library(dplyr)
library(stringr)
library(tibble)

#Food dataframe (the one given for the datathon)
Food_df <- read_excel("~/Desktop/Datathon/Food/chronicgdayconsumers.xlsx", col_names = TRUE, sheet = 3)
colnames(Food_df) <- gsub(" ", "_", Food_df[2,])
Food_df <- Food_df[-2,]

#######################
## CREATE DATAFRAME: ##
#######################

#CO2 == Dataframe with info of the carbon footprint
CO2 <- read.csv("~/Desktop/Datathon/CO2df.csv", sep = ",")

#Change units to grams
CO2$Serving.Size[which(CO2$SS.Unit == "ounce")] <- CO2$Serving.Size[which(CO2$SS.Unit == "ounce")]*28
CO2$Serving.Size[which(CO2$SS.Unit == "tbsp")] <- CO2$Serving.Size[which(CO2$SS.Unit == "tbsp")]*14.3
CO2$Serving.Size[which(CO2$SS.Unit == "egg")] <- CO2$Serving.Size[which(CO2$SS.Unit == "egg")]*40
CO2$Serving.Size[which(CO2$SS.Unit == "ear/half cup kernels")] <- CO2$Serving.Size[which(CO2$SS.Unit == "ear/half cup kernels")]*112
CO2$Serving.Size[which(CO2$SS.Unit == "fl. Oz.")] <- CO2$Serving.Size[which(CO2$SS.Unit == "fl. Oz.")]*40
CO2$Serving.Size[which(CO2$SS.Unit == "portion of pound (http://www.ers.usda.gov/data/foodconsumption/FoodAvailDoc.htm)")] <- CO2$Serving.Size[which(CO2$SS.Unit == "portion of pound (http://www.ers.usda.gov/data/foodconsumption/FoodAvailDoc.htm)")]*453.59
CO2$Food <- tolower(CO2$Food)

foods_str <- unlist(str_split(tolower(toString(CO2$Food)), pattern = ", "))

#Creation of the new columns:
#column_foods == Vector with the name of the food...if it is not one of the 89 foods then it contains NA
column_foods <- rep(NA, dim(Food_df)[1])

#Creation of the column with the name of one of the 89 foods (or NA if that food does not appear)
for (i in 1:dim(Food_df)[1]){
  if (any(str_detect(tolower(Food_df$Foodex_L3[i]), foods_str))){
    if(str_detect(tolower(Food_df$Foodex_L3[i]), "pineapple")){
      column_foods[i] <- "pineapple"
    } else if(str_detect(tolower(Food_df$Foodex_L3[i]), "eggplant")){
      column_foods[i] <- "eggplant"
    } else if(str_detect(tolower(Food_df$Foodex_L3[i]), "sweet corn")){
        column_foods[i] <- "sweet corn"
    } else if(str_detect(tolower(Food_df$Foodex_L3[i]), "lamb") & str_detect(tolower(Food_df$Foodex_L3[i]), "lettuce")){
      column_foods[i] <- "lettuce"  
    } else if(str_detect(tolower(Food_df$Foodex_L3[i]), "grapefruit")){
      column_foods[i] <- "grapefruit"
    } else if(str_detect(tolower(Food_df$Foodex_L3[i]), "bacon")){
      column_foods[i] <- "pork"
    } else if(str_detect(tolower(Food_df$Foodex_L3[i]), "sausage")){
      column_foods[i] <- "pork"
    } else if(str_detect(tolower(Food_df$Foodex_L2[i]), "fish")){
        column_foods[i] <- "fish"
    } else if(str_detect(tolower(Food_df$Foodex_L3[i]), "omelette")){
          column_foods[i] <- "egg"
    } else if(str_detect(tolower(Food_df$Foodex_L3[i]), "butter") & str_detect(tolower(Food_df$Foodex_L3[i]), "milk")){
      column_foods[i] <- "milk"  
    } else if(str_detect(tolower(Food_df$Foodex_L3[i]), "fries")){
      column_foods[i] <- "potato"  
    } else if(str_detect(tolower(Food_df$Foodex_L3[i]), "butterkase")){
      column_foods[i] <- "cheese" 
    } else if(str_detect(tolower(Food_df$Foodex_L3[i]), "reggiano")){
      column_foods[i] <- "cheese" 
    } else if(str_detect(tolower(Food_df$Foodex_L3[i]), "wheat flour, with eggs")){
      column_foods[i] <- "egg, wheat flour" 
    } else if(str_detect(tolower(Food_df$Foodex_L3[i]), "wheat flour")){
      column_foods[i] <- "wheat flour" 
    } else if(str_detect(tolower(Food_df$Foodex_L3[i]), "corn oil")){
      column_foods[i] <- "corn oil" 
    } else if(str_detect(tolower(Food_df$Foodex_L3[i]), "pork lard")){
      column_foods[i] <- "lard" 
    } else if(str_detect(tolower(Food_df$Foodex_L3[i]), "peanuts butter")){
      column_foods[i] <- "peanuts" 
    } else if(str_detect(tolower(Food_df$Foodex_L3[i]), "coffee beans")){
      column_foods[i] <- "coffee"
    } else if(str_detect(tolower(Food_df$Foodex_L3[i]), "wheat coffee")){
      column_foods[i] <- "wheat"
    } else if(str_detect(tolower(Food_df$Foodex_L3[i]), "ham")){
      if (str_detect(toString(foods_str[str_detect(tolower(Food_df$Foodex_L3[i]), foods_str)]), "pork")){
        column_foods[i] <- toString(foods_str[str_detect(tolower(Food_df$Foodex_L3[i]), foods_str)])
      }else{
        if (str_detect(tolower(Food_df$Foodex_L3[i]), "bechamel")){
          column_foods[i] <- toString(foods_str[str_detect(tolower(Food_df$Foodex_L3[i]), foods_str)])
        }else{
          column_foods[i] <- paste(toString(foods_str[str_detect(tolower(Food_df$Foodex_L3[i]), foods_str)]), "pork", sep = ", ")
        }
      }
    } else {
      column_foods[i] <- toString(foods_str[str_detect(tolower(Food_df$Foodex_L3[i]), foods_str)])
    }
  }
}

#df_aux == Auxiliar df created from the dataframe Food_df merged with CO2
df_aux <- add_column(Food_df, column_foods, .after = "Foodex_L3")
df_aux <- df_aux[!is.na(df_aux$column_foods),]
df_aux$Survey <- NULL
df_aux$Metrics <- NULL
df_aux$Mean<- as.numeric(df_aux$Mean)
df_aux$Nr_Consumer<- as.numeric(df_aux$Nr_Consumer)

countries <- unique(df_aux$Country)
pop_class <- unique(df_aux$Pop_Class)

#CleanFoodData == Final df
#CleanFoodData <- data.frame(Country = character(), Pop_Class = character(), Food = character(), Nr_Consumer = double(), Mean = double(), Serving_Size = double(), CO2_Per_Serving = double())
CleanFoodData <- data.frame(Country = NA, Pop_Class = NA, Food = NA, Nr_Consumer = NA, Mean = NA, Serving_Size = NA, CO2_Per_Serving = NA)

#Creation of the final dataframe with the mean of all the appearances of a food
for (country in countries){
  for (pop in pop_class){
    for (food in foods_str){
      df_temp <- filter(df_aux, Country == country & Pop_Class == pop & str_detect(column_foods, food))
      if (sum(df_temp$Nr_Consumer) != 0){
        mean <- sum(df_temp$Nr_Consumer*df_temp$Mean)/sum(df_temp$Nr_Consumer)
        CleanFoodData <- rbind(CleanFoodData ,c(country, pop, food, sum(df_temp$Nr_Consumer),mean, CO2$Serving.Size[which(CO2$Food==food)],CO2$Grams.CO2e.per.Serving[which(CO2$Food==food)]))
      }
    }
  }
}
CleanFoodData = CleanFoodData[-1,]

#Create column with food ids
ID <- rep(NA, dim(CleanFoodData)[1])
for (i in row.names(CO2)){
  ID[match(CleanFoodData$Food ,CO2[i,]$Food)==1] <- i
}
CleanFoodData<- add_column(CleanFoodData, ID, .after = "Food")
CleanFoodData$CO2_Per_Serving <- NULL
CleanFoodData$Serving_Size <- NULL

#Clean CO2 df
ID <- row.names(CO2)
CO2 <- add_column(CO2, ID, .before = "Food")
CO2$Price..1997... <- NULL
CO2$Price.Unit <- NULL
CO2$SS.Unit <- NULL
CO2$Price.per.Serving <- NULL

#Save CSV
write.csv(CleanFoodData, file = "CleanFoodData.csv", row.names=FALSE)
write.csv(CO2, file = "CO2Footprint.csv", row.names=FALSE)





