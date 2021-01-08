from flask import Flask, render_template, request
import sqlite3 as sql
from datetime import datetime as dt
import time
import re

app = Flask(__name__)

host = 'http://127.0.0.1:5000/'


@app.route('/')
def index():
    return render_template('test.html')

@app.route('/staLogin', methods=['POST', 'GET'])
def staLogin():
    error = ""

    if request.method == 'POST':
        input_username=request.form['Username']
        input_password=request.form['Password']
        result = validateS(input_username,input_password)
        connection = sql.connect('NittanyPath.db')
        cursor = connection.execute('SELECT name FROM Students WHERE email = (?);',(input_username,))
        data=cursor.fetchall()[0][0]
        if result:
            return render_template('Stapage.html', error=error, result=result, name = data, email=input_username)
        else:
            error = 'email and password do not match'
    return  render_template("stalogin.html", error=error)


def validateS(input_username,input_password):
    connection=sql.connect("NittanyPath.db")
    cursor = connection.execute("SELECT password FROM Students WHERE email = (?);",(input_username,))
    correctpassword = cursor.fetchall()[0][0]
    if input_password == correctpassword:
        return True
    else:
        return False

@app.route('/Stapage', methods=['POST', 'GET'])
def Stapage():
    if request.method=="POST":
        passedemail=request.form["hidden_value"]
        connection = sql.connect('NittanyPath.db')
        cursor = connection.execute('SELECT name FROM Students WHERE email = (?);', (passedemail,))
        data = cursor.fetchall()[0][0]
        return render_template("Stapage.html",email=passedemail,name=data)



@app.route('/Flogin', methods=['POST', 'GET'])
def Flogin():
    error = ""

    if request.method == 'POST':
        input_username = request.form['Username']
        input_password = request.form['Password']
        result = validateF(input_username, input_password)
        connection = sql.connect('NittanyPath.db')
        cursor = connection.execute('SELECT name FROM Professors WHERE email = (?);', (input_username,))
        data = cursor.fetchall()[0][0]
        if result:
            return render_template('Fpage.html', error=error, result=result, name=data, email=input_username)
        else:
            error = 'email and password do not match'
    return render_template("Flogin.html", error=error)


def validateF(input_username,input_password):
    connection=sql.connect("NittanyPath.db")
    cursor = connection.execute("SELECT password FROM Professors WHERE email = (?);",(input_username,))
    correctpassword = cursor.fetchall()[0][0]
    if input_password == correctpassword:
        return True
    else:
        return False

@app.route('/checkInfo', methods=['POST', 'GET'])
def checkInfo():
    if request.method == 'POST':
        passedEmail=request.form['hidden_value']
        connection = sql.connect('NittanyPath.db')
        cursor = connection.execute('SELECT name FROM Students WHERE email = (?);', (passedEmail,))
        data = cursor.fetchall()[0][0]
        cursor = connection.execute('SELECT age FROM Students WHERE email = (?);', (passedEmail,))
        age = cursor.fetchall()[0][0]
        cursor = connection.execute('SELECT gender FROM Students WHERE email = (?);', (passedEmail,))
        gender = cursor.fetchall()[0][0]
        cursor = connection.execute('SELECT major FROM Students WHERE email = (?);', (passedEmail,))
        major = cursor.fetchall()[0][0]
        cursor = connection.execute('SELECT street FROM Students WHERE email = (?);', (passedEmail,))
        street = cursor.fetchall()[0][0]
        cursor = connection.execute('SELECT zipcode FROM Students WHERE email = (?);', (passedEmail,))
        zipcode = cursor.fetchall()[0][0]
        cursor = connection.execute('SELECT course_id FROM Enrolls WHERE student_email = (?);', (passedEmail,))
        courses = cursor.fetchall()
        cursor = connection.execute('SELECT section_no FROM Enrolls WHERE student_email = (?);', (passedEmail,))
        section_nos = cursor.fetchall()
        courselist= [x[0] for x in courses]
        sectionlist = [x[0] for x in section_nos]
        size=len(courselist)
        # for i in range(size):
        #     str(courses[i])
        #     courses[i].replace("('","")
        #     courses[i].replace("',)", "")
        return render_template('checkInfo.html', email=passedEmail, name=data, age=age, gender=gender,
                                   major=major, street=street, zipcode=zipcode, courses=courselist, section_nos=sectionlist, size=size)
    return render_template('checkInfo.html')


