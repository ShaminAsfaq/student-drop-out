__author__ = 'shamin'

import csv

# grade= {'A+':4.0}
# grade.update({'A':3.75})
# grade.update({'A-':3.5})
# grade.update({'B+':3.25})
# grade.update({'B':3.0})
# grade.update({'B-':2.75})
# grade.update({'C+':2.5})
# grade.update({'C':2.25})
# grade.update({'D':2.0})
# grade.update({'F':0.0})

class Student:

    def assignLabTheory(self):
        labTheory = {}
        singleList = self.getGrades()
        for each in singleList:
                if(labTheory.has_key(each[3])):
                    continue
                else:
                    labTheory.update({each[3]:each[6]})
                    # labTheory[each[3]] = each[6]
        return labTheory

    def __init__(self, id):
        self.id = id


    def getGrades(self):
        file = "/home/shamin/NetBeansProjects/CSVReader/Files/normalizedGrades.csv"
        with open(file, 'rb') as f:
            reader = csv.reader(f)
            gradeList = list(reader)

        return gradeList

    def getCGPA(self):
        singleList = self.getGrades()

        bestGrade = {}
        labTheory = self.assignLabTheory()

        for each in singleList:
                if(each[0]==str(self.id)):
                    if(bestGrade.has_key(each[3])):
                        if(bestGrade[each[3]]<each[5]):
                            bestGrade[each[3]] = each[5]
                            singleList.extend([each[2],each[3],each[4],each[5],each[6]])
                    else:
                        if(each[5]!="0.00"):
                            bestGrade.update({each[3]:each[5]})

        creditsEarned = 0
        cumilitiveScore = 0.0

        for each in bestGrade:
            creditsEarned+= float(labTheory[each])
            cumilitiveScore+= (float(bestGrade[each]) * float(labTheory[each]))
        # print 'Total earned score: ', cumilitiveScore
        # print 'Total earned credits: ', creditsEarned
        if creditsEarned==0:
            cgpa = 0.0
        else:
            cgpa = round(cumilitiveScore/creditsEarned,2)
        # print 'CGPA so far: ', cgpa
        return cgpa,creditsEarned

    def getCgpaTillCertainSemester(self,semester):
        singleList = self.getGrades()

        bestGrade = {}
        labTheory = self.assignLabTheory()

        firstSemester = -1
        for each in singleList:
                if(each[0]==str(self.id)):
                    if(firstSemester==-1):
                        firstSemester= int(each[2])
                    if((int(each[2])-firstSemester)==(semester+1)):
                        break
                    if(bestGrade.has_key(each[3])):
                        if(bestGrade[each[3]]<each[5]):
                            bestGrade[each[3]] = each[5]
                            singleList.extend([each[2],each[3],each[4],each[5],each[6]])
                    else:
                        if(each[5]!="0.00"):
                            bestGrade.update({each[3]:each[5]})

        creditsEarned = 0
        cumilitiveScore = 0.0
        semesterCount = 0

        for each in bestGrade:
            creditsEarned+= float(labTheory[each])
            cumilitiveScore+= (float(bestGrade[each]) * float(labTheory[each]))
        # print 'Total earned score: ', cumilitiveScore
        # print 'Total earned credits: ', creditsEarned
        if creditsEarned==0:
            cgpa = 0.0
        else:
            cgpa = round(cumilitiveScore/creditsEarned,2)
        # print 'CGPA so far: ', cgpa
        return cgpa

    def getTotalCreditsEarned(self):
        return self.getCGPA()[1]

    def getTGPA(self,semester):
        studentGrades = self.getGrades()
        labTheory = self.assignLabTheory()

        totalTermCredits = 0
        totalTermScore = 0.0
        for each in studentGrades:
            if((each[0]==str(self.id)) & (each[2]==str(semester))):
                if(each[5]!="0.00"):
                    totalTermScore+= float(labTheory[each[3]])*float(each[5])
                    totalTermCredits+= float(labTheory[each[3]])

        # print 'Total earned score: ', totalTermScore
        # print 'Total earned credits: ', totalTermCredits
        if totalTermCredits == 0:
            return 0
        else:
            termCredits = totalTermCredits
            # print 'TGPA in semester ',semester,' is: ',round(totalTermScore/totalTermCredits,2)
            return round(totalTermScore/totalTermCredits,2)
