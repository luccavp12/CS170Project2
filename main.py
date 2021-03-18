import random
import csv
import numpy as np
import math
import pandas as pd
import copy
import sys
import time

def leave_one_out_cross_validation(data, current_set_of_features, feature_to_add):
    number_correctly_classified = 0

    # Create a copy of data set and feature list so we don't change the originals
    data2 = copy.deepcopy(data)
    current_set_of_features2 = copy.deepcopy(current_set_of_features)
    # Change features by 1 for backend, change back for display
    for x in range(len(current_set_of_features2)):
        current_set_of_features2[x] = current_set_of_features2[x] + 1

    # Check if feature to add is not included in function call, i.e. backwards elim...
    if feature_to_add != -1:
        # If not so, you can go ahead with making copies of feature to add, and add it to list used to clean data
        feature_to_add2 = copy.deepcopy(feature_to_add)
        current_set_of_features2.append(feature_to_add2)
        
    # Iterate through all instances
    for row in data2:
        # Check each object, 0 out each feature that is not included in current set + feature to add
        for val in range(1,len(row)):
            if val not in current_set_of_features2:
                # print("val",val)
                row[val] = 0

    size = len(data2)
    
    # Iterate through all instances
    for i in range(size):
        # Current object, select all features
        object_to_classify = data2[i][1:]

        # Label in the first column is saved
        label_object_to_classify = data2[i][0]

        # Set nearest neighbor values to infinity
        nearest_neighbor_distance = np.inf
        nearest_neighbor_location = np.inf

        # Iterate through all instances again
        for j in range(size):
            # Compare all other instances to object_to_classify
            if i != j:
                # Calculate the distance formula between object_to_classify and other object 'j'
                distance = math.sqrt(sum((object_to_classify - data2[j][1:]) ** 2))
                # If you find a better distance, save it
                if distance < nearest_neighbor_distance:
                    nearest_neighbor_distance = distance
                    nearest_neighbor_location = j
                    nearest_neighbor_label = data[nearest_neighbor_location][0]

        # If the object_to_classify's label is the same label as the one you classified it as, can increase # correctly found
        if label_object_to_classify == nearest_neighbor_label:
            number_correctly_classified = number_correctly_classified + 1
        
    # Make accuracy calculation and return value
    accuracy = number_correctly_classified / size
    return accuracy

def backward_elimination(data):
    current_set_of_features = []
    # List of all iterations of feature set
    current_set_of_features_features = []

    # Adding all features to the feature set at the beginning
    for x in range(len(data[0]) - 1):
        current_set_of_features.append(x)

    print("In the beginning, with all features, the accuracy of backward elimination is:", leave_one_out_cross_validation(data,current_set_of_features,-1))

    overall_best = 0
    best_accuracy_so_far_list = []

    # Iterate through all levels
    for i in range(len(data[0]) - 1):
        feature_to_remove_at_this_level = []
        best_accuracy_so_far = 0

        # Compare each removal, and call cross validation function
        for j in range(len(data[0]) - 1):
            # Make sure we aren't removing one we already have
            if j in current_set_of_features: 
                # Calling cross validation with copy of set with guess removed
                removed_current_set_of_features = copy.deepcopy(current_set_of_features)
                removed_current_set_of_features.remove(j)
                accuracy = leave_one_out_cross_validation(data, removed_current_set_of_features, -1)
                # Checking if accuracy has improved
                if accuracy > best_accuracy_so_far:
                    best_accuracy_so_far = accuracy
                    feature_to_remove_at_this_level = j

        # Creating a list of all renditions of the feature set for finding the overall best accuracy
        current_set_of_features_copy = copy.deepcopy(current_set_of_features)
        current_set_of_features_features.append(current_set_of_features_copy)
        current_set_of_features.remove(feature_to_remove_at_this_level)
        print("On level", i+1, "I removed feature", feature_to_remove_at_this_level + 1, "from current set")
        print("current_set_of_features == [",end='')
        for x in current_set_of_features:
            print(x + 1, "", end='')
        print("]")
        print("best_accuracy_so_far", best_accuracy_so_far)
        best_accuracy_so_far_list.append(best_accuracy_so_far)
    
    # Looping through list of all accuracies to find the best overall
    for x in range(len(best_accuracy_so_far_list)):
        if best_accuracy_so_far_list[x] > overall_best:
                    overall_best = best_accuracy_so_far_list[x]
                    most_accurate_feature = x

    most_accurate_features_display = [x + 1 for x in current_set_of_features_features[most_accurate_feature + 1]]
    print("highest accuracy with backward elimination was:", most_accurate_features_display, "with an accuracy of", overall_best)