@app.route('/courseInfo', methods=['POST', 'GET'])
def courseInfo():
    if request.method =="POST":
        passedcourse=request.form["hidden_value"]
        passedsection = request.form["hidden_value1"]
        connection = sql.connect('NittanyPath.db')
        cursor = connection.execute('SELECT * FROM Courses WHERE course_id = (?);', (passedcourse,))
        data = cursor.fetchall()
        cursor = connection.execute("SELECT teaching_team_id FROM Sections where course_id = ? and sec_no = ?",(passedcourse,(passedsection)))
        teachingid = cursor.fetchall()[0][0]
        cursor = connection.execute('SELECT prof_email FROM Prof_teaching_teams WHERE teaching_team_id = (?);', (teachingid,))
        ProfessorEmail = cursor.fetchall()[0][0]
        cursor = connection.execute('SELECT name FROM Professors WHERE email = (?);',(ProfessorEmail,))
        ProfessorName = cursor.fetchall()[0][0]
        cursor = connection.execute('SELECT office_address FROM Professors WHERE email = (?);', (ProfessorEmail,))
        ProfessorOffice = cursor.fetchall()[0][0]
        return render_template("courseInfo.html", course=passedcourse, courseName=data[0][1], courseDescription=data[0][2], dropDeadline=data[0][3], ProfessorEmail=ProfessorEmail, ProfessorName=ProfessorName, ProfessorOffice=ProfessorOffice)
    return render_template("courseInfo.html")


@app.route('/homeworkInfo', methods=['POST', 'GET'])
def homeworkInfo():
    hw_grade=[]
    hw_description=[]
    if request.method =="POST":
        passedemail = request.form["hidden_value"]
        passedcourse=request.form["hidden_value1"]
        passedsection = request.form["hidden_value2"]
        connection = sql.connect('NittanyPath.db')
        cursor = connection.execute("SELECT hw_no FROM Homeworks where  course_id = ? and sec_no = ?",( passedcourse,passedsection))
        hw_no = cursor.fetchall()
        hwList = [x[0] for x in hw_no]
        size=len(hwList)
        cursor = connection.execute("SELECT grade FROM Homework_grades where student_email = ? and course_id = ? and sec_no = ?",( passedemail, passedcourse, passedsection))
        hw_grade=cursor.fetchall()
        hwGradeList = [x[0] for x in hw_grade]
        cursor = connection.execute("SELECT hw_details FROM Homeworks where course_id = ? and sec_no = ? ",(passedcourse, passedsection))
        hw_description=cursor.fetchall()
        hwDesList = [x[0] for x in hw_description]
        return render_template("homeworkInfo.html", hw_no=hwList, hw_grade=hwGradeList,hw_description=hwDesList,size=size)
    return render_template("homeworkInfo.html")

@app.route('/examInfo', methods=['POST', 'GET'])
def examInfo():
    exam_grade=[]
    exam_description=[]
    if request.method =="POST":
        passedemail = request.form["hidden_value"]
        passedcourse=request.form["hidden_value1"]
        passedsection = request.form["hidden_value2"]
        connection = sql.connect('NittanyPath.db')
        cursor = connection.execute("SELECT exam_no FROM Exams where  and course_id = ? and sec_no = ?",( passedcourse,passedsection))
        exam_no = cursor.fetchall()
        examList = [x[0] for x in exam_no]
        size=len(examList)
        cursor = connection.execute("SELECT grade FROM Exam_grades where student_email = ? and course_id = ? and sec_no = ?",( passedemail, passedcourse, passedsection))
        exam_grade=cursor.fetchall()
        examGradeList = [x[0] for x in exam_grade]
        cursor = connection.execute("SELECT exam_details FROM Exams where course_id = ? and sec_no = ? ",(passedcourse, passedsection))
        exam_description=cursor.fetchall()
        examDesList = [x[0] for x in exam_description]

        return render_template("examInfo.html", exam_no=examList, exam_grade=examGradeList, exam_description=examDesList,size=size)
    return render_template("examInfo.html")


