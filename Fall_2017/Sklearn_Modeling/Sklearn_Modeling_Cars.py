###########################################
#
# Gaussian Naive Baye Probability Model
#
# Created by: Sam Showalter
# Creation Date: 2017-07-23
#
###########################################


"""
INFORMATION ABOUT DATASET: Classifying Overall Rating Cars Get Based On Attributes

6.  Car Evaluation Database was derived from a simple hierarchical
   decision model originally developed for the demonstration of DEX
   (M. Bohanec, V. Rajkovic: Expert system for decision
   making. Sistemica 1(1), pp. 145-157, 1990.). The model evaluates
   cars according to the following concept structure:

   CAR                      car acceptability
   . PRICE                  overall price
   . . buying               buying price
   . . maint                price of the maintenance
   . TECH                   technical characteristics
   . . COMFORT              comfort
   . . . doors              number of doors
   . . . persons            capacity in terms of persons to carry
   . . . lug_boot           the size of luggage boot
   . . safety               estimated safety of the car

7. Attribute Values:

   buying       v-high, high, med, low
   maint        v-high, high, med, low
   doors        2, 3, 4, 5-more
   persons      2, 4, more
   lug_boot     small, med, big
   safety       low, med, high

8. Missing Attribute Values: none

9. Class Distribution (number of instances per class)

   class      N          N[%]
   -----------------------------
   unacc     1210     (70.023 %) 
   acc        384     (22.222 %) 
   good        69     ( 3.993 %) 
   v-good      65     ( 3.762 %) 

** We will predict the estimated rating of a car (low, med, high, v-high) using the data shown and compare it 
** across different models with sklearn.
"""

###########################################
#
# Import Dependencies and Data Collection
#
###########################################

import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd 
import os
from matplotlib import style

#Style that will be used for the graph that shows model comparison
style.use('ggplot')

#Dictionary to translate numbers into user friendly strings for overall car rating
target_dict = {1:'Unacceptable',2:'Acceptable',3:'Good',4:'Very_Good'}

#Change this to the working directory of your dataset
os.chdir('/Users/Sam/Documents/Python/DPUDS/DPUDS_Meetings/Fall_2017/Sklearn_Modeling')

#Train test split
from sklearn.model_selection import train_test_split

# K-Nearest Neighbors
from sklearn.neighbors import KNeighborsClassifier

# Random Forest Classifier
from sklearn.ensemble import RandomForestClassifier

# Support Vector Machine model
from sklearn.svm import SVC

# Logistic Regression
from sklearn.linear_model import LogisticRegression

# Stochastic Gradient Descent Optimizer
from sklearn.linear_model import SGDClassifier

# Gaussian Naive Bayes Optimizer
from sklearn.naive_bayes import GaussianNB


###########################################
#
# Data Refinement and Dummy Variables
#
###########################################

#Refines our data in place
def refine_data_master(data):
	# Buy price
	data.replace({'buy_price':{'vhigh':4,'high':3,'med':2,'low':1}}, regex = True, inplace = True)
	# Maintanence Price
	data.replace({'maintanence_price':{'vhigh':4,'high':3,'med':2,'low':1}}, regex = True, inplace = True)
	# Number of doors
	data.replace({'num_doors':{'2':2,'4':4,'more':6}}, regex = True, inplace = True)
	# Number of people
	data.replace({'num_people':{'2':2,'3':3,'4':4,'5more':5}}, regex = True, inplace = True)
	# Trunk Size
	data.replace({'trunk_size':{'small':1,'med':2,'big':3}}, regex = True, inplace = True)
	# Safety rating
	data.replace({'safety_rating':{'low':1,'med':2,'high':3}}, regex = True, inplace = True)

	# Overall rating (our labels) (MAKE SURE unacc goes before acc, and vgood before good)
	data.replace({'overall_rating':{'vgood':4,'good':3,'unacc':1,'acc':2}}, regex = True, inplace = True)

	#Data without labels
	data_features = data.drop('overall_rating',axis = 1)

	#Data labels only
	data_labels = data.overall_rating

	return data_features, data_labels
	
