from flask import Flask, render_template, request, abort, jsonify, redirect, url_for
import pymysql

app = Flask(__name__)

conn = pymysql.connect(host="localhost", user="tms", passwd="tse2101", db="trainingmanagement")


@app.route('/')
def firstpage():
    return render_template("tms_home.html")


@app.route('/', methods=['POST'])
def main():

    selection = request.form['button']
    print(selection)
    if request.form['button'] == 'Login':

        username = request.form['username']
        psw = request.form['psw']

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM account WHERE account.accID = %s AND account.accPassword = %s", (username, psw))
        account = cursor.fetchone()

        if account:
            print(username)
            cursor2 = conn.cursor()
            cursor2.execute("SELECT account.accType FROM account WHERE account.accID = %s", (username))
            accountType = cursor2.fetchone()
            print(accountType)
            if accountType == ('trainee',):
                return render_template("Trainee/Trainee_Home.html")

            elif accountType == ('trainer',):
                return render_template("Trainer/Trainer_Home.html")

            elif accountType == ('admin',):
                return render_template("Admin/Admin_Home.html")

        else:
            error = "Incorrect Username or Password, Please Try Again."
            return render_template("tms_home.html", error=error)

    elif request.form['button'] == 'Register':

        accountType = request.form['accountType']
        username = request.form['username']
        nickname = request.form['nickname']
        email = request.form['email']
        psw = request.form['psw']

        cursor3 = conn.cursor()

        if accountType == 'trainee':
            cursor3.execute(
                "INSERT INTO account (accID, accType, accName, accPassword, accEmail) VALUES (%s,%s,%s,%s,%s)",
                (username, accountType, nickname, psw, email))
            cursor3.execute("INSERT INTO trainee (accID, traineeID, traineeName) VALUES (%s,%s,%s)",
                            (username, username, nickname))

            conn.commit()

            return render_template("Trainee/Trainee_Home.html")

        else:
            cursor3.execute(
                "INSERT INTO account (accID, accType, accName, accPassword, accEmail) VALUES (%s,%s,%s,%s,%s)",
                (username, accountType, nickname, psw, email))
            cursor3.execute("INSERT INTO trainer (accID, trainerID, trainerName) VALUES (%s,%s,%s)",
                            (username, username, nickname))

            conn.commit()

            return render_template("Trainer/Trainer_Home.html")


@app.route('/Trainer_Home.html')
def trainerhome():
    return render_template("Trainer/Trainer_Home.html")


@app.route('/Trainer_MyCourse.html')
def trainermycourses():
    c = [" ", " ", " "]

    cursor4 = conn.cursor()
    cursor4.execute("SELECT course.courseName FROM course WHERE course.trainerID = 'leeguangshen'")
    course = cursor4.fetchall()
    print(course)
    for x in range(len(course)):
        c[x] = course[x]

    return render_template("Trainer/Trainer_MyCourse.html", c1=c[0], c2=c[1], c3=c[2])


@app.route('/Trainer_AddCourse.html')
def trainerAddCourse():
    return render_template('Trainer/Trainer_AddCourse.html')


@app.route('/AddCourse', methods=['POST'])
def traineraddcourse():

    if request.form['button'] == 'submit':
        trainerID = request.form['trainerID']
        courseID = request.form['courseID']
        courseName = request.form['courseName']

        cursor5 = conn.cursor()
        cursor5.execute(
            "INSERT INTO course (trainerID, courseID, courseName) VALUES (%s,%s,%s)", (trainerID, courseID, courseName))

        conn.commit()

        return redirect(url_for('trainermycourses'))


@app.route('/Trainer_CourseDetails.html')
def trainercoursedetails():
    return render_template('Trainer/Trainer_CourseDetails.html')


@app.route('/Trainer_CourseDetails2.html')
def trainercoursedetails2():
    return render_template('Trainer/Trainer_CourseDetails2.html')