@app.route('/changePassword', methods=['POST', 'GET'])
def changePassword():
    message=''
    error=""
    passedemail=""
    if request.method == "POST":
        passedemail = request.form["hidden_value"]
        oldPassword = request.form["oldPassword"]
        newPassword = request.form["newPassword"]
        againPassword = request.form["againPassword"]
        if newPassword != againPassword:
            error = "two new password input does not match"
            return render_template("changePassword.html", message=message, error=error, email=passedemail)
        connection = sql.connect('NittanyPath.db')
        cursor = connection.execute("SELECT password FROM Students where email = ?;",(passedemail,))
        acutalpassword=cursor.fetchall()[0][0]
        if oldPassword != acutalpassword:
            error = "old password is not correct"
            return render_template("changePassword.html", message=message, error=error, email=passedemail)
        if oldPassword == newPassword:
            error="new password cannot be the same as the old password"
            return render_template("changePassword.html",message=message,error=error,email=passedemail)
        else:
            cursor = connection.execute("UPDATE Students SET password = ? WHERE email=? ", (newPassword,passedemail))
            connection.commit()
            message="Success"
            return render_template("changePassword.html",message=message,error=error,email=passedemail)
    return render_template("changePassword.html")

@app.route('/passwordHelper', methods=['POST','GET'])
def passwordHelper():
    if request.method == "POST":
        passedemail = request.form["hidden_value"]
        return render_template("changePassword.html", email=passedemail)

@app.route('/postHelper', methods=['POST','GET'])
def postHelper():
    courselist=[]
    if request.method == "POST":
        passedemail = request.form["hidden_value"]
        connection = sql.connect('NittanyPath.db')
        cursor = connection.execute("SELECT course_id FROM Enrolls WHERE student_email = ?", (passedemail,))
        courses=cursor.fetchall()
        courselist = [x[0] for x in courses]
        size = len(courselist)
        return render_template("postHelper.html", email = passedemail, courses=courselist,size=size)


@app.route('/createHomework', methods=['POST','GET'])
def createHomework():
    error=''
    if request.method == "POST":
        print("in post")
        intext=request.form["description"]
        email=request.form["email"]
        connection = sql.connect('NittanyPath.db')
        cursor = connection.execute("SELECT teaching_team_id FROM Prof_teaching_teams where  prof_email = ?",
                                    (email,))
        team=cursor.fetchall()[0][0]
        cursor = connection.execute("SELECT course_id FROM Sections where  teaching_team_id = ?",
                                    (team,))
        course=cursor.fetchall()[0][0]

        cursor = connection.execute("SELECT hw_no FROM Homeworks where  course_id = ?",
                                    (course,))
        hw_no = cursor.fetchall()
        size=len(hw_no)
        cursor = connection.execute("INSERT INTO Homeworks(course_id,sec_no,hw_no,hw_details) VALUES(?,?,?,?)", (course,1,size,intext))
        cursor = connection.execute("INSERT INTO Homeworks(course_id,sec_no,hw_no,hw_details) VALUES(?,?,?,?)",
                                    (course, 2, size , intext))
        connection.commit()

        return render_template("createHomework.html", error=error)
    else:
        return render_template("createHomework.html", error=error)