def forward_selection(data):
    current_set_of_features = []
    # List of all iterations of feature set
    current_set_of_features_features = []
    overall_best = 0
    best_accuracy_so_far_list = []

    print("In the beginning, with no features, the accuracy of forward selection is:", leave_one_out_cross_validation(data,[],-1))

    # Iterating through each level
    for i in range(len(data[0]) - 1):
        feature_to_add_at_this_level = []
        
        best_accuracy_so_far = 0
        # Compare with other feature choices
        for j in range(len(data[0]) - 1):
            # Make sure we are not using duplicates
            if j not in current_set_of_features: 
                # Calling nearest neighbors with our current set and the one we are thinking about
                accuracy = leave_one_out_cross_validation(data, current_set_of_features, j+1)
                # Decide if accuracy is better
                if accuracy > best_accuracy_so_far:
                    best_accuracy_so_far = accuracy
                    feature_to_add_at_this_level = j

        # Creating a list of all renditions of the feature set for finding the overall best accuracy
        current_set_of_features_copy = copy.deepcopy(current_set_of_features)
        current_set_of_features_features.append(current_set_of_features_copy)
        current_set_of_features.append(feature_to_add_at_this_level)
        print("On level", i+1, "I added feature", feature_to_add_at_this_level + 1, "to current set")
        print("current_set_of_features == [",end='')
        for x in current_set_of_features:
            print(x + 1, "", end='')
        print("]")
        print("best_accuracy_so_far", best_accuracy_so_far)
        best_accuracy_so_far_list.append(best_accuracy_so_far)

    for x in range(len(best_accuracy_so_far_list)):
        if best_accuracy_so_far_list[x] > overall_best:
                    overall_best = best_accuracy_so_far_list[x]
                    most_accurate_feature = x

    most_accurate_features_display = [x + 1 for x in current_set_of_features_features[most_accurate_feature + 1]]
    print("highest accuracy on forward selection was with:", most_accurate_features_display, "with an accuracy of", overall_best)

 
if __name__ == '__main__':
    fileChoice = input("(1) Small Data set\n(2) Large Data set(takes a while)\n(Press 1 or 2)\n")
    searchAlgoChoice = input("(1) Forward Selection\n(2) Backward Elimination\n(Press 1 or 2)\n")

    if fileChoice == '1' and searchAlgoChoice == '1':
        data = pd.read_csv('CS170_SMALLtestdata__31.txt', delim_whitespace=True, header=None).values 
        t0 = time.time() 
        forward_selection(data)
        t1 = time.time()
        totalTime = t1-t0
        print("totalTime:", totalTime, "seconds")
    elif fileChoice == '2' and searchAlgoChoice == '1':
        data = pd.read_csv('CS170_largetestdata__70.txt', delim_whitespace=True, header=None).values
        t0 = time.time() 
        forward_selection(data)
        t1 = time.time()
        totalTime = t1-t0
        print("totalTime:", totalTime, "seconds")
    elif fileChoice == '1' and searchAlgoChoice == '2':
        data = pd.read_csv('CS170_SMALLtestdata__31.txt', delim_whitespace=True, header=None).values 
        t0 = time.time()
        backward_elimination(data)
        t1 = time.time()
        totalTime = t1-t0
        print("totalTime:", totalTime, "seconds")
    elif fileChoice == '2' and searchAlgoChoice == '2':
        data = pd.read_csv('CS170_largetestdata__70.txt', delim_whitespace=True, header=None).values
        t0 = time.time()
        backward_elimination(data)
        t1 = time.time()
        totalTime = t1-t0
        print("totalTime:", totalTime, "seconds")
        
    