@app.route('/Trainer_UserFeedback_SEF.html')
def userfeedbacksef():
    cursor12 = conn.cursor()
    cursor12.execute("SELECT courseName FROM feedback")

    course = cursor12.fetchall()

    for j in range(len(course)):
        if course[j] == ('Software Engineering Fundamentals',):
            s = [" ", " ", " ", " ", " ", " "]
            f = [" ", " ", " ", " ", " ", " "]

            cursor13 = conn.cursor()
            cursor13.execute("SELECT traineeID FROM feedback WHERE courseName = 'Software Engineering Fundamentals'")

            trainee = cursor13.fetchall()

            for i in range(len(trainee)):
                s[i] = trainee[i]

            cursor14 = conn.cursor()
            cursor14.execute("SELECT feedbackContent FROM feedback WHERE courseName = 'Software Engineering Fundamentals'")

            feedback = cursor14.fetchall()

            for i in range(len(feedback)):
                f[i] = feedback[i]

            return render_template('Trainer/Trainer_UserFeedback_SEF.html', s1=s[0], s2=s[1], s3=s[2], s4=s[3], s5=s[4], s6=s[5], f1=f[0], f2=f[1], f3=f[2], f4=f[3], f5=f[4], f6=f[5])


@app.route('/Trainer_UserFeedback_OOAD.html')
def userfeedbackooad():
    cursor15 = conn.cursor()
    cursor15.execute("SELECT courseName FROM feedback")

    course = cursor15.fetchall()

    for j in range(len(course)):
        if course[j] == ('Object-Oriented Analysis and Design',):
            s = [" ", " ", " ", " ", " ", " "]
            f = [" ", " ", " ", " ", " ", " "]

            cursor16 = conn.cursor()
            cursor16.execute("SELECT traineeID FROM feedback WHERE courseName = 'Object-Oriented Analysis and Design'")

            trainee = cursor16.fetchall()

            for i in range(len(trainee)):
                s[i] = trainee[i]

            cursor17 = conn.cursor()
            cursor17.execute("SELECT feedbackContent FROM feedback WHERE courseName = 'Object-Oriented Analysis and Design'")

            feedback = cursor17.fetchall()

            for i in range(len(feedback)):
                f[i] = feedback[i]

            return render_template('Trainer/Trainer_UserFeedback_OOAD.html', s1=s[0], s2=s[1], s3=s[2], s4=s[3], s5=s[4], s6=s[5], f1=f[0], f2=f[1], f3=f[2], f4=f[3], f5=f[4], f6=f[5])


@app.route('/Trainer_UserFeedback_OS.html')
def userfeedbackos():
    return render_template('Trainer/Trainer_UserFeedback_OS.html')


@app.route('/Trainer_Upload_CourseMaterial.html')
def uploadCourseMaterial():
    return render_template('Trainer/Trainer_Upload_CourseMaterial2.html')


@app.route('/AddMaterials', methods=['POST'])
def uploadcoursematerial():

    if request.form['button'] == 'submit':
        courseName = request.form['courseName']
        materialID = request.form['materialID']
        materialName = request.form['materialName']
        materialContent = request.form['materialContent']

        cursor40 = conn.cursor()
        cursor40.execute(
            "INSERT INTO Training_Materials (courseName, materialID, materialName, materialContent) VALUES (%s,%s,%s,%s)", (courseName, materialID, materialName, materialContent))

        conn.commit()

        return redirect(url_for('trainercoursedetails'))


@app.route('/Trainer_Upload_CourseMaterial2.html')
def uploadCourseMaterial2():
    return render_template('Trainer/Trainer_Upload_CourseMaterial2.html')


