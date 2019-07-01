import random
import pydot
import pydotplus
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals.six import StringIO

__author__ = 'shamin'

import csv
from sklearn import tree, neighbors, linear_model
from Student import Student
from collections import defaultdict

#   For K_Nearest_Neighbor Classifier
from sklearn.preprocessing import StandardScaler

#   For neural_network
from sklearn.neural_network import MLPClassifier

#   Graphical Bar Chart for dropped out students
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

class Utility:

    def assignCgpa(self):
        #   Assiging the cgpa's in a Dictionary
        file = "/home/shamin/PycharmProjects/Student Drop Out/normalizedCgpaAndDroppedCount.csv"
        with open(file, 'rb') as f:
            reader = csv.reader(f)
            enrolledList = list(reader)

        cgpaList = {}
        droppedCoutnList = {}

        for grades in enrolledList:
            newLine = str(grades)
            newLine = newLine[newLine.find('\'')+1:newLine.find(']')-1]
            newLine = newLine.split(',')
            # print newLine[0]
            cgpaList.update({newLine[0]:newLine[1]})
            droppedCoutnList.update({newLine[0]:newLine[2]})
        #   Assigned
        return cgpaList,droppedCoutnList

    # this method should be called once at the very beginning of the project,
    # then should be commented out
    def getAllStudentsEnrolledSemesters(self):
        studentList = self.getStudentList()

        outputCsv = "/home/shamin/PycharmProjects/Student Drop Out/semesterEnrolled.csv"
        with open(outputCsv, "wb") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow('')

        for each in studentList:
            gradeList = self.getGradeList()
            enrolledSemesters = defaultdict(list)
            semesterValidation = {}
            for eachx in gradeList:
                if(each[0]==eachx[0]):
                    if(semesterValidation.has_key(eachx[2])):
                        continue
                    semesterValidation.update({eachx[2]:eachx[0]})
                    enrolledSemesters[eachx[0]].append(eachx[2])

            with open(outputCsv, "ab") as csv_file:
                writer = csv.writer(csv_file)
                tempList = {}
                tempList[each[0]] = each[0]
                tempList.update({each[0]:enrolledSemesters[each[0]]})

                if len(enrolledSemesters[each[0]])>0:
                    writer.writerow(tempList.items())

    def checkStatus(self, id, batch):
        student = Student(id)
        totalCredits = student.getTotalCreditsEarned()

        if batch<24:
            if totalCredits < 132:
                return False
            return True
        else:
            if totalCredits < 144:
                return False
            return True

    def getStudentList(self):
        file = "/home/shamin/PycharmProjects/Student Drop Out/normalizedInfo.csv"
        with open(file, 'rb') as f:
            reader = csv.reader(f)
            studentList = list(reader)

        return studentList

    def getGradeList(self):
        file = "/home/shamin/PycharmProjects/Student Drop Out/normalizedGrades.csv"
        with open(file, 'rb') as f:
            reader = csv.reader(f)
            gradeList = list(reader)

        return gradeList

    def getEnrolledSemesters(self):
        file = "/home/shamin/PycharmProjects/Student Drop Out/semesterEnrolled.csv"
        with open(file, 'rb') as f:
            reader = csv.reader(f,delimiter=',')
            # print list(reader)
            semestersEnrolled = list(reader)
        return semestersEnrolled

    def getSpecifiedEnrolledSemesters(self,studentId):
        allData = self.getEnrolledSemesters()

        for data in allData:
            for bits in data:
                # print bits
                input = str(bits)
                id = input[input.find('\'')+1:input.find(',')-1]
                input = input[input.find('[')+1:input.find(']')]
                if(id[0]<'0' or id[0]>'9'):
                    continue
                if id != studentId:
                    continue
                if len(input)==0:
                    return ""
                return input.split(',')

    #   run only once at the very beginning of the project
    def getIrregularStudentHistory(self):
        studentList = self.getStudentList()
        batchList = {}
        cnt = 0

        for each in studentList:
            if((each[1][0]<'0') or (each[1][0]>'9')):
                continue
            enrollmentYear = each[1][:-1]
            semester = each[1][-1:]
            batch = int(enrollmentYear) - 2002
            batch*= 3
            batch+= int(semester)   # batch of the student
            batchList[each[0]] = batch
            # print batch,each[1]

        semesterEnrolled = self.getEnrolledSemesters()

        irregularList = defaultdict(list)
        for data in semesterEnrolled:
            for bits in data:
                #print bits
                input = str(bits)
                studentId = input[input.find('\'')+1:input.find(',')-1]
                input = input[input.find('[')+1:input.find(']')]

                tmp = ""
                if(studentId[0]<'0' or studentId[0]>'9'):
                    continue

                previousSemester = batchList[studentId]
                gap = 0
                if self.checkStatus(studentId,batchList[studentId]) == True:
                    continue

                for i in range(0,len(input)):
                    if input[i]>='0' and input[i]<='9':
                        tmp += input[i]
                    else:
                        if(len(tmp)==0):
                            continue
                        gap = int(tmp) - previousSemester
                        previousSemester = int(tmp)
                        if gap>1:
                            irregularList[gap-1].append(studentId)
                        tmp = ""
                        gap = 0
                gap = 46 - previousSemester
                if gap>1:
                    irregularList[gap-1].append(studentId)
                gap = 0

        outputCsv = file = "/home/shamin/PycharmProjects/Student Drop Out/irregularityList.csv"
        with open(outputCsv, "wb") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow('')

        for each in irregularList.items():
            with open(outputCsv, "ab") as csv_file:
                writer = csv.writer(csv_file)
                if len(each)>0:
                    writer.writerow(list(each))
            print each
        return irregularList

    def getDroppedOutStudents(self):
        file = "/home/shamin/PycharmProjects/Student Drop Out/irregularityList.csv"
        # droppedOutStudents = self.getIrregularStudentHistory()
        with open(file, 'rb') as f:
            reader = csv.reader(f, delimiter=',')
            droppedOutStudents = list(reader)

        return droppedOutStudents

    def printDroppedOutStudents(self,threshold):
        droppedOutStudents = self.getDroppedOutStudents()
        totalDroppedOut = 0
        for each in droppedOutStudents:
            input = str(each)
            irregularityLabel = input[input.find('\'')+1:input.find(',')-1]
            input = input[input.find('"')+2:input.find(']')]

            if(irregularityLabel<'0' or irregularityLabel>'9'):
                continue

            irregularityCount = int(irregularityLabel)
            if irregularityCount>=threshold:

                # print 'added',[input]
                print irregularityCount,':',input
                # print input.split() #   making a list from string
                totalDroppedOut+= len(input.split())
        print '-----------------------'
        print 'Total dropped out:',totalDroppedOut

    def isDroppedOut(self,studentId,threshold):
        enrolledSemesters = self.getSpecifiedEnrolledSemesters(studentId)

        #print 'enrolled semesters:',enrolledSemesters

        previousSemester = enrolledSemesters[0]
        #print 'previous semester was ', previousSemester
        for each in enrolledSemesters:
            # print each
            if each == previousSemester:
                continue

            each = str(each)
            previousSemester = str(previousSemester)
            newEach = ""
            newPreviousSemester = ""

            for x in range(0,len(each)):
                if each[x]>='0' and each[x]<='9':
                    newEach+=each[x]
                    #print newEach[x]

            #print 'string NEW EACH is ', newEach

            for x in range(0,len(previousSemester)):
                if previousSemester[x]>='0' and previousSemester[x]<='9':
                    newPreviousSemester+=previousSemester[x]

            #print 'Current Previous is ', newPreviousSemester

            gap = int(newEach)-int(newPreviousSemester)
            if gap >= threshold:
                return 1
            previousSemester = newEach

        #Current Semester is now written manually, will be replaced by a function
        currentSemester = 46
        previousSemester = str(previousSemester)

        newPreviousSemester = ""
        for x in range(0,len(previousSemester)):
                if previousSemester[x]>='0' and previousSemester[x]<='9':
                    newPreviousSemester+=previousSemester[x]

        newPreviousSemester = int(newPreviousSemester)
        student = Student(studentId)
        if student.getTotalCreditsEarned()<144:
            if currentSemester-newPreviousSemester >= threshold:
                return 1
        return 0

    def getTrainingData(self,percentage,threshold,semesterCount):

        file = "/home/shamin/PycharmProjects/Student Drop Out/semesterEnrolled"+str(semesterCount)+".csv"
        shuffledFile= "/home/shamin/PycharmProjects/Student Drop Out/semesterEnrolledShuffled.csv"

        #   Shuffling the current file
        fileTemp = open(file)
        shuffledFileTemp = open(shuffledFile, "w")
        entire_file = fileTemp.read()
        file_in_a_list = entire_file.split("\n")
        num_lines = len(file_in_a_list)
        random_nums = random.sample(xrange(num_lines), num_lines)
        for i in random_nums:
            shuffledFileTemp.write(file_in_a_list[i] + "\n")

        shuffledFileTemp.close()
        fileTemp.close()

        with open(shuffledFile, 'rb') as f:
            reader = csv.reader(f)
            studentList = list(reader)

        #   Assiging the cgpa's in a Dictionary
        cgpaList = {}
        droppedCountList = self.assignCgpa()[1]
        #   Assigned

        #temp test
        for each in studentList:
            each = str(each)
            each = each[each.find('\'')+1:each.find(',')-1]

            student = Student(each)
            cgpaList.update({each:student.getCgpaTillCertainSemester(6)})
        #temp test

        amount = percentage * (len(studentList)-1)
        amount /= 100
        print 'Semesters In Count:',semesterCount
        print 'Total training data',amount,'(',percentage,'% )'

        totalDroppedOut = 0
        testFeatures = []
        features = []
        labels = []
        dropOutIds = []

        tempCounter = 0


        for data in studentList:
        # for each in data:
            if len(data)==0:
                continue
            each = data[0]

            each = str(each)
            each = each[each.find('\'')+1:each.find(',')-1]

            totalSemesters = str(data[0])
            totalSemesters = totalSemesters[totalSemesters.find('[')+1:totalSemesters.find(']')]

            totalSemesters= totalSemesters.replace(' ','')
            totalSemesters= totalSemesters.split(',')
            totalSemesters = len(totalSemesters)

            if len(each)==0:
                continue
            if each[0]<'0' or each[0]>'9':
                continue

            file = "/home/shamin/PycharmProjects/Student Drop Out/normalizedInfo.csv"

            with open(file, 'rb') as f:
                reader = csv.reader(f)
                normalizedInfo = list(reader)

            for item in normalizedInfo:
                if len(item)==0:
                    continue
                if item[0][0]<'0' or item[0][0]>'9':
                    continue
                if item[0]!=each:
                    continue


                ssc = float(item[11])
                hsc = float(item[17])

                #   Adding new feature: Father's Monthly Income

                incomeFlag = True
                income = item[6]
                length = len(income)
                # print 'Income is: ',income
                for i in range(0,length):
                    if income[i]>='0' and income[i]<='9':
                        continue
                    else:
                        incomeFlag = False
                        break
                if incomeFlag==False:
                    continue
                income = income + '.00'

                fathersIncome = float(income)

                if cgpaList.has_key(item[0]):

                    #   Find CGPA until 'SemesterCount' number of semesters
                    cgpa = cgpaList[item[0]]

                    # termFile = "/home/shamin/PycharmProjects/Student Drop Out/normalizedTermGpa.csv"
                    # with open(termFile, 'rb') as f:
                    #     reader = csv.reader(f)
                    #     gpaList = list(reader)
                    #
                    # count = 0
                    # totalGpa = float(0)
                    # for gpa in gpaList:
                    #     # print gpa
                    #     ss= str(gpa).replace(' ','')
                    #     id = ss[ss.find('\'')+1:ss.find(',')-1]
                    #     # print id
                    #     flag = True
                    #
                    #     if item[0]==id:
                    #         ss = ss[ss.find(',')+3:ss.find(']')]
                    #         ss= ss.split(',')
                    #         # print ss
                    #
                    #         for every in ss:
                    #             totalGpa+= float(every)
                    #             count+= 1
                    #             if count == semesterCount:
                    #                 flag = False
                    #                 break
                    #     if flag==False:
                    #         break
                    # cgpa = round(totalGpa/semesterCount,2)

                    # print 'CGPA is:',cgpa

                    droppedCount = droppedCountList[item[0]]
                    # gpas = gpaDict[item[0]]
                else:
                    break
                    # continue

                dropOutPrediction = self.isDroppedOut(each,threshold)
                tempCounter = tempCounter + 1
                # print 'Counter:',tempCounter,'Data is:',data
                if dropOutPrediction == 1:
                    # features.append([ssc,hsc,cgpa,droppedCount,fathersIncome])    #   with        father's income
                    features.append([ssc,hsc,cgpa,droppedCount,totalSemesters])                    #   with-OUT    father's income
                    labels.append([1])

                    totalDroppedOut+=1
                    dropOutIds.append(item[0])
                else:
                    # features.append([ssc,hsc,cgpa,droppedCount,fathersIncome])    #   with        father's income
                    features.append([ssc,hsc,cgpa,droppedCount,totalSemesters])                    #   with-OUT    father's income
                    labels.append([0])
                break
            if tempCounter==amount:
                break
        # print 'probable dropped out count is',totalDroppedOut,'out of',len(studentList)-1,'students'
        return features,labels,totalDroppedOut,dropOutIds,cgpaList,droppedCountList,testFeatures

    def predictDropOutAccuracy(self,percentage,threshold,semesterCount):
        data = self.getTrainingData(percentage,threshold,semesterCount)
        #print 'data is ', data

        testFeatures = data[6]
        features = data[0]
        labels = data[1]
        actualDropOuts = data[2]
        # dropOutIds = data[3]
        dropOutIds = []
        predictedDropOuts = 0

        # print 'Features are:',features

        file = "/home/shamin/PycharmProjects/Student Drop Out/semesterEnrolledShuffled.csv"
        with open(file, 'rb') as f:
            reader = csv.reader(f)
            studentsList = list(reader)

        totalStudents = len(studentsList)-1
        amount = percentage * totalStudents
        amount /= 100
        detectedDrops = 0
        undetectedDrops = 0
        falseDrops = 0
        subtractableAmount = amount
        print 'Test data size is',totalStudents-amount,'\n'


        probableDropOutIds = []

        # Random Forest Classifier
        clf = RandomForestClassifier()
        clf = clf.fit(features,labels)

        #   Decision Tree Classifier
        # clf = tree.DecisionTreeClassifier()
        # clf = clf.fit(features,labels)
        #
        # #--------------------------------------
        # # Visualize Decision Tree
        # dot_data = StringIO()
        # tree.export_graphviz(clf,
        #                      out_file=dot_data,
        #                      # feature_names=['SSC GPA','HSC GPA','CGPA','Semesters Missed','Fathers Income'],      #   with        father's income
        #                      feature_names=['SSC GPA','HSC GPA','CGPA','Semesters Missed','Total Semesters'],                         #   with-OUT    father's income
        #                      class_names=['Regular','Dropped Out'],
        #                      filled=True, rounded=True,
        #                      special_characters=True)
        # graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
        # graph.write_pdf("Visualization.pdf")
        #--------------------------------------

        #   KNearestNeighbor Classifier
        # clf = neighbors.KNeighborsClassifier()

        #   Neural_Network
        # clf = MLPClassifier()   #   Is not working, find out why
        # clf = clf.fit(features,labels)

        #   Useful for Neural Net
        #   scaler = StandardScaler()
        #   features = scaler.transform(features)


        file = "/home/shamin/PycharmProjects/Student Drop Out/normalizedInfo.csv"
        with open(file, 'rb') as f:
            reader = csv.reader(f)
            normalizedInfo = list(reader)

        for item in normalizedInfo:
            # print 'current item is',item[0]
            if item[0][0]<'0' or item[0][0]>'9':
                continue
            amount = amount - 1
            if amount>0:
                continue
            # print 'Amount is:',amount

            # student = Student(item[0])
            ssc = float(item[11])
            hsc = float(item[17])
            cgpaList = data[4]
            droppedCountList = data[5]
            # gpaList = data[6]

            if cgpaList.has_key(item[0]):
                # cgpa = cgpaList[item[0]]

                shuffledFile= "/home/shamin/PycharmProjects/Student Drop Out/semesterEnrolledShuffled.csv"
                with open(shuffledFile, 'rb') as f:
                    reader = csv.reader(f)
                    studentList = list(reader)

                cgpa = 0
                for instance in studentList:
                    # print 'This is instance:',instance

                    if len(instance)==0:
                        continue

                    each = instance[0]
                    each = str(each)
                    each = each[each.find('\'')+1:each.find(',')-1]


                    totalSemesters = str(instance[0])
                    totalSemesters = totalSemesters[totalSemesters.find('[')+1:totalSemesters.find(']')]

                    totalSemesters= totalSemesters.replace(' ','')
                    totalSemesters= totalSemesters.split(',')
                    totalSemesters = len(totalSemesters)

                    if len(each)==0:
                        continue
                    if each[0]<'0' or each[0]>'9':
                        continue
                    if each != item[0]:
                        continue

                    termFile = "/home/shamin/PycharmProjects/Student Drop Out/normalizedTermGpa.csv"
                    with open(termFile, 'rb') as f:
                        reader = csv.reader(f)
                        gpaList = list(reader)

                    count = 0
                    totalGpa = float(0)
                    for gpa in gpaList:
                        # print gpa
                        ss= str(gpa).replace(' ','')
                        id = ss[ss.find('\'')+1:ss.find(',')-1]
                        # print id
                        flag = True

                        if item[0]==id:
                            ss = ss[ss.find(',')+3:ss.find(']')]
                            ss= ss.split(',')
                            # print ss

                            for every in ss:
                                totalGpa+= float(every)
                                count+= 1
                                if count == semesterCount:
                                    flag = False
                                    break
                        if flag==False:
                            break
                    cgpa = round(totalGpa/semesterCount,2)
                    break

                droppedCount = droppedCountList[item[0]]
                # gpas = gpaList[item[0]]
            else:
                continue

            incomeFlag = True
            income = item[6]
            length = len(income)
            # print 'Income is: ',income
            for i in range(0,length):
                if income[i]>='0' and income[i]<='9':
                    continue
                else:
                    incomeFlag = False
                    break
            if incomeFlag==False:
                continue
            income = income + '.00'
            fathersIncome = float(income)

            dropOutFlag = self.isDroppedOut(item[0],threshold)


            # test = [ssc,hsc,cgpa,droppedCount,fathersIncome]       #   with        father's income
            test = [ssc,hsc,cgpa,droppedCount,totalSemesters]                       #   with-OUT    father's income
            # test = scaler.transform(test)
            # print 'current item is',item

            # if clf.predict([test]) == 1:
            if clf.predict([test]) == 1:
                probableDropOutIds.append(item[0])
                #print 'Probable DropOut ID is: ', item[0]
                predictedDropOuts = predictedDropOuts + 1
                if dropOutFlag == 1:
                    detectedDrops = detectedDrops + 1
                    dropOutIds.append(item[0])
                else:
                    falseDrops = falseDrops + 1
                    print item[0],'was false positive for drop out.'
            else:
                if dropOutFlag == 1:
                    undetectedDrops = undetectedDrops + 1


        actualDropOutPercentage = float(detectedDrops)/float(totalStudents-subtractableAmount)
        predictedDropOutPercentage = float(predictedDropOuts)/float(totalStudents-subtractableAmount)

        #--------------------------------------

        print '----------------------------------'
        print 'Total Students:',totalStudents
        # print 'Actual Dropouts:',actualDropOuts
        # print 'Detected Dropouts Within Range:',detectedDrops
        print '\n'
        print 'Undetected Dropouts Within Range:',undetectedDrops
        print 'Total Dropouts Within Range:',undetectedDrops+detectedDrops
        print '\n'
        print 'Total Predicted Dropouts:',predictedDropOuts
        print 'Failed Predictions:',falseDrops
        # print 'Total Successful Predictions:',predictedDropOuts-falseDrops
        print '----------------------------------'

        # here goes the accuracy measurements
        accuracyList = list(set(dropOutIds) & set(probableDropOutIds))
        accurateDropOuts = len(accuracyList)
        print 'Total Match count:', accurateDropOuts
        print '----------------------------------'
        cnt = 0
        for element in probableDropOutIds:
            if element in dropOutIds:
                cnt = cnt + 1
                # print 'Matched id is ', element
                # print element
            # else:
            #     print element,'--False'
        print '----------------------------------'
        accuracy = (float(accurateDropOuts)/float(undetectedDrops+detectedDrops)) * 100
        print 'Predicted DropOut Accuracy: ', round(accuracy,2) , "%"
        print '----------------------------------'

        #--------------------------------------

        return actualDropOutPercentage*100,predictedDropOutPercentage*100

    def printDroppedOutBarChart(self):
        irregularityList = "/home/shamin/PycharmProjects/Student Drop Out/irregularityList.csv"
        with open(irregularityList, "rb") as file:
            reader = csv.reader(file)
            studentList = list(reader)

        missedSemesters = []
        totalStudentCount = []

        for each in studentList:
            #for input in each:

                input = str(each)
                semester = input[input.find('\'')+1:input.find('"')-3]
                #print semester
                if len(semester) != 0:
                    semester = int(semester)
                    missedSemesters.extend([semester])
                    #print semester
                else:
                    missedSemesters.extend([0])

                #print semester,' with length of ', len(semester)

                studentCount = input[input.find('"')+2:input.find(']')]
                input = str(studentCount)

                droppedList = input.split()
                totalStudentCount.extend([len(droppedList)])

                #semester = str(input)
                #print 'bit is: ', semester, 'length was: ', len(semester)
        #print missedSemesters
        #print totalStudentCount

        y_pos = np.arange(len(missedSemesters))
        plt.bar(y_pos,totalStudentCount,align='center',alpha=3)
        plt.xticks(y_pos,missedSemesters)
        plt.ylabel('Students Count')
        plt.title('Missed Semesters')

        plt.show()

    # Faculty Initial will be parameter
    def printFacultyGradeBarChart(self,facultyInitial):
        sectionList= "/home/shamin/PycharmProjects/Student Drop Out/normalizedSections.csv"
        with open(sectionList, "rb") as file:
            reader = csv.reader(file)
            facultyCourseList = list(reader)

        gradeList= "/home/shamin/PycharmProjects/Student Drop Out/normalizedGrades.csv"
        with open(gradeList, "rb") as file:
            reader = csv.reader(file)
            studentGradeList = list(reader)


        subjectIdList = defaultdict(list)

        for each in facultyCourseList:

            if each[4] == facultyInitial :
                subjectIdList[each[4]].append([each[0]])

        for each in subjectIdList:
            ids = subjectIdList[each]

            gpaList = {}

            for x in ids:
                idCount= 0
                totalGradePoint = 0.0
                for grade in studentGradeList:
                    lst = x[0]
                    if grade[1] == lst:
                        course = grade[3]
                        idCount = idCount + 1
                        totalGradePoint+= float(grade[5])
                        # print 'Match Found for',lst
                if idCount!=0:
                    if gpaList.has_key(course):
                        totals= [gpaList[course][0]+totalGradePoint, gpaList[course][1]+idCount]
                        gpaList.update({course:totals})
                    else:
                        totals = [totalGradePoint,idCount]  #   totals = [totalGPA,totalStudentCount]
                        gpaList.update({course:totals})

        #   divided courses and the regarding gpas in separate lists
        courses = []
        gpas = []
        for each in gpaList.items():
            courses.extend([each[0]])
            gpas.extend([round(float(each[1][0]/each[1][1]),2)])

        #   drawing the graph Horizontally
        y_pos = np.arange(len(courses))
        plt.barh(y_pos,gpas,align='center',alpha=1)
        plt.yticks(y_pos,courses)
        plt.xlabel('GpaCount')
        plt.ylabel('Courses')

        plt.show()

    def printTermGpas(self):
        file = "/home/shamin/PycharmProjects/Student Drop Out/normalizedTermGpa.csv"
        with open(file, 'rb') as f:
            reader = csv.reader(f,delimiter=',')
            # print list(reader)
            gpaList = list(reader)

        gpaDict = defaultdict(list)
        for each in gpaList:
            id = each[0]
            each = str(each)
            each = each[each.find(',')+4:each.find(']')]
            each = each.split(", ")
            gpaDict.update({id:each})
            # print id, gpaDict[id]


