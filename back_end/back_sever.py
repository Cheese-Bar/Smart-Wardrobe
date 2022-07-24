from flask import Flask

app = Flask(__name__)



@app.route('/')
def index():
	
	return 'Index'



@app.route('/hello')
def hello():
	
	return 'Hello World!'



@app.route('/greeting/<name>/<int:age>')
def greeting(name, age):

	print(type(name))
	print(type(age))
	return 'Hello {}! You are {} years old!'.format(name, age)

app.run('0.0.0.0',9000)