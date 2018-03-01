###########################################
#
# Gaussian Naive Baye Probability Model
#
# Created by: Sam Showalter
# Creation Date: 2017-07-22
#
###########################################


###########################################
#
# Import Dependencies and Data Collection
#
###########################################

#Import all dependencies
from sklearn import datasets
import random
import pandas as pd 
from numpy import mean, std, exp, pi, sqrt

#Data collection and organization
data = datasets.load_iris()

print(data.DESCR)

iris_data = list(data.data)
iris_label = list(data.target)

target_dict = {0:'setosa',1:'versicolor',2:'virginica'}

###########################################
#
#          Function Development
#
###########################################

"""
Splits data into a training and testing set. A random sample of the test_set size is set
by the test_ratio. The first input takes the entire dataset, excluding labels, the second input
takes a columns of class labels, and the third input gives a test ratio.
The first output is a tuple list of train data and train labels, the last two are the data and labels
of the testing sample.
"""
def train_test_split(data,label,test_ratio):
	train_data = []
	test_data = []
	test_label = []

	test_set_num = int(round(test_ratio*len(data),0))
	test_records = random.sample(range(len(data)), test_set_num)

	for i in range(len(data)):
		if i in test_records:
			test_data.append(data[i])
			test_label.append(label[i])
		else:
			train_record = (data[i],label[i])
			train_data.append(train_record)

	return train_data, test_data, test_label


"""
Separates records in the training dataset by class (label). This takes an input of a
training dataset and outputs a dictionary of records by class.
"""
def classSep(train_data):
	classDict = {}
	for i in range(len(train_data)):
		if train_data[i][1] not in classDict:
			classDict[train_data[i][1]] = []
		classDict[train_data[i][1]].append(train_data[i][0])

	return classDict


"""
Creates a dictionary of the mean and standard deviation of every feature for each class. This takes a dictionary
of separated training data, and outputs a dictionary of summary statistics (mean and stdev). For a dataset with three 
classes and four features, there would be a total of 3x4 = 12 means and stdevs, separated by class.
"""
def classStats(train_classDict):
	classStats = {}
	for i in train_classDict:
		if i not in classStats:
			classStats[i] = []
		classStats[i] = [(mean(j), std(j))for j in zip(*train_classDict[i])]

	return classStats


"""
Returns the probability of a feature given this attribute follows a normal (Gaussian) Distribution
with the provided mean and standard deviation.
"""
def gaussProb(mean,stddev,feature):
	num = exp(-((feature - mean)**2) / (2*(stddev**2)))
	den = stddev*sqrt(2*pi)

	if den == 0: return 0

	return num / den

"""
Gathers the probability each record belongs to each class. This information is submitted as a list
of tuples, one for each class, in the format (class, probability). Takes in the summary statistics 
dictionary of the training data, as well as the testing data to determine the probability a testing 
record belongs to each class. probDist determines what probability engine is used for the records.
"""	
def probsByClass(classStats, test_data, probDist = gaussProb):
	finalProbList = []
	
	for i in range(len(test_data)):
		tempProbList = []
		for j in classStats:
			classProb = 1
			for k in range(len(test_data[i])):
				classProb *= probDist(classStats[j][k][0],classStats[j][k][1],test_data[i][k])

			tempProbList.append((j,classProb))

		finalProbList.append(tempProbList)

	return finalProbList

"""
The function is the final step of the prediction process. The probabilities list found in the previous step 
are now ranked, and the highest probability class for each record is saved to a predictions list.
"""
def predict(finalProbList):
	predictions = []

	for i in range(len(finalProbList)):
		bestClass = -1
		bestProb = 0

		for j in range(len(finalProbList[i])):
			if bestProb < finalProbList[i][j][1]:
				bestClass = finalProbList[i][j][0]
				bestProb = finalProbList[i][j][1]
		
		predictions.append(bestClass)

	return predictions

"""
This function visualizes the results of the model. Inputs include a column of the actual labels, and
the predicted labels. It outputs a dataframe with all the results and whether or not they were correct.
"""
def getResults(actual, predicted):
	result = pd.DataFrame()
	for i in range(len(actual)):
		predicted[i] = target_dict[predicted[i]]
		actual[i] = target_dict[actual[i]]
	
	result['ACTUAL'] = actual
	result['PREDICTED'] = predicted
	result['CORRECT?'] = [actual[i] == predicted[i] for i in range(len(actual))]

	return result

"""
Prints the accuracy of the dataframe. Takes a column of actual labels v. predicted labels. It gives
the accuracy, the number of cases correctly predicted, and the number of cases incorrectly predicted.
"""
def getAccuracy(actual, predicted):
	total_cases = len(actual)
	num_correct = 0
	num_incorrect = 0
	for i in range(len(actual)):
		if actual[i] == predicted[i]:
			num_correct += 1
		else:
			num_incorrect += 1

	accuracy = (num_correct / total_cases)*100

	return "Accuracy: {0}%\nNumber correct: {1}\nNumber incorrect: {2}".format(str(accuracy),str(num_correct),str(num_incorrect))


"""
Runs the entire script for the Iris dataset.
"""
def main(data,labels,train_test_split_ratio):
	iris_train, x_test, y_test = train_test_split(data, labels, train_test_split_ratio)
	classSepDict = classSep(iris_train)
	classStatDict = classStats(classSepDict)
	finalProbs = probsByClass(classStatDict, x_test)
	preds = predict(finalProbs)
	results = getResults(y_test,preds)
	accuracy = getAccuracy(y_test,preds)

	print(results)
	print()
	print(accuracy)

#Execute Script
main(iris_data,iris_label,0.25)


		