@app.route('/createExam', methods=['POST','GET'])
def createExam():
    error=''
    if request.method == "POST":
        print("in post")
        intext=request.form["description"]
        email=request.form["email"]
        connection = sql.connect('NittanyPath.db')
        cursor = connection.execute("SELECT teaching_team_id FROM Prof_teaching_teams where  prof_email = ?",
                                    (email,))
        team=cursor.fetchall()[0][0]
        cursor = connection.execute("SELECT course_id FROM Sections where  teaching_team_id = ?",
                                    (team,))
        course=cursor.fetchall()[0][0]

        cursor = connection.execute("SELECT exam_no FROM Exams where  course_id = ?",
                                    (course,))
        exam_no = cursor.fetchall()
        size=len(exam_no)
        cursor = connection.execute("INSERT INTO Exams(course_id,sec_no,exam_no,exam_details) VALUES(?,?,?,?)", (course,1,size,intext))
        cursor = connection.execute("INSERT INTO Exams(course_id,sec_no,exam_no,exam_details) VALUES(?,?,?,?)",
                                    (course, 2, size , intext))
        connection.commit()

        return render_template("createExam.html", error=error)
    else:
        return render_template("createExam.html", error=error)


@app.route('/assignment', methods=['POST','GET'])
def assignment():
    if request.method == "POST":
        course=request.form['hidden_value']
        connection = sql.connect('NittanyPath.db')
        cursor = connection.execute("SELECT * FROM Homework_grades where  course_id = ?",
                                    (course,))
        result=cursor.fetchall()

        cursor = connection.execute("SELECT * FROM exam_grades where  course_id = ?",
                                    (course,))
        result1 = cursor.fetchall()
        return render_template("assignment.html", result=result, result1=result1)
    return render_template("homeworkInfo.html")

@app.route('/submitScore', methods=['POST','GET'])
def submitScore():
    if request.method == "POST":
        connection = sql.connect('NittanyPath.db')
        email = request.form["email"]
        course = request.form['course']
        hw_no = request.form["hw_no"]
        grade = request.form["grade"]
        type = request.form["type"]
        if type =="exam":
            cursor = connection.execute("UPDATE Exam_grades SET grade = ? WHERE student_email=? and course_id=? and exam_no=? ", (grade, email, course, hw_no))
        elif type =="homework":
            cursor = connection.execute("UPDATE Homework_grades SET grade = ? WHERE student_email=? and course_id=? and hw_no=? ",
                                        (grade, email, course, hw_no))
        connection.commit()
        return render_template("submitScore.html")
    return render_template("submitScore.html")


@app.route('/dropHelper', methods=['POST','GET'])
def dropHelper():
    error='success'
    if request.method == "POST":
        course=request.form["hidden_value"]
        deadline = request.form["hidden_value1"]
        email = request.form["hidden_value2"]
        todaysDate = time.strftime("%m/%d/%Y")
        connection = sql.connect('NittanyPath.db')

        print(todaysDate[6:8])
        print(deadline[6:8])
        if(int(todaysDate[6:8])>int(deadline[6:8])):
            error="too late to drop"
            return render_template("dropHelper.html",error=error)
        else:
            cursor = connection.execute('DELETE FROM Enrolls  WHERE student_email = (?) and course_id=?;', (email,course))
            cursor = connection.execute('DELETE FROM Homework_grades  WHERE student_email = (?) and course_id=?;',
                                        (email, course))
            cursor = connection.execute('DELETE FROM Exam_grades  WHERE student_email = (?) and course_id=?;',
                                        (email, course))
            connection.commit()
            return render_template("dropHelper.html", error=error)


@app.route('/dropCourse', methods=['POST','GET'])
def dropCourse():
    deadline=[]
    if request.method == "POST":
        connection = sql.connect('NittanyPath.db')
        email=request.form["hidden_value1"]
        cursor = connection.execute('SELECT course_id FROM Enrolls WHERE student_email = (?);', (email,))
        courses = cursor.fetchall()
        courselist = [x[0] for x in courses]
        size=len(courselist)
        for i in courselist:
            cursor = connection.execute('SELECT late_drop_deadline FROM Courses WHERE course_id = (?);', (i,))
            deadline.append(cursor.fetchall()[0][0])
        print(courselist,deadline)
    return render_template("dropCourse.html",courselist=courselist, deadline=deadline, email=email,size=size)