@app.route('/AddMaterials2', methods=['POST'])
def uploadcoursematerial2():

    if request.form['button'] == 'submit':
        courseName = request.form['courseName']
        materialID = request.form['materialID']
        materialName = request.form['materialName']
        materialContent = request.form['materialContent']

        cursor41 = conn.cursor()
        cursor41.execute(
            "INSERT INTO Training_Materials (courseName, materialID, materialName, materialContent) VALUES (%s,%s,%s,%s)", (courseName, materialID, materialName, materialContent))

        conn.commit()

        return redirect(url_for('trainercoursedetails2'))


#########################################################################


@app.route('/Trainee_Home.html')
def traineehome():
    return render_template("Trainee/Trainee_Home.html")


@app.route('/Trainee_Courses.html')
def traineecourses():
    return render_template("Trainee/Trainee_Courses.html")


@app.route('/Trainee_MyCourse.html')
def traineemycourse():
    return render_template("Trainee/Trainee_MyCourse.html")


@app.route('/Trainee_CourseDetails_SEF.html')
def traineecoursedetailsSEF():
    return render_template('Trainee/Trainee_CourseDetails_SEF.html')


@app.route('/Trainee_CourseDetails_OOAD.html')
def traineecoursedetailsOOAD():
    return render_template('Trainee/Trainee_CourseDetails_OOAD.html')


@app.route('/Trainee_CourseDetails_OS.html')
def traineecoursedetailsOS():
    return render_template('Trainee/Trainee_CourseDetails_OS.html')


@app.route('/Trainee_Userfeedback_SEF.html')
def traineefeedbacksef():
    cursor18 = conn.cursor()
    cursor18.execute("SELECT courseName FROM feedback")

    course = cursor18.fetchall()

    t = [" ", " ", " "]
    f = [" ", " ", " "]

    for j in range(len(course)):
        if course[j] == ('Software Engineering Fundamentals',):
            print("ABC")
            cursor19 = conn.cursor()
            cursor19.execute("SELECT feedbackTitle FROM feedback WHERE courseName = 'Software Engineering Fundamentals'")

            title = cursor19.fetchall()

            for i in range(len(title)):
                t[i] = title[i]
                print(t[i])
            cursor20 = conn.cursor()
            cursor20.execute("SELECT feedbackContent FROM feedback WHERE courseName = 'Software Engineering Fundamentals'")

            feedback = cursor20.fetchall()

            for i in range(len(feedback)):
                f[i] = feedback[i]
                print(f[i])
            return render_template('Trainee/Trainee_Userfeedback_SEF.html', t1=title[0], t2=title[1], f1=feedback[0], f2=feedback[1])


@app.route('/Trainee_Userfeedback_OOAD.html')
def traineefeedbackooad():
    cursor21 = conn.cursor()
    cursor21.execute("SELECT courseName FROM feedback")

    course = cursor21.fetchall()

    t = [" ", " ", " "]
    f = [" ", " ", " "]

    for j in range(len(course)):
        if course[j] == ('Object-Oriented Analysis and Design',):

            cursor22 = conn.cursor()
            cursor22.execute("SELECT feedbackTitle FROM feedback WHERE courseName = 'Object-Oriented Analysis and Design'")

            title = cursor22.fetchall()

            for i in range(len(title)):
                t[i] = title[i]

            cursor23 = conn.cursor()
            cursor23.execute("SELECT feedbackContent FROM feedback WHERE courseName = 'Object-Oriented Analysis and Design'")

            feedback = cursor23.fetchall()

            for i in range(len(feedback)):
                f[i] = feedback[i]

            return render_template('Trainee/Trainee_Userfeedback_OOAD.html', t1=title[0], t2=title[1], f1=feedback[0], f2=feedback[1])


@app.route('/Trainee_Userfeedback_OS.html')
def traineefeedbackos():
    return render_template('Trainee/Trainee_Userfeedback_OS.html')


@app.route('/Trainee_GiveUserfeedback.html')
def traineegiveuserfeedback():
    return render_template('Trainee/Trainee_GiveUserfeedback.html')


