import numpy as np 
from math import sqrt
import pandas as pd
import random
from statistics import mode
import os

#Change to current working directory
os.chdir('/Users/Sam/Documents/Python/Datasets')


#Data organization and parsing

#Reading in the data set to a dataframe
orig_data = pd.read_csv('breast_cancer.txt')

#Next, separate the data into the features (predictors) and labels (classes: malignant or benign)
data = orig_data.drop(['class', 'patient_id'], axis = 1)
label = orig_data['class']

#Now we need to replace missing values in the data with the number zero.
data['bare_nuclei'].replace('?',0.0, inplace = True)
data['bare_nuclei'] = data['bare_nuclei'].astype('float')

#Convert both features (data) and labels
data = list(data.values)
label = list(label)

#Reference dictionary for easy to read results. 
dict = {2:'benign',4:'malignant'}


#Must sort from smallest to largest to get similarity rankings.
def euclid(x,y):
    sums = 0.0
    for i in range(len(x)):
        sums += pow((x[i] - y[i]),2)

    return sqrt(sums)

#Split data to train and test samples
def train_test_split(data,label, test_ratio):
    x_data = []
    x_test = []
    y_test = []
    train_count = 0
    test_count = 0
    for i in range(len(data)):
        if random.random() < test_ratio:
            test_count += 1
            x_test.append(data[i])
            y_test.append(label[i])
        else:
            train_count += 1
            x_data.append((data[i],label[i]))
            
    return x_data, x_test, y_test

#Get closest neighbors
def getNeighbors(data, testInstance,similarity,k):
    neighbor = []
    for i in range(len(data)):
        neighbor.append(((similarity(data[i][0],testInstance)),data[i][1]))
    
    neighbor.sort(key=lambda tup: tup[0]) 
    
    neighbors = pd.DataFrame()
    neighbors['euclid'] = [x[0] for x in neighbor]
    neighbors['label'] = [x[1] for x in neighbor]
    
    return neighbors['label'][:k].tolist()
 
#Iteratively call getNeighbors for all testing points    
def get_results(x_data,x_test,k):
    res_list = []
    label = [x[1] for x in x_data]
    for i in range(len(x_test)):
        kNeighbor = getNeighbors(x_data, x_test[i],euclid,k)
        res_list.append(mode(kNeighbor))
    return res_list
   
#Determine accuracy      
def get_accuracy(actual, predicted):
    count = 0
    for i in range(len(actual)):
        if actual[i] == predicted[i]:
            count += 1
    num_correct = count
    num_incorrect = len(actual) - count
    return "Accuracy: " + str(count / len(actual)*100) + " percent" + '\n' + "Number correct: " + str(num_correct) + '\n' + "Number incorrect: " + str(num_incorrect)

def view_results(actual,predicted):
    result = pd.DataFrame()
    for i in range(len(actual)):
        actual[i] = dict[actual[i]]
        predicted[i] = dict[predicted[i]]
    result['ACTUAL'] = actual
    result['PREDICTED'] = predicted
    result['CORRECT?'] = [actual[i] == predicted[i] for i in range(len(actual))]
    
    return result

#Testing dataset 20% of full dataset
x_data, x_test, y_test = train_test_split(data,label,0.2)

#Get results
predicted_results = get_results(x_data,x_test,5)

#Format results
viewed_results = view_results(y_test,predicted_results)
viewed_results = viewed_results[:20]

#Print results and accuracy
print(viewed_results)
print()
print(get_accuracy(y_test,predicted_results))


