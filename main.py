import random
import csv

def leave_one_out_cross_validation():
    accuracy = random.random()
    return accuracy

def feature_search(reader):
    # size = 0
    csvFileList = []
    for row in reader:
        csvFileList.append(row)
    # for row in csvFileList:
    #     print(row)
    # print(csvFileList[0])
    for i in range(len(csvFileList[0]) - 1):
        print("On level", i + 1, "of the search tree")

with open('CS170_SMALLtestdata__31.txt', 'r') as f:
    reader = csv.reader(f, delimiter=' ', skipinitialspace = True)
    print(type(reader))
    print(reader)
    feature_search(reader)
    # for row in reader:
    #     print(row)







# function  feature_search_demo(data)
 
#   for i = 1 : size(data,2)-1    # size(data,2) means that it is looking at the second dimension
#                                 #, i.e. the # of columns
#     disp(['On the ',num2str(i),'th level of the search tree'])
#   end
# end