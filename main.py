import random
import csv

def leave_one_out_cross_validation():
    accuracy = random.random()
    return accuracy

# with open('CS170_SMALLtestdata__31.txt', newline = '') as vals:
#     val_reader = csv.reader(vals, delimiter='t')
#     for val in val_reader:
#         print(val)




with open('CS170_SMALLtestdata__31.txt', 'r') as f:
    reader = csv.reader(f, delimiter=' ', skipinitialspace = True)
    for row in reader:
        print(row)
















        # for val in row:
        #     if val != '':
        #         print(val)

# def feature_search(data):
#     for 

# function  feature_search_demo(data)
 
#   for i = 1 : size(data,2)-1    # size(data,2) means that it is looking at the second dimension
#                                 #, i.e. the # of columns
#     disp(['On the ',num2str(i),'th level of the search tree'])
#   end
 
# end