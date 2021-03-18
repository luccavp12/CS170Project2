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

    data2 = copy.deepcopy(data)
    current_set_of_features2 = copy.deepcopy(current_set_of_features)
    for x in range(len(current_set_of_features2)):
        # x = x + 1
        current_set_of_features2[x] = current_set_of_features2[x] + 1
        # print("current_set_of_features2[x]",current_set_of_features2[x])

    if feature_to_add != -1:
        feature_to_add2 = copy.deepcopy(feature_to_add)
        current_set_of_features2.append(feature_to_add2)
    
    # print('')
    # print("current_set_of_features2:", current_set_of_features2)
    # print('')
    # print("current_set_of_features2 [",end='')
    # for x in current_set_of_features2:
    #     x = x + 1
        # print(x + 1, "", end='')
    # print("]")
        
    for row in data2:
        # print('len(row)', len(row))
        for val in range(1,len(row)):
            if val not in current_set_of_features2:
                # print("val",val)
                row[val] = 0

    # for row in data2:
    #     print(row)
    #     break

    # print(data2)
    size = len(data2)
    # print("size =", size)
    for i in range(size):
        object_to_classify = data2[i][1:]
        # print(object_to_classify)

        label_object_to_classify = data2[i][0]

        # print("Looping over i, at location", i+1)
        # print("Object", i+1, "is in class", label_object_to_classify)

        nearest_neighbor_distance = np.inf
        nearest_neighbor_location = np.inf
        for j in range(size):
            # print("Ask if", i+1, "is nearest neighbor with", j+1)
            
            if i != j:
                distance = math.sqrt(sum((object_to_classify - data2[j][1:]) ** 2))
                # print("distance", distance)
                if distance < nearest_neighbor_distance:
                    nearest_neighbor_distance = distance
                    nearest_neighbor_location = j
                    nearest_neighbor_label = data[nearest_neighbor_location][0]

        # print("Object", i+1, "is class", label_object_to_classify)
        # print("its nearest_neighbor is", nearest_neighbor_location, "which is in class", nearest_neighbor_label)

        if label_object_to_classify == nearest_neighbor_label:
            number_correctly_classified = number_correctly_classified + 1
        
    # print("number_correctly_classified", number_correctly_classified)
    accuracy = number_correctly_classified / size
    return accuracy


###################################################################################################################
###################################################################################################################


def backward_elimination(data):
    current_set_of_features = []
    current_set_of_features_features = []
    for x in range(len(data[0]) - 1):
        current_set_of_features.append(x)

    # print("current_set_of_features", current_set_of_features)
    print("In the beginning, with all features, the accuracy of backward elimination is:", leave_one_out_cross_validation(data,current_set_of_features,-1))

    overall_best = 0
    best_accuracy_so_far_list = []

    for i in range(len(data[0]) - 1):
        # print("On level", i + 1, "of the search tree")

        # print("current_set_of_features == [",end='')
        # for x in current_set_of_features:
        #     print(x + 1, "", end='')
        # print("]")

        feature_to_remove_at_this_level = []
        # current_set_of_features_ACC = leave_one_out_cross_validation(data, current_set_of_features, 20)
        # print("current_set_of_features_ACC:", current_set_of_features_ACC)
        
        best_accuracy_so_far = 0
        for j in range(len(data[0]) - 1):
            if j in current_set_of_features: 
                # print("-- Considering removing feature", j+1)
                # print("CALCULATING ACCURACY --------------------------------------------------------------------")
                # print("current_set_of_features", current_set_of_features)
                removed_current_set_of_features = copy.deepcopy(current_set_of_features)
                removed_current_set_of_features.remove(j)
                accuracy = leave_one_out_cross_validation(data, removed_current_set_of_features, -1)
                # print("accuracy:", accuracy)
                if accuracy > best_accuracy_so_far:
                    best_accuracy_so_far = accuracy
                    feature_to_remove_at_this_level = j

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
        # current_set_of_features_features.append(current_set_of_features)
        # print("")
    
    # print("current_set_of_features_features", current_set_of_features_features)
    for x in range(len(best_accuracy_so_far_list)):
        if best_accuracy_so_far_list[x] > overall_best:
                    overall_best = best_accuracy_so_far_list[x]
                    most_accurate_feature = x

    # print("current set of features:", current_set_of_features)
    # print("most accurate feature:", most_accurate_feature)
    most_accurate_features_display = [x + 1 for x in current_set_of_features_features[most_accurate_feature + 1]]
    print("highest accuracy with backward elimination was:", most_accurate_features_display, "with an accuracy of", overall_best)
    # print("] with an accuracy of ", overall_best)
    # print("highest accuracy was with: [ ", end='')
    # for item in current_set_of_features[:most_accurate_feature + 1]:
    #     print(item,end=' ')
    # print("] with an accuracy of ", overall_best)

###################################################################################################################
###################################################################################################################

def forward_selection(data):
    current_set_of_features = []
    current_set_of_features_features = []
    overall_best = 0
    best_accuracy_so_far_list = []

    print("In the beginning, with no features, the accuracy of forward selection is:", leave_one_out_cross_validation(data,[],-1))

    for i in range(len(data[0]) - 1):
        # print("On level", i + 1, "of the search tree")

        # print("current_set_of_features == [",end='')
        # for x in current_set_of_features:
        #     print(x + 1, "", end='')
        # print("]")
        feature_to_add_at_this_level = []
        # current_set_of_features_ACC = leave_one_out_cross_validation(data, current_set_of_features, 20)
        # print("current_set_of_features_ACC:", current_set_of_features_ACC)
        
        best_accuracy_so_far = 0
        for j in range(len(data[0]) - 1):
            if j not in current_set_of_features: 
                # print("-- Considering adding feature", j+1)
                # print("CALCULATING ACCURACY --------------------------------------------------------------------")
                # print("current_set_of_features", current_set_of_features)
                accuracy = leave_one_out_cross_validation(data, current_set_of_features, j+1)
                # print("accuracy:", accuracy)
                if accuracy > best_accuracy_so_far:
                    best_accuracy_so_far = accuracy
                    feature_to_add_at_this_level = j

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
        # current_set_of_features_features.append(current_set_of_features)
        # print("")
    
    # print("current_set_of_features_features", current_set_of_features_features)
    for x in range(len(best_accuracy_so_far_list)):
        if best_accuracy_so_far_list[x] > overall_best:
                    overall_best = best_accuracy_so_far_list[x]
                    most_accurate_feature = x

    # print("current set of features:", current_set_of_features)
    # print("most accurate feature:", most_accurate_feature)
    # print("highest accuracy was with: [ ", end='')
    # for item in current_set_of_features[:most_accurate_feature + 1]:
    #     print(item,end=' ')
    # print("] with an accuracy of ", overall_best)
    most_accurate_features_display = [x + 1 for x in current_set_of_features_features[most_accurate_feature + 1]]
    print("highest accuracy on forward selection was with:", most_accurate_features_display, "with an accuracy of", overall_best)

 
if __name__ == '__main__':
    # data = pd.read_csv('CS170_small_special_testdata__95.txt', delim_whitespace=True, header=None).values
    # print(data)
    # print(len(data[0]))
    # t0 = 0
    # data = []

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
        
    