@app.route('/assignmentHelper', methods=['POST','GET'])
def assignmentHelper():
    courselist = []
    if request.method == "POST":
        passedemail = request.form["hidden_value"]
        connection = sql.connect('NittanyPath.db')
        cursor = connection.execute("SELECT teaching_team_id FROM Prof_teaching_teams WHERE prof_email = ?", (passedemail,))
        team=cursor.fetchall()[0][0]
        cursor = connection.execute("SELECT course_id FROM Sections WHERE teaching_team_id = ?", (team,))
        course = cursor.fetchall()[0][0]
        return render_template("assignmentHelper.html", email=passedemail, courses=course)


@app.route('/FpostHelper', methods=['POST','GET'])
def FpostHelper():
    courselist = []
    if request.method == "POST":
        passedemail = request.form["hidden_value"]
        connection = sql.connect('NittanyPath.db')
        cursor = connection.execute("SELECT teaching_team_id FROM Prof_teaching_teams WHERE prof_email = ?", (passedemail,))
        team=cursor.fetchall()[0][0]
        cursor = connection.execute("SELECT course_id FROM Sections WHERE teaching_team_id = ?", (team,))
        courses = cursor.fetchall()
        courselist = [x[0] for x in courses]
        size = len(courselist)
        return render_template("postHelper.html", email=passedemail, courses=courselist, size=size)

@app.route('/forumHelper', methods=['POST','GET'])
def forumHelper():
    if request.method == 'POST':
        intext=request.form["yourPost"]
        courseName =request.form["hidden_value1"]
        email=request.form["hidden_value6"]
        index=request.form["hidden_value"]
        connection = sql.connect('NittanyPath.db')
        studentName = []
        comment_no = []
        cursor = connection.execute("SELECT post_no FROM Posts WHERE course_id = ?", (courseName,))
        Posts_no = cursor.fetchall()
        cursor = connection.execute("INSERT INTO Posts(course_id,post_no,student_email,post_info ) VALUES(?,?,?,?)",
                                    (courseName, len(Posts_no) + 1, email, intext))
        connection.commit()
        cursor = connection.execute("SELECT student_email FROM Posts WHERE course_id = ?", (courseName,))
        student_email = cursor.fetchall()
        cursor = connection.execute("SELECT post_info FROM Posts WHERE course_id = ?", (courseName,))
        Posts = cursor.fetchall()
        emailList = [x[0] for x in student_email]
        for i in emailList:
            cursor = connection.execute("SELECT name FROM name WHERE email = ?", (i,))
            name = cursor.fetchall()[0][0]
            studentName.append(name)
        size = len(Posts_no)
        Posts_noList = [x[0] for x in Posts_no]
        PostsList = [x[0] for x in Posts]

        for j in Posts_noList:
            cursor = connection.execute("SELECT comment_no FROM Comments WHERE Post_no = ? and course_id = ?",
                                        (j, courseName))
            comment_no.append(len(cursor.fetchall()))





        return render_template("Forum.html", studentName=studentName, course=courseName,
                               Posts_no=Posts_noList, size=size, Posts=PostsList, comment_no=comment_no, email=email
                               )
    return render_template("Forum.html")


@app.route('/Forum', methods=['POST','GET'])
def Forum():
    submitted=False
    if request.method == "POST":
        courseName=request.form["hidden_value"]
        connection = sql.connect('NittanyPath.db')
        email = request.form["hidden_value1"]
        studentName=[]
        comment_no=[]
        cursor = connection.execute("SELECT post_no FROM Posts WHERE course_id = ?", (courseName,))
        Posts_no=cursor.fetchall()
        cursor = connection.execute("SELECT student_email FROM Posts WHERE course_id = ?", (courseName,))
        student_email = cursor.fetchall()
        cursor = connection.execute("SELECT post_info FROM Posts WHERE course_id = ?", (courseName,))
        Posts = cursor.fetchall()
        emailList = [x[0] for x in student_email]
        for i in emailList:
            cursor = connection.execute("SELECT name FROM name WHERE email = ?", (i,))
            name = cursor.fetchall()[0][0]
            studentName.append(name)
        size=len(Posts_no)
        Posts_noList = [x[0] for x in Posts_no]
        PostsList = [x[0] for x in Posts]

        for j in Posts_noList:
            cursor = connection.execute("SELECT comment_no FROM Comments WHERE Post_no = ? and course_id = ?", (j,courseName))
            comment_no.append(len(cursor.fetchall()))
        return render_template("Forum.html", studentName=studentName, course=courseName,
                               Posts_no=Posts_noList, size=size, Posts=PostsList, comment_no=comment_no,email=email, submitted=submitted)

