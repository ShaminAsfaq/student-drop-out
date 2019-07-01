from Normalization import Normalization
from Utility import Utility
from Student import Student
__author__ = 'shamin'


#   The next THREE lines are meant to be executed only once in the lifetime of this project
# normalization = Normalization()
# normalization.getCgpaAndDroppedCount()
# normalization.generateTermGpa()
# normalization.generateNSemesterList() #   N is the number of semesters a students has enrolled so far

utility = Utility()

#   W A R N I N G
#   The next TWO lines should be executed only ONCE in the lifetime of the project.
#   utility.getIrregularStudentHistory()
#   utility.getAllStudentsEnrolledSemesters()


# Printing the term GPA's for every student
# utility.printTermGpas()


#   if you want to see the D R O P O U T prediction of any particular student then
#   enter her/his id beside 'id', enter how much from the actual data you want
#   as training data and also enter the Threshold for Dropout. This here
#   takes 6 semesters gap as a dropout case.
#
#
#   Training data is not randomly chosen yet , but pretty soon.
#
#   Test data is (100-N)% of the main data where N% is the training data.
#
#   Wait for a F E W - S E C O N D S after executing the project.
#

trainingDataPercentage = 60     #   N = 60 here.
dropOutThreshold = 3            #   T = 6
semesterCount = 5               #   C = Number of semester's results that will be counted


#   to check the dropout prediction status of a certain student
#   id=5
#
#   prediction = utility.predictDropOut(id, trainingDataPercentage, dropOutThreshold)
#   if prediction[0]==1:
#     print 'Student id',id,'is on RISK of drop out'
#   else:
#     print 'Student id',id,'is safe'

# plot graph


# import matplotlib
# matplotlib.use('Qt4Agg')
# from matplotlib import pyplot as plt
#
# dt = [94.30,90.76,91.06,82.79]
# dt = [96.14,89.57,85.32,87.05,93.14,73.38]    #   updated and average of 4 results for each N = 1
# knn = [78.66,72.99,61.49,51.23]
# rf = [95.28,89.88,90.37,76.44]

# dt = [96,90,83,81]
# knn = [78,72,61,51]
# rf = [95,89,90,76]

# n = [1,2,3,4,5,6]
#
# plt.plot(n,dt,linewidth='2')
# # plt.plot(n,knn,linewidth='2')
# # plt.plot(n,rf,linewidth='2')
# plt.ylabel('Accuracy')
# plt.xlabel('Semester Count')
# plt.show()


#  just to check the accuracy
percentageRatio = utility.predictDropOutAccuracy(trainingDataPercentage,dropOutThreshold,semesterCount)

print 'Actual Dropout Percentage:',round(percentageRatio[0],2),"%",'(within test data)'
print 'Predicted Dropout Percentage:',round(percentageRatio[1],2),"%",'(within test data)'




# utility.printDroppedOutBarChart()
# utility.printFacultyGradeBarChart("SM")