############################################
#
# Supplement Functions for gathering samples
#
############################################


'''
This function is equivalent to what we saw in the KNN
tutorial. It shows the accuracy of the model, including
the number correct and the number incorrect. Its inputs
are the actual list of labels and the list of predicted
labels.
'''
def viz_get_accuracy(actual, predicted):
    count = 0
    for i in range(len(actual)):
        if actual[i] == predicted[i]:
            count += 1
    num_correct = count
    num_incorrect = len(actual) - count
    return "Accuracy: " + str(count / len(actual)*100) + " percent" + '\n' + "Number correct: " + str(num_correct) + '\n' + "Number incorrect: " + str(num_incorrect)


'''
Inputs are actual and predicted labels for the dataset. 
This model prints the results of the model next to the actual
results for side-by-side viewing.
'''
def viz_view_results(actual,predicted):
    result = pd.DataFrame()
    for i in range(len(actual)):
        actual[i] = target_dict[actual[i]]
        predicted[i] = target_dict[predicted[i]]
    result['ACTUAL'] = actual
    result['PREDICTED'] = predicted
    result['CORRECT?'] = [actual[i] == predicted[i] for i in range(len(actual))]

    return result

    #print(view_results(actual,predictions))
	#print()
	#print(get_accuracy(actual,predictions))

'''
This model iteratively returns a single value,
the accuracy of the model as found by 
num_correct/tot_num_samples. This is the function
that will be called iteratively when the sampling
engine runs for all sklearn models. Inputs are 
actual labels, and predicted labels.
'''
def iter_accuracy(actual, predicted):
	correct_count = 0
	for i in range(len(actual)):
		if actual[i] == predicted[i]:
			correct_count += 1
	accuracy = correct_count/len(actual)
	return accuracy

'''
This is the sklearn KNN model. By passing in the train and test
data, we can train the model and then test it. This function
does exactly that and then returns the accuracy, as found
with the function iter_accuracy
'''
def KNN_train_test_model(X_train, X_test, y_train, y_test):
	KNN_clf = KNeighborsClassifier(n_neighbors = 5, 
								   weights = 'uniform', 
								   algorithm = 'auto', 
								   leaf_size = 30)
	KNN_clf.fit(X_train,y_train)
	predicted = list(KNN_clf.predict(X_test))
	actual = list(y_test)

	accuracy = iter_accuracy(actual,predicted)

	return accuracy

'''
This is the sklearn SVM model. By passing in the train and test
data, we can train the model and then test it. This function
does exactly that and then returns the accuracy, as found
with the function iter_accuracy
'''
def SVM_train_test_model(X_train, X_test, y_train, y_test):
	SVM_clf = SVC()
	SVM_clf.fit(X_train,y_train)
	predicted = list(SVM_clf.predict(X_test))
	actual = list(y_test)

	accuracy = iter_accuracy(actual,predicted)

	return accuracy

'''
This is the sklearn GNB model. By passing in the train and test
data, we can train the model and then test it. This function
does exactly that and then returns the accuracy, as found
with the function iter_accuracy
'''
def GNB_train_test_model(X_train, X_test, y_train, y_test):
	GNB_clf = GaussianNB()
	GNB_clf.fit(X_train, y_train)
	predicted = list(GNB_clf.predict(X_test))
	actual = list(y_test)

	accuracy = iter_accuracy(actual,predicted)

	return accuracy

'''
This is the sklearn Stochastic Gradient Descent model. By passing 
in the train and test data, we can train the model and then test it. 
This function does exactly that and then returns the accuracy, as 
found with the function iter_accuracy.
'''
def SGDC_train_test_model(X_train, X_test, y_train, y_test):
	SGDC_clf = SGDClassifier(loss = 'hinge', 
							 alpha = 0.0001, 
							 fit_intercept = True, 
							 learning_rate = 'optimal', 
							 average = False)
	SGDC_clf.fit(X_train, y_train)
	predicted = list(SGDC_clf.predict(X_test))
	actual = list(y_test)

	accuracy = iter_accuracy(actual,predicted)

	return accuracy

