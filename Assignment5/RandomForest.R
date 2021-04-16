rm(list=ls())
set.seed(1) #reproduceability

# install packages and set library
#install.packages("randomForest")
library(randomForest)

setwd("C:/Users/Saskia/Documents/Master/NC/Ass5")
data <- read.csv('heart.csv')

## Data cleaning and converting
data$thall[data$thall == 0] <- NA
data$caa[data$caa == 4] <- NA
# Remove NA rows (only 7 rows)
data = data[complete.cases(data),]

# Sex, cp, fbs, restecg, exng, slp, thal, caa and the output must be changed to type factor
data$sex <- as.factor(data$sex)            # 0 = female, 1 = male
data$cp <- as.factor(data$cp)              # chest pain type
data$fbs <- as.factor(data$fbs)            # fasting blood sugar > 120, 0 = false, 1 = true
data$restecg <- as.factor(data$restecg)    # resting electrocardiographic results (0 = normal, 1 = ST-T or 2 = hypertrophy)
data$exng <- as.factor(data$exng)          # exercise induced angina, 0 = no, 1 = yes
data$slp <- as.factor(data$slp)            # slope, 0 = downsloping, 1 = flap, 2 = upsloping
data$thall <- as.factor(data$thall)          # 1 = fixed, 2 = normal, 3 = reversable
data$output <- as.factor(data$output)      # output, 1 = heart attack, 0 = no heart attack

# Split data into train- and testset (70% train, 30% test)
# Bootstrapping is done witin the randomForest classifier
sampling <- sample(nrow(data), 0.7*nrow(data), replace = FALSE)
train <- data[sampling,]
test <- data[-sampling,]

## parameter tuning: find best values for mtry, maxnodes and ntree
# Use cross validation
control <- trainControl(method = "cv", number = 10, search ="grid")

#Find best mtry value
set.seed(1)
tuneGrid <- expand.grid(.mtry = c(1: 15)) # test mtry values between 1 and `5`
rf_mtry <- train(output ~., data = train, method = "rf", metric = "Accuracy", tuneGrid = tuneGrid,
                 trControl = control, importance = TRUE, nodesize = 14, ntree = 300)

# store best value for mtry
best_mtry <- rf_mtry$bestTune$mtry 

# find best maxnodes
store_maxnode <- list()
tuneGrid <- expand.grid(.mtry = best_mtry)
for (maxnodes in c(2: 20)) {   # search for values of maxnodes between 2 and 20
  set.seed(1)
  rf_maxnode <- train(output ~., data = train, method = "rf", metric = "Accuracy", tuneGrid = tuneGrid,
                      trControl = control, importance = TRUE, nodesize = 14, maxnodes = maxnodes, ntree = 300)
  current_iteration <- toString(maxnodes)
  store_maxnode[[current_iteration]] <- rf_maxnode
}
results_mtry <- resamples(store_maxnode)
summary(results_mtry)

best_maxnodes <- 13

# find best number of trees
store_maxtrees <- list()
for (ntree in c(100, 250, 300, 350, 400, 450, 500, 550, 600, 800, 1000, 2000)) {
  set.seed(1)
  rf_maxtrees <- train(output ~., data = train, method = "rf", metric = "Accuracy", tuneGrid = tuneGrid,
                       trControl = control, importance = TRUE, nodesize = 14, maxnodes = best_maxnodes, ntree = ntree)
  key <- toString(ntree)
  store_maxtrees[[key]] <- rf_maxtrees
}
results_tree <- resamples(store_maxtrees)
summary(results_tree)

best_numtrees <- 600 # (or 250 or 300)

# final model: mtry = 4, maxnodes = 13 and ntrees = 600
set.seed(1)
model <- randomForest(output ~., data = train,mtry = best_mtry, maxnodes = best_maxnodes , ntree= best_numtrees, replace = FALSE)
model
pred <- predict(model, test)
mean(pred == test$output)

# RandomForest classifier with default settings for comparison
set.seed(1)
model_def <- randomForest(output ~., data = train)
model_def
pred_def <- predict(model_def, test)
mean(pred_def == test$output)
model_def$importance
