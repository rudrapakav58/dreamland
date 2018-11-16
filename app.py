from flask import Flask, render_template, request,flash,redirect
import psycopg2
app = Flask(__name__)
# db = psycopg2.connect(
#     database = "Dreamland",
#     user = "postgres",
#     password = "1234",
#     host = "localhost"
# )
# print(db)
@app.route('/', methods = ['GET','POST'])
def index():
        try:
            result = request.form.to_dict()
            #print(result)

        except:
            pass
        try:
            if result=={}:
                return render_template('index.html')
            elif result['password'] != result['c_password']:
                msg="Passwords do not match"
                return render_template('reg_user.html',msg=msg)
            elif result['password'] == result['c_password']:
                #print(result['first_name'])
                db = psycopg2.connect(
                                    database = "dcore2hl3fm13v",
                                    user = "pnevkxlqdlmdif",
                                    password = "4d4a6fea5afacaab6d2e7372233725045c0b183e96925dec212ddf0ac468cdc1",
                                    host = "ec2-174-129-192-200.compute-1.amazonaws.com"
                                )
                #print(db)
                cur = db.cursor()
                cur.execute(
                    "INSERT INTO test_user1 (First_name,Last_name,Email,Password,Dob,Gender) VALUES ('{}','{}','{}','{}',{},'{}')".format(
                        result['first_name'], result['last_name'], result['mail'], result['password'],
                        result['datetimepicker'],
                        result['gender']))
                db.commit()
                #print(" user info created successfully")
                db.close()
                msg="You Are Now A Registered User!"
                return render_template('reg_user.html',msg=msg)
        except:
            pass
@app.route('/login',methods=['GET', 'POST'])
def Login():
    try:
        result = request.form.to_dict()
        email = result['mail']
        password = result['password']
        db = psycopg2.connect(
                                database = "dcore2hl3fm13v",
                                user = "pnevkxlqdlmdif",
                                password = "4d4a6fea5afacaab6d2e7372233725045c0b183e96925dec212ddf0ac468cdc1",
                                host = "ec2-174-129-192-200.compute-1.amazonaws.com"
                            )
        cur = db.cursor()
        cur.execute("SELECT email,password FROM test_user1 where email='{}'".format(email))
        mail_user = cur.fetchone()
        if mail_user == None:
            msg = "Username is incorrect."
            return render_template('login.html', msg=msg)

        elif str(email) == mail_user[0]:
            cur.execute("SELECT password From test_user1 where email='{}'".format(email))
            password_user = cur.fetchone()
            if password_user[0] == password:
                msg = "You are logged in"
                return render_template('homepage.html', msg=msg)
            else:
                msg = "Password is incorrect."
                return render_template('login.html', msg=msg)
        else:
            msg = "Username is incorrect."
            return render_template('login.html', msg=msg)

        db.commit()
        db.close()
    except:
        pass


# @app.route('/reg', methods=['POST'])
# def user_reg():
#     print("In create")
#     error = False
#     result = request.form.to_dict()
#     print(result)
#     if result['password'] != result['c_password']:
#         flash('Passwords do not match')
#         return redirect('/reg')
#     if result['password'] == result['c_password']:
#         print(result['first_name'])
#         db = psycopg2.connect(
#             database="dcore2hl3fm13v",
#             user="pnevkxlqdlmdif",
#             password="4d4a6fea5afacaab6d2e7372233725045c0b183e96925dec212ddf0ac468cdc1",
#             host="ec2-174-129-192-200.compute-1.amazonaws.com"
#         )
#         cur = db.cursor()
#         cur.execute(
#             "INSERT INTO test_user (First_name,Last_name,Email,Password,Dob,Gender) VALUES ('{}','{}','{}','{}',{},'{}')".format(
#                 result['first_name'], result['last_name'], result['mail'], result['password'],
#                 result['datetimepicker'],
#                 result['gender']))
#         db.commit()
#         print("Records created successfully")
#         db.close()
#     else:
#         flash('You Are Now A Registered User!')
#         return redirect('/')
#     return render_template('landingpage.html')
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')