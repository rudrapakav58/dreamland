from flask import Flask, render_template, request,flash,redirect
import psycopg2
import base64
import smtplib
from email.mime.text import MIMEText
import random
import string

app = Flask(__name__)
# db = psycopg2.connect(
#     database = "Dreamland",
#     user = "postgres",
#     password = "1234",
#     host = "localhost"
# )
# print(db)
# db = psycopg2.connect(
#                 database="dcore2hl3fm13v",
#                 user="pnevkxlqdlmdif",
#                 password="4d4a6fea5afacaab6d2e7372233725045c0b183e96925dec212ddf0ac468cdc1",
#                 host="ec2-174-129-192-200.compute-1.amazonaws.com"
#             )
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
        except:
            pass
        try:
            mail_id=result['mail']
            db = psycopg2.connect(
                database="dcore2hl3fm13v",
                user="pnevkxlqdlmdif",
                password="4d4a6fea5afacaab6d2e7372233725045c0b183e96925dec212ddf0ac468cdc1",
                host="ec2-174-129-192-200.compute-1.amazonaws.com"
            )
            # print(db)
            # db = psycopg2.connect(
            #     database="Dreamland",
            #     user="postgres",
            #     password="1234",
            #     host="localhost"
            # )
            cur = db.cursor()
            cur.execute("SELECT email FROM test_user1 where email='{}'".format(mail_id))
            email_id = cur.fetchone()
            db.commit()
            # print(" user info created successfully")
            db.close()
            db_mailid=str(email_id)
            # print(type(db_mailid))
            # print(type(mail_id))
            if email_id==None:
                try:
                    # print(type(mail_id))
                    if result['password'] != result['c_password']:
                        # print(type(mail_id))
                        msg="Passwords do not match"
                        return render_template('reg_user.html',msg=msg)
                    elif result['password'] == result['c_password']:
                        # print(type(mail_id))
                        # print(result['first_name'])
                        db = psycopg2.connect(
                            database="dcore2hl3fm13v",
                            user="pnevkxlqdlmdif",
                            password="4d4a6fea5afacaab6d2e7372233725045c0b183e96925dec212ddf0ac468cdc1",
                            host="ec2-174-129-192-200.compute-1.amazonaws.com"
                        )
                        # db = psycopg2.connect(
                        #     database="Dreamland",
                        #     user="postgres",
                        #     password="1234",
                        #     host="localhost"
                        # )
                        enc = base64.b64encode(result['password'].encode())
                        enc = enc.decode()
                        cur = db.cursor()
                        cur.execute(
                            "INSERT INTO test_user1 (First_name,Last_name,Email,Password,Dob,Gender) VALUES ('{}','{}','{}','{}',0,0)".format(
                                result['first_name'], result['last_name'], result['mail'], enc))
                        db.commit()
                        #print(" user info created successfully")
                        db.close()
                        msg="You Are Now A Registered User!"
                        #return render_template('reg_user.html',msg=msg)
                        return redirect('/post')
                except:
                    pass
            else:
                # print(db_mailid)
                # print(mail_id)
                msg = "The email address you have entered is already registered!"
                #print(msg)
                return render_template('reg_user.html', msg=msg)

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
            enc = base64.b64encode(password.encode())
            enc = enc.decode()
            if password_user[0] == enc:
                msg = "You are logged in"
                #return render_template('homepage.html', msg=msg)
                return redirect('/post')
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

@app.route('/verify',methods=['GET', 'POST'])
def verify():
    try:
        result = request.form.to_dict()
        # print(result)
    except:
        pass
    try:
        result = request.form.to_dict()
        if result == {}:
            return render_template('forgot_password.html')
        else:
            db = psycopg2.connect(
                database="dcore2hl3fm13v",
                user="pnevkxlqdlmdif",
                password="4d4a6fea5afacaab6d2e7372233725045c0b183e96925dec212ddf0ac468cdc1",
                host="ec2-174-129-192-200.compute-1.amazonaws.com"
            )
            email = result['mail']
            cur = db.cursor()
            cur.execute("SELECT email,password FROM test_user1 where email='{}'".format(email))
            mail_user = cur.fetchone()
            if mail_user==None:
                msg = 'Incorrect mail ID'
                return render_template('forgot_password.html',msg=msg)
            else:
                charecters = string.ascii_letters + string.digits
                newPassword = random.choices(charecters, k=8)
                newPassword = (''.join(newPassword)).encode()
                enc = base64.b64encode(newPassword)
                enc = enc.decode()
                cur.execute("UPDATE test_user1 SET password = '{}' WHERE email = '{}';".format(str(enc),str(mail_user[0])))
                db.commit()
                db.close()
                msg = 'New Password sent to your mail'
                fromx = 'dreamland.textmail@gmail.com'
                to = str(mail_user[0])
                message = MIMEText("Your dreamland password is '{}'".format(str(newPassword.decode())))
                message['Subject'] = 'Dream Land Password'
                message['From'] = fromx
                message['To'] = to

                server = smtplib.SMTP('smtp.gmail.com:587')
                server.starttls()
                server.ehlo()
                server.login('dreamland.textmail@gmail.com', 'dreamland@12345')
                server.sendmail(fromx, to, message.as_string())
                server.quit()

                return render_template('login.html', msg=msg)
    except:
        pass
@app.route('/post',methods=['GET', 'POST'])
def post():
    try:
        result = request.form.to_dict()
        print(result)
        if result=={}:
            return render_template('dream_post.html')
        elif len(result['dream_type'])>1:
            dream=result['dream']
            import random
            for x in range(1):
                id1=random.randint(1, 100000)
            db = psycopg2.connect(
                database="dcore2hl3fm13v",
                user="pnevkxlqdlmdif",
                password="4d4a6fea5afacaab6d2e7372233725045c0b183e96925dec212ddf0ac468cdc1",
                host="ec2-174-129-192-200.compute-1.amazonaws.com"
            )
            # db = psycopg2.connect(
            #     database="Dreamland",
            #     user="postgres",
            #     password="1234",
            #     host="localhost"
            # )
            cur = db.cursor()
            cur.execute(
                "INSERT INTO user_dreams (id,user_name,date_post,dream) VALUES ('{}',0,0,'{}')".format(
                    id1,result['dream']))
            # dreams_user=cur.execute("SELECT dream From user_dreams")
            print(id1)
            db.commit()
            print(result['dream'])
            db.close()
            db = psycopg2.connect(
                database="dcore2hl3fm13v",
                user="pnevkxlqdlmdif",
                password="4d4a6fea5afacaab6d2e7372233725045c0b183e96925dec212ddf0ac468cdc1",
                host="ec2-174-129-192-200.compute-1.amazonaws.com"
            )
            # db = psycopg2.connect(
            #     database="Dreamland",
            #     user="postgres",
            #     password="1234",
            #     host="localhost"
            # )
            cur = db.cursor()
            cur.execute("SELECT dream From user_dreams")
            dream_user1 = cur.fetchall()
            #print(tuple())
            db.commit()
            db.close()
            dream_user=[]
            for i in dream_user1:
                dream_user.append(str(i))
            post_type=result['category']
            msg="Thanks for feeling  out your dream"
            return render_template('dream_post.html',dream=dream,msg=msg,dream_user=dream_user)
    except:
        pass
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')