from flask import Flask,render_template,request
import pickle
import pandas as pd
import sklearn
import numpy as np

app = Flask(__name__)
DEBUG = 1
HOST = '0.0.0.0'
PORT = 8080
app.jinja_env.auto_reload = True

model = pickle.load(open("model1.pkl","rb"))

"""""THIS IS THE DECALRATION OF THE VARIABLES WHICH WILL BE USED FURTHER IN THE CODE """

c = {"f_Delhi":0,"f_Mumbai":0,"f_Bangalore":0,"f_Kolkata":0,"f_Hyderabad":0,"f_Chennai":0}
for i in c.keys():
    globals()[i]=0


d = {"t_Delhi": 0, "t_Mumbai": 0, "t_Bangalore": 0, "t_Kolkata": 0, "t_Hyderabad": 0, "t_Chennai": 0}
for i in d.keys():
    globals()[i] = 0


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/predict',methods = ['POST'])
def predict_fare():
    if request.method == "POST":
        # Date_of_Journey
        date_dep = request.form["Dep_Time"]
        Dep_day = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day)
        Dep_month = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").month)


        # Departure
        Dep_hour = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").hour)
        Dep_min = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").minute)


        # Arrival
        date_arr = request.form["Arrival_Time"]
        Arr_hour = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").hour)
        Arr_min = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").minute)


        # Duration
        dur_hour = abs(Arr_hour - Dep_hour)
        dur_min = abs(Arr_min - Dep_min)
        timetaken = dur_hour+dur_min


        # Total Stops
        Stoppage = int(request.form["stops"])

        #airline
        airline = request.form['airline']
        a = 0


        if(airline=='Trujet'):
            a = 0
        elif(airline=='StarAir'):
            a = 1
        elif(airline=='SpiceJet'):
            a =2
        elif(airline=='AirAsia'):
            a = 3
        elif(airline=='GO First'):
            a =4
        elif(airline=='Indigo'):
            a =5
        elif(airline=='Air India'):
            a =6
        elif(airline=='Vistara'):
            a =7

        #source
        Source = request.form["Source"]

        c = {"f_Delhi":0,"f_Mumbai":0,"f_Bangalore":0,"f_Kolkata":0,"f_Hyderabad":0,"f_Chennai":0}
        for i in c.keys():
            if i == Source:
                c[Source] =1
                globals().update(c)


        #destination
        Source = request.form["Destination"]

        d = {"t_Delhi": 0, "t_Mumbai": 0, "t_Bangalore": 0, "t_Kolkata": 0, "t_Hyderabad": 0, "t_Chennai": 0}
        for i in d.keys():
            if i == Source:
                d[Source] =1
                globals().update(d)

        #class
        class1 = request.form['Class']
        f = 0
        if(class1=='Economy'):
            f = 0
        elif(class1=='Business'):
            f =1

        """ "" In this step some of the variables may show a error because the have not be declared yet they will be 
        created at the run time of the code"""

        prediction = model.predict([[a ,Stoppage,Dep_day,Dep_month,Dep_hour,Dep_min,Arr_hour,Arr_min,timetaken,f,
                                     f_Bangalore,f_Chennai,f_Delhi,f_Hyderabad,f_Kolkata,f_Mumbai,t_Bangalore,t_Chennai,
                                     t_Delhi,t_Hyderabad,t_Kolkata,t_Mumbai]])
        output = round(prediction[0], 2)

        return render_template("index.html", prediction_text="Your Flight price is Rs. {}".format(output))


if __name__=="__main__":
    app.run(debug=True)