'''
This is the sklearn Random Forest model. By passing 
in the train and test data, we can train the model and then test it. 
This function does exactly that and then returns the accuracy, as 
found with the function iter_accuracy.
'''
def RF_train_test_model(X_train, X_test, y_train, y_test):
	RF_clf = RandomForestClassifier(n_estimators = 10, 
									criterion = 'gini', 
									max_depth = None, 
									bootstrap = True)
	RF_clf.fit(X_train, y_train)
	predicted = list(RF_clf.predict(X_test))
	actual = list(y_test)

	accuracy = iter_accuracy(actual,predicted)

	return accuracy

'''
This is the sklearn Logistic Regression model. By passing 
in the train and test data, we can train the model and then test it. 
This function does exactly that and then returns the accuracy, as 
found with the function iter_accuracy.
'''
def LOG_train_test_model(X_train, X_test, y_train, y_test):
	LOG_clf = LogisticRegression(penalty = 'l2', 
								 fit_intercept = True, 
								 solver = 'liblinear',
								 class_weight = None)
	LOG_clf.fit(X_train, y_train)
	predicted = list(LOG_clf.predict(X_test))
	actual = list(y_test)

	accuracy = iter_accuracy(actual,predicted)

	return accuracy


###########################################
#
#        Gathering Samples Function 
#		 and Visualization Function
#
###########################################

'''
Main engine of the model. For each model specified above, this 
function will run it and store the accuracy data as a dictionary.
The keys for this dictionary are the names of the functions above,
before the first underscore. This function allows you to specify
the number of samples you would like to collect, the test ratio for
how much of the dataset you want to predict, and a list of the
models that you want to provide. For this model we are going to predict
all six.
'''
def gather_samples(models,num_samples,test_ratio,data_features,data_labels):
	results_dict = {}
	model_tags = []
	for model in models:
		res_list = []
		model_tag = model.__name__.rsplit('_')[0]
		model_tags.append(model_tag)
		for j in range(num_samples):
			X_train, X_test, y_train, y_test = train_test_split(data_features, data_labels, test_size = test_ratio)
			accuracy = model(X_train,X_test,y_train,y_test)
			res_list.append(accuracy)
		results_dict[model_tag] = res_list

	results_df = pd.DataFrame.from_dict(results_dict)

	return results_df

'''
This function visualizes the results of the gather samples function
above. By taking the results dataframe, it will give a graph of the boxplots 
of accuracy results, one for each model. This will be labeled by the headers 
of the dataframe.
'''
def visualize_results(results_df):
	#Intialize and plot data
	plt.figure()
	results_df.boxplot()

	#Axes labels and title
	plt.xlabel('Classifier Model')
	plt.ylabel('Prediction Accuracy')
	plt.title('Classifier Accuracy Analysis with Sklearn')

	#Show the plot
	plt.show()


###########################################
#
# 			Data Pull and Main Method
#
###########################################

#Import data using pandas
data = pd.read_csv('Car_Ratings.csv', names = ['buy_price', 
		   										   'maintanence_price',
		   										   'num_people',
		   										   'num_doors',
		   										   'trunk_size',
		   										   'safety_rating',
		   										   'overall_rating'])

'''
The main method runs the model, taking in the test ratio you want, 
the number of samples you want, and the dataset, after it has been
refined of all bad data.
'''
def main(data, num_samples, test_ratio):

	data_features, data_labels = refine_data_master(data)

	classifiers = [RF_train_test_model,
	               LOG_train_test_model,
	               GNB_train_test_model,
	               KNN_train_test_model,
	               SVM_train_test_model,
	               SGDC_train_test_model]

	results_df = gather_samples(classifiers,num_samples,test_ratio,data_features,data_labels)

	visualize_results(results_df)

main(data, 100, 0.25)
#main(data, 100, 0.90)





