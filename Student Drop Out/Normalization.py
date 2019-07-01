from collections import defaultdict
from Student import Student

__author__ = 'shamin'

import csv


class Normalization:
    def generateNSemesterList(self):
        outputCsv = "/home/shamin/PycharmProjects/Student Drop Out/semesterEnrolled"
        extension = ".csv"

        file = "/home/shamin/PycharmProjects/Student Drop Out/normalizedInfo.csv"
        with open(file, 'rb') as f:
            reader = csv.reader(f)
            studentList = list(reader)

        file = "/home/shamin/PycharmProjects/Student Drop Out/normalizedGrades.csv"
        with open(file, 'rb') as f:
            reader = csv.reader(f)
            gradeList = list(reader)

        for i in range(1, 13):
            # n = i
            tempCsv = outputCsv + str(i) + extension

            with open(tempCsv, "wb") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow('')

            for each in studentList:
                # print each
                enrolledSemesters = defaultdict(list)
                semesterValidation = {}
                for eachx in gradeList:
                    if(each[0]==eachx[0]):
                        if(semesterValidation.has_key(eachx[2])):
                            continue
                        semesterValidation.update({eachx[2]:eachx[0]})
                        enrolledSemesters[eachx[0]].append(eachx[2])

                with open(tempCsv, "ab") as csv_file:
                    writer = csv.writer(csv_file)
                    tempList = {}
                    tempList[each[0]] = each[0]
                    tempList.update({each[0]:enrolledSemesters[each[0]]})

                    if len(enrolledSemesters[each[0]])>=i:
                        writer.writerow(tempList.items())



def getCgpaAndDroppedCount(self):
    outputCsv = file = "/home/shamin/PycharmProjects/Student Drop Out/normalizedCgpaAndDroppedCount.csv"
    with open(outputCsv, "wb") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['id,cgpa,dropped_semesters'])

    file = "/home/shamin/PycharmProjects/Student Drop Out/semesterEnrolled.csv"
    with open(file, 'rb') as f:
        reader = csv.reader(f)
        enrolledList = list(reader)

    for each in enrolledList:
        # print each
        each = str(each)
        studentId = each[each.find('\'') + 1:each.find(',') - 1]

        if len(studentId) == 0 or len(studentId) == 6:
            continue

        student = Student(studentId)
        cgpa = student.getCGPA()[0]
        # print 'CGPA is:',cgpa

        enrolledSemesters = each[each.find(',') + 3:each.find(')') - 1].split(", ")

        tag = False
        dropCount = 0
        for x in enrolledSemesters:
            if tag == False:
                x = str(x)
                lastSemester = x[1:-1]
                tag = True
            else:
                x = str(x)
                currentSemester = x[1:-1]
                gap = int(currentSemester) - int(lastSemester)
                lastSemester = currentSemester
                # print 'Gap is:',gap,currentSemester,lastSemester
                if gap > 1:
                    dropCount = dropCount + gap

        #   runningSemester is now written manually, later it will be replaced by a function
        runningSemester = 46
        gap = runningSemester - int(lastSemester)
        if gap > 1:
            dropCount = dropCount + gap

        # print 'Drop count for',studentId,'is:',dropCount

        with open(outputCsv, "ab") as csv_file:
            writer = csv.writer(csv_file)
            ss = str(cgpa) + ''
            output = studentId + ',' + ss + ',' + str(dropCount)
            # print output
            writer.writerow([output])


def generateTermGpa(self):
    outputCsv = "/home/shamin/PycharmProjects/Student Drop Out/normalizedTermGpa.csv"
    with open(outputCsv, "wb") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['id,term_gpa'])

    file = "/home/shamin/PycharmProjects/Student Drop Out/semesterEnrolled.csv"
    with open(file, 'rb') as f:
        reader = csv.reader(f)
        enrolledList = list(reader)

    for each in enrolledList:
        # print each
        each = str(each)
        studentId = each[each.find('\'') + 1:each.find(',') - 1]
        enrollements = each[each.find(',') + 3:each.find(']')]

        if len(studentId) == 0 or len(studentId) == 6:
            continue
        listOfEnrollments = list(enrollements.split(", "))

        student = Student(studentId)

        # print listOfEnrollments
        with open(outputCsv, "ab") as csv_file:
            # print 'ID =',studentId
            gpaList = []

            for terms in listOfEnrollments:
                writer = csv.writer(csv_file)
                # print 'Term is',str(terms)

                terms = terms[1:-1]
                tgpa = student.getTGPA(int(terms))
                gpaList.extend([tgpa])

                # print len(gpaList)
            writer.writerow([studentId, gpaList])




