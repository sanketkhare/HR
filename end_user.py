import os
from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
import pickle

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('file_upload.html')

@app.route('/file_upload', methods=['POST'])
def file_upload():
    file = request.files['file']
    file_path = os.path.abspath(file.filename)
    filename = file.filename
    folder_path = os.path.join(os.getcwd(), 'uploads', filename)
    file.save(file_path)

    # Loading the datasets
    test = pd.read_csv(file_path)
    test.insert(1, column = "target", value = 0)
    pre_result = test
    test = test.drop(columns = ['target'])

    # Data management on new test data same as training data
    test.drop(['enrollee_id','city'],axis=1,inplace=True)

    X_cats2 = (OneHotEncoder(sparse=False,handle_unknown='ignore')
                    .fit_transform(test[['gender','relevent_experience',
                            'enrolled_university','education_level',
                            'major_discipline','company_type',
                            'last_new_job','experience','company_size']]))
    X_cats2 = pd.DataFrame(X_cats2)

    X_numerical2 = test.drop(columns=['gender','relevent_experience',
                                    'enrolled_university','education_level',
                                    'major_discipline','company_type',
                                    'last_new_job','experience','company_size'])
    col_names = X_numerical2.columns
    X_numerical2 = pd.DataFrame(X_numerical2, columns=col_names)
    X_test2 = X_numerical2.join(X_cats2)

    X_test2.fillna(0, inplace=True)
    X_test2.columns = X_test2.columns.astype('str')

    with open("model_hr.pkl", "rb") as f:
        model = pickle.load(f)

    # Prediction for new test data
    pre_result.target = model.predict(X_test2)
    
    pre_result.to_csv('result.csv',index=False)
    folder_path2 = os.path.join(os.getcwd(), 'result.csv')
    #return render_template('prediction.html', prediction=folder_path2)
    pre_result.fillna('-', inplace=True)
    return render_template('table.html',pre_result=pre_result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)