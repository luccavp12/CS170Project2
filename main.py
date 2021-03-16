import random
import csv
import numpy as np
import math
import pandas as pd
import copy
import sys

def leave_one_out_cross_validation(data, current_set_of_features, feature_to_add):
    # accuracy = random.random()

    number_correctly_classified = 0

    data2 = copy.deepcopy(data)
    current_set_of_features2 = copy.deepcopy(current_set_of_features)
    feature_to_add2 = copy.deepcopy(feature_to_add)
    current_set_of_features2.append(feature_to_add2)

        
    for row in data2:
        for val in range(1,len(row)):
            if val not in current_set_of_features2:
                row[val] = 0


        #     print("val",val)
        #     print("current_set_of_features2",current_set_of_features2)
        #     # print("row[val]",row[val])
        #     if val not in current_set_of_features2:
        #         print(val,"is in current_set_of_features2!")
        #         row[val] = 0
        #         # print("val",val)
        # # break

    # np.set_printoptions(threshold=sys.maxsize)
    # print(data2)
    # print(data2.to_string())

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
                distance = math.sqrt(sum((object_to_classify - data2[j][1:])**2))
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
    print("accuracy:", accuracy)
    return accuracy


def feature_search(data):
    current_set_of_features = []

    for i in range(len(data[0]) - 1):
        print("On level", i + 1, "of the search tree")

        print("current_set_of_features [",end='')
        for x in current_set_of_features:
            print(x + 1, "", end='')
        print("]")
        feature_to_add_at_this_level = []
        # current_set_of_features_ACC = leave_one_out_cross_validation(data, current_set_of_features, 20)
        # print("current_set_of_features_ACC", current_set_of_features_ACC)
        
        best_accuracy_so_far = 0
        for j in range(len(data[0]) - 1):
            if j not in current_set_of_features: 
                print("-- Considering adding feature", j+1)
                # print("CALCULATING ACCURACY --------------------------------------------------------------------")
                # print("current_set_of_features", current_set_of_features)
                accuracy = leave_one_out_cross_validation(data, current_set_of_features, j+1)
                if accuracy > best_accuracy_so_far:
                    best_accuracy_so_far = accuracy
                    feature_to_add_at_this_level = j

        current_set_of_features.append(feature_to_add_at_this_level)
        print("On level", i+1, "I added feature", feature_to_add_at_this_level + 1, "to current set")
        print("best_accuracy_so_far", best_accuracy_so_far)
        print("")


if __name__ == '__main__':
    # data = pd.read_csv('CS170_SMALLtestdata__31.txt', delim_whitespace=True, header=None).values
    data = pd.read_csv('CS170_small_special_testdata__95.txt', delim_whitespace=True, header=None).values
    # data = pd.read_csv('CS170_small_special_testdata__96.txt', delim_whitespace=True, header=None).values
    # print(data)
    # print(len(data[0]))
    feature_search(data) 





# def feature_search(data):
#     # csvFileList = []
#     # for row in reader:
#     #     csvFileList.append(row)
        
    
#     # print("length of csvFileList:", len(csvFileList))
#     # for row in csvFileList:
#     #     for val in row:
#     #         val = float(val)
#             # print(type(val))

#     # print(row)
#     # print(csvFileList[0])

#     current_set_of_features = []

#     for i in range(len(data[0]) - 1):
#         print("On level", i + 1, "of the search tree")
#         feature_to_add_at_this_level = []
#         best_accuracy_so_far = 0
#         for j in range(len(data[0]) - 1):
#             if j not in current_set_of_features: 
#                 print("-- Considering adding feature", j + 1)
#                 # print("CALCULATING ACCURACY --------------------------------------------------------------------")
#                 accuracy = leave_one_out_cross_validation(data, current_set_of_features, j+1)
#                 if accuracy > best_accuracy_so_far:
#                     best_accuracy_so_far = accuracy
#                     feature_to_add_at_this_level = j
#         current_set_of_features.append(feature_to_add_at_this_level)
#         print("On level", i+1, "I added feature", feature_to_add_at_this_level + 1, "to current set")

#     # print(type(csvFileList[0][0]))