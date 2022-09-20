from .flaskcast import app
#from flaskcast import app

print('Hello')

if __name__ == '__main__':
    print('Flask is run from casting_agency.py')
    print(__name__)
    #app.run(host='0.0.0.0', port=8080, debug=True) #changed it before pusghing to Heroku
else:
    print('Je comprends pas tout')
    print(__name__)