@app.route('/viewComments', methods=['POST','GET'])
def viewComments():
    student_email = []
    studentName=[]
    if request.method == 'POST':
        post_no=request.form["hidden_value"]
        course=request.form["hidden_value1"]
        email=request.form["hidden_value2"]

        connection = sql.connect('NittanyPath.db')
        cursor = connection.execute("SELECT comment_no FROM Comments WHERE course_id = ? and post_no = ?", (course,post_no))
        comment_no = cursor.fetchall()
        cursor = connection.execute("SELECT student_email FROM Comments WHERE course_id = ? and post_no = ?", (course,post_no))
        student_email = cursor.fetchall()
        cursor = connection.execute("SELECT comment_info FROM Comments WHERE course_id = ? and post_no = ?",(course, post_no))
        comment = cursor.fetchall()

        emailList = [x[0] for x in student_email]
        for i in emailList:
            cursor = connection.execute("SELECT name FROM name  WHERE email = ?", (i,))
            name = cursor.fetchall()[0][0]
            studentName.append(name)
        size = len(comment_no)
        comment_noList = [x[0] for x in comment_no]
        commentList = [x[0] for x in comment]

        return render_template("Comments.html", studentName=studentName, course=course,
                        Post_no=post_no, size=size, comments=commentList, comment_no=comment_noList,email=email)


@app.route('/commentHelper', methods=['POST','GET'])
def commentHelper():
    student_email = []
    studentName=[]
    if request.method == 'POST':
        post_no=request.form["hidden_value"]
        course=request.form["hidden_value1"]
        email=request.form["hidden_value6"]
        intext = request.form["yourComment"]
        connection = sql.connect('NittanyPath.db')
        cursor = connection.execute("SELECT comment_no FROM Comments WHERE course_id = ? and post_no = ?", (course,post_no))
        comment_no = cursor.fetchall()
        cursor = connection.execute("SELECT student_email FROM Comments WHERE course_id = ? and post_no = ?", (course,post_no))
        student_email = cursor.fetchall()
        cursor = connection.execute("SELECT comment_info FROM Comments WHERE course_id = ? and post_no = ?",(course, post_no))
        comment = cursor.fetchall()
        cursor = connection.execute("INSERT INTO Comments(course_id,post_no,comment_no,student_email,comment_info ) VALUES(?,?,?,?,?)",
                                    (course, post_no, len(comment_no)+ 1, email, intext))

        emailList = [x[0] for x in student_email]
        for i in emailList:
            cursor = connection.execute("SELECT name FROM name  WHERE email = ?", (i,))
            name = cursor.fetchall()[0][0]
            studentName.append(name)
        size = len(comment_no)
        comment_noList = [x[0] for x in comment_no]
        commentList = [x[0] for x in comment]
        connection.commit()
        return render_template("Comments.html", studentName=studentName, course=course,
                        Post_no=post_no, size=size, comments=commentList, comment_no=comment_noList,email=email)


def delete_name(first_name, last_name):
    connection = sql.connect('dataset.db')
    connection.execute('DELETE FROM users WHERE firstname=? and lastname=?', (first_name,last_name))
    connection.commit()
    cursor = connection.execute('SELECT * FROM users;')
    return cursor.fetchall()


def add_name(email, course, ):
    connection = sql.connect('dataset.db')
    connection.execute('CREATE TABLE IF NOT EXISTS users(pid integer PRIMARY KEY, firstname TEXT, lastname TEXT);')
    connection.execute('INSERT INTO users ( firstname, lastname) VALUES (?,?);', ( first_name, last_name))
    connection.commit()
    cursor = connection.execute('SELECT * FROM users;')
    return cursor.fetchall()




if __name__ == "__main__":
    app.run()



