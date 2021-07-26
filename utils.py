from models import People, db_session, Users

def insert_people():
    person = People(name='Isaac', age=36)
    print(person)
    person.save()

def query_people():
    person = People.query.all()
    # person = People.query.filter_by(name='Rachel')#.first()
    for p in person:
        print(p.name)
        print(p.age)

def update_people():
    person = People.query.filter_by(name='Jordan').first()
    person.age=25
    person.save()

def remove_people():
    person = People.query.filter_by(name='isaac').first()
    person.delete()
    
def insert_user(login, password):
    user=Users(login=login, password=password)
    user.save()

def query_all_users():
    users = Users.query.all()
    print(users)
    
    
if __name__ == '__main__':
    # insert_people()
    # remove_people()
    # query_people()
    insert_user('david', '1234')
    insert_user('nat', '123')
    query_all_users()