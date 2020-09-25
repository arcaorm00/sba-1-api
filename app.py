from flask import Flask
from flask import render_template, request
from price_prediction.cabbage import Cabbage
from member.students import Student, StudentService

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('join.html')

# method 종류에는 총 4개가 있다.
# GET, POST, PUT, DELETE 그래서 이것들은 다같이 array를 이룬다.
# 그 array 이름은 methods이다.
# app에서는 POST라고 하면 인지하지 못하고 ['POST']라고 해야 인지한다.
# 따라서 아래의 코드는 method=['POST']로 바뀌어야 한다.
# @app.route('/cabbage', method='POST')
# 이런 methods를 RESTful이라고 한다.
@app.route('/cabbage', methods=['POST'])
def cabbage():
    print('UI -> API Connect Success')
    avgTemp = request.form['avgTemp']
    minTemp = request.form['minTemp']
    maxTemp = request.form['maxTemp']
    rainFall = request.form['rainFall']
    print(f'avgTemp: {avgTemp}')
    print(f'minTemp: {minTemp}')
    print(f'maxTemp: {maxTemp}')
    print(f'rainFall: {rainFall}')
    cabbage = Cabbage()
    cabbage.avgTemp = avgTemp
    cabbage.minTemp = minTemp
    cabbage.maxTemp = maxTemp
    cabbage.rainFall = rainFall
    result = cabbage.service()
    print(f'**** PREDICTION RESULT: {result}')
    render_params = {}
    render_params['result'] = result
    return render_template('index.html', **render_params)

@app.route('/signup', methods=['POST'])
def signup():
    print('########## SIGNUP ##########')
    id = request.form['id']
    pwd = request.form['pwd']
    name = request.form['name']
    birth = request.form['birth']

    student = Student()
    student.id = id
    student.pwd = pwd
    student.name = name
    student.birth = birth
    service = StudentService()
    service.add_students(student)

    

if __name__ == "__main__":
    app.run()