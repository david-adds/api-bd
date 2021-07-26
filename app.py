from flask import Flask, request
from flask_restful import Resource, Api
from models import People, Tasks, Users
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)
'''
USERS_ ={
    'david':'010203',
    'nat':'123'
}


@auth.verify_password
def verification(login, password):
    print('validate user')
    print(USERS_.get(login)==password)
    if not (login, password):
        return False
    return USERS_.get(login) == password
'''

@auth.verify_password
def verification(login, password):
    if not (login, password):
        return False
    return Users.query.filter_by(login=login, password=password).first()

class Person(Resource):
    @auth.login_required
    def get(self, name):
        person = People.query.filter_by(name=name).first()
        try:
            response = {
                'name': person.name,
                'age': person.age,
                'id': person.id
            }
        except  AttributeError:
            response = {
                'status': 'ERROR',
                'message': 'Person not found!'
            }
        return response
    def put(self, name):
        person = People.query.filter_by(name=name).first()
        data = request.json
        
        if "name" in data:
            person.name = data["name"]
        if "age" in data:
            person.age = data["age"]
        person.save()
        response = {
            'id': person.id,
            'name': person.name,
            'age': person.age
        }        
        return response
    
    def delete(self, name):
        person = People.query.filter_by(name=name).first()
        message = 'Person successfully deleted'.format(person.name)
        person.delete()
        return {'status':'Success!',
                'message': message}
    
class ListPeople(Resource):
    @auth.login_required
    def get(self):
        people = People.query.all()
        response = [{'id': p.id, 'name':p.name, 'age':p.age}  for p in people]
        return response
    def post(self):
        data = request.json
        person = People(name=data['name'], age = data['age'])
        person.save()
        response = {
            'id': person.id,
            'name': person.name,
            'age': person.age
        }
        return response

class ListTasks(Resource):
    
    def get(self):
        tasks = Tasks.query.all()
        response = [{'id':i.id, 'person':i.person.name, 'name': i.name} for i in tasks]
        return response
    
    def post(self):
        data = request.json
        person = People.query.filter_by(name = data['person']).first()
        task = Tasks(name = data['name'], person = person)
        task.save()
        response = {
            'person': task.person.name,
            'name': task.name,
            'id':task.id
        }
        return response

api.add_resource(Person, '/person/<string:name>/')
api.add_resource(ListPeople, '/person/')
api.add_resource(ListTasks,'/tasks/')
        

if __name__ == '__main__':
    app.run(debug=True)