@app.route('/GiveFeedback', methods=['POST'])
def traineeGiveUserFeedback():

    if request.form['button'] == 'submit':
        traineeID = request.form['traineeID']
        courseName = request.form['courseName']
        feedbackID = request.form['feedbackID']
        feedbackTitle = request.form['feedbackTitle']
        feedbackContent = request.form['feedbackContent']

        cursor27 = conn.cursor()
        cursor27.execute(
            "INSERT INTO feedback (traineeID, courseName, feedbackID, feedbackTitle, feedbackContent) VALUES (%s,%s,%s,%s,%s)", (traineeID, courseName, feedbackID, feedbackTitle, feedbackContent))

        conn.commit()

        return redirect(url_for('traineemycourse'))


@app.route('/Trainee_View_TrainingMaterials_SEF.html')
def traineeviewtrainingmaterialssef():
    cursor42 = conn.cursor()
    cursor42.execute("SELECT courseName FROM training_materials")

    course = cursor42.fetchone()

    if course:
        t = [" ", " ", " ", " ", " ", " "]
        c = [" ", " ", " ", " ", " ", " "]

        cursor43 = conn.cursor()
        cursor43.execute("SELECT materialName FROM training_materials WHERE courseName = 'Software Engineering Fundamentals'")

        material = cursor43.fetchall()

        for i in range(len(material)):
            t[i] = material[i]

        cursor44 = conn.cursor()
        cursor44.execute("SELECT materialContent FROM training_materials WHERE courseName = 'Software Engineering Fundamentals'")

        content = cursor44.fetchall()

        for i in range(len(content)):
            c[i] = content[i]

        return render_template('Trainee/Trainee_View_TrainingMaterials_SEF.html', t1=t[0], t2=t[1], t3=t[2], t4=t[3], c1=c[0], c2=c[1], c3=c[2], c4=c[3])


@app.route('/Trainee_View_TrainingMaterials_OOAD.html')
def traineeviewtrainingmaterialsooad():
    cursor45 = conn.cursor()
    cursor45.execute("SELECT courseName FROM training_materials")

    course = cursor45.fetchone()

    if course:
        t = [" ", " ", " ", " ", " ", " "]
        c = [" ", " ", " ", " ", " ", " "]

        cursor46 = conn.cursor()
        cursor46.execute("SELECT materialName FROM training_materials WHERE courseName = 'Object-Oriented Analysis and Design'")

        material = cursor46.fetchall()

        for i in range(len(material)):
            t[i] = material[i]

        cursor47 = conn.cursor()
        cursor47.execute("SELECT materialContent FROM training_materials WHERE courseName = 'Object-Oriented Analysis and Design'")

        content = cursor47.fetchall()

        for i in range(len(content)):
            c[i] = content[i]

        return render_template('Trainee/Trainee_View_TrainingMaterials_OOAD.html', t1=t[0], t2=t[1], t3=t[2], t4=t[3], c1=c[0], c2=c[1], c3=c[2], c4=c[3])


@app.route('/Trainee_View_TrainingMaterials_OS.html')
def traineeviewtrainingmaterialsos():
    cursor48 = conn.cursor()
    cursor48.execute("SELECT courseName FROM training_materials")

    course = cursor48.fetchone()

    if course:
        t = [" ", " ", " ", " ", " ", " "]
        c = [" ", " ", " ", " ", " ", " "]

        cursor49 = conn.cursor()
        cursor49.execute("SELECT materialName FROM training_materials WHERE courseName = 'Operating System'")

        material = cursor49.fetchall()

        for i in range(len(material)):
            t[i] = material[i]

        cursor50 = conn.cursor()
        cursor50.execute("SELECT materialContent FROM training_materials WHERE courseName = 'Operating System'")

        content = cursor50.fetchall()

        for i in range(len(content)):
            c[i] = content[i]

        return render_template('Trainee/Trainee_View_TrainingMaterials_OS.html', t1=t[0], t2=t[1], t3=t[2], t4=t[3], c1=c[0], c2=c[1], c3=c[2], c4=c[3])


##########################################################################################


@app.route('/Admin_Home.html')
def adminhome():
    return render_template("Admin/Admin_Home.html")


@app.route('/Admin_Courses.html')
def admincourses():
    return render_template("Admin/Admin_Courses.html")


@app.route('/Admin_Materials_SEF.html')
def admin_material_SEF():
    return render_template('Admin/Admin_Materials_SEF.html')


@app.route('/Admin_Materials_OOAD.html')
def admin_material_OOAD():
    return render_template('Admin/Admin_Materials_OOAD.html')


@app.route('/Admin_UserFeedback_SEF.html')
def admin_user_feedback_SEF():
    cursor34 = conn.cursor()
    cursor34.execute("SELECT courseName FROM feedback")

    course = cursor34.fetchall()

    for j in range(len(course)):
        if course[j] == ('Software Engineering Fundamentals',):
            t = [" ", " ", " ", " ", " ", " ", " "]
            f = [" ", " ", " ", " ", " ", " ", " "]

            cursor35 = conn.cursor()
            cursor35.execute("SELECT feedbackTitle FROM feedback WHERE courseName = 'Software Engineering Fundamentals'")

            title = cursor35.fetchall()

            for i in range(len(title)):
                t[i] = title[i]

            cursor36 = conn.cursor()
            cursor36.execute("SELECT feedbackContent FROM feedback WHERE courseName = 'Software Engineering Fundamentals'")

            feedback = cursor36.fetchall()

            for i in range(len(feedback)):
                f[i] = feedback[i]

            return render_template('Admin/Admin_UserFeedback_SEF.html', t1=t[0], t2=t[1], t3=t[2], t4=t[3], t5=t[4], t6=t[5], t7=t[6], f1=f[0], f2=f[1], f3=f[2], f4=f[3], f5=f[4], f6=f[5], f7=f[6])


@app.route('/Admin_UserFeedback_OOAD.html')
def admin_user_feedback_OOAD():
    cursor37 = conn.cursor()
    cursor37.execute("SELECT courseName FROM feedback")

    course = cursor37.fetchall()

    for j in range(len(course)):
        if course[j] == ('Object-Oriented Analysis and Design',):
            t = [" ", " ", " ", " ", " ", " ", " "]
            f = [" ", " ", " ", " ", " ", " ", " "]

            cursor38 = conn.cursor()
            cursor38.execute("SELECT feedbackTitle FROM feedback WHERE courseName = 'Object-Oriented Analysis and Design'")

            title = cursor38.fetchall()

            for i in range(len(title)):
                t[i] = title[i]

            cursor39 = conn.cursor()
            cursor39.execute("SELECT feedbackContent FROM feedback WHERE courseName = 'Object-Oriented Analysis and Design'")

            feedback = cursor39.fetchall()

            for i in range(len(feedback)):
                f[i] = feedback[i]

            return render_template('Admin/Admin_UserFeedback_OOAD.html', t1=t[0], t2=t[1], t3=t[2], t4=t[3], t5=t[4], t6=t[5], t7=t[6], f1=f[0], f2=f[1], f3=f[2], f4=f[3], f5=f[4], f6=f[5], f7=f[6])


@app.route('/Admin_UserFeedback_OS.html')
def admin_user_feedback_OS():
    cursor60 = conn.cursor()
    cursor60.execute("SELECT courseName FROM feedback")

    course = cursor60.fetchall()

    for j in range(len(course)):
        if course[j] == ('Operating System',):
            t = [" ", " ", " ", " ", " ", " ", " "]
            f = [" ", " ", " ", " ", " ", " ", " "]

            cursor61 = conn.cursor()
            cursor61.execute("SELECT feedbackTitle FROM feedback WHERE courseName = 'Operating System'")

            title = cursor61.fetchall()

            for i in range(len(title)):
                t[i] = title[i]

            cursor62 = conn.cursor()
            cursor62.execute("SELECT feedbackContent FROM feedback WHERE courseName = 'Operating System'")

            feedback = cursor62.fetchall()

            for i in range(len(feedback)):
                f[i] = feedback[i]

            return render_template('Admin/Admin_UserFeedback_OS.html', t1=t[0], t2=t[1], t3=t[2], t4=t[3], t5=t[4], t6=t[5], t7=t[6], f1=f[0], f2=f[1], f3=f[2], f4=f[3], f5=f[4], f6=f[5], f7=f[6])


##### Mang Fish #####


@app.route('/Admin_View_TrainingMaterials_SEF.html')
def adminviewtrainingmaterialssef():
    cursor51 = conn.cursor()
    cursor51.execute("SELECT courseName FROM training_materials")

    course = cursor51.fetchone()

    if course:
        t = [" ", " ", " ", " ", " ", " "]
        c = [" ", " ", " ", " ", " ", " "]

        cursor52 = conn.cursor()
        cursor52.execute("SELECT materialName FROM training_materials WHERE courseName = 'Software Engineering Fundamentals'")

        material = cursor52.fetchall()

        for i in range(len(material)):
            t[i] = material[i]

        cursor53 = conn.cursor()
        cursor53.execute("SELECT materialContent FROM training_materials WHERE courseName = 'Software Engineering Fundamentals'")

        content = cursor53.fetchall()

        for i in range(len(content)):
            c[i] = content[i]

        return render_template('Admin/Admin_View_TrainingMaterials_SEF.html', t1=t[0], t2=t[1], t3=t[2], t4=t[3], c1=c[0], c2=c[1], c3=c[2], c4=c[3])



@app.route('/Admin_View_TrainingMaterials_OOAD.html')
def adminviewtrainingmaterialsooad():
    cursor54 = conn.cursor()
    cursor54.execute("SELECT courseName FROM training_materials")

    course = cursor54.fetchone()

    if course:
        t = [" ", " ", " ", " ", " ", " "]
        c = [" ", " ", " ", " ", " ", " "]

        cursor55 = conn.cursor()
        cursor55.execute("SELECT materialName FROM training_materials WHERE courseName = 'Object-Oriented Analysis and Design'")

        material = cursor55.fetchall()

        for i in range(len(material)):
            t[i] = material[i]

        cursor56 = conn.cursor()
        cursor56.execute("SELECT materialContent FROM training_materials WHERE courseName = 'Object-Oriented Analysis and Design'")

        content = cursor56.fetchall()

        for i in range(len(content)):
            c[i] = content[i]

        return render_template('Admin/Admin_View_TrainingMaterials_OOAD.html', t1=t[0], t2=t[1], t3=t[2], t4=t[3], c1=c[0], c2=c[1], c3=c[2], c4=c[3])


@app.route('/Admin_View_TrainingMaterials_OS.html')
def adminviewtrainingmaterialsos():
    cursor57 = conn.cursor()
    cursor57.execute("SELECT courseName FROM training_materials")

    course = cursor57.fetchone()

    if course:
        t = [" ", " ", " ", " ", " ", " "]
        c = [" ", " ", " ", " ", " ", " "]

        cursor58 = conn.cursor()
        cursor58.execute("SELECT materialName FROM training_materials WHERE courseName = 'Operating System'")

        material = cursor58.fetchall()

        for i in range(len(material)):
            t[i] = material[i]

        cursor59 = conn.cursor()
        cursor59.execute("SELECT materialContent FROM training_materials WHERE courseName = 'Operating System'")

        content = cursor59.fetchall()

        for i in range(len(content)):
            c[i] = content[i]

        return render_template('Admin/Admin_View_TrainingMaterials_OS.html', t1=t[0], t2=t[1], t3=t[2], t4=t[3], c1=c[0], c2=c[1], c3=c[2], c4=c[3])


if __name__ == "__main__":
    app.run(debug=True)
