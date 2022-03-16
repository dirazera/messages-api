import uuid
from datetime import datetime, timedelta
from messages import app, db
from messages.models import MessageDB


dt1 = datetime.now()
dt2 = dt1 + timedelta(hours=1)
dt3 = dt1 + timedelta(hours=2)
id1 = str(uuid.uuid4())
id2 = str(uuid.uuid4())
id3 = str(uuid.uuid4())
recipient='you1@test.com'


def do_db_drop():
    db.drop_all()
    print('Database dropped!')


def do_db_create():
    db.create_all()
    print('Database created!')

def do_db_seed():
    msg1 = MessageDB(id=id1,
                     creation_date=dt1,
                     sender='test1@test.com',
                     recipient=recipient,
                     subject='First meeting',
                     content='Monday we will meet at 15',
                     new=True)

    msg2 = MessageDB(id=id2,
                     creation_date=dt2,
                     sender='test2@test.com',
                     recipient=recipient,
                     subject='Second meeting',
                     content='Tuesday we will meet at 15',
                     new=True)
    
    msg3 = MessageDB(id=id3,
                     creation_date=dt3,
                     sender='test3@test.com',
                     recipient=recipient,
                     subject='Third meeting',
                     content='Wednesday we will meet at 15',
                     new=True)

    db.session.add(msg1)
    db.session.add(msg2)
    db.session.add(msg3)
    db.session.commit()
    print('Database seeded!')


# Standalone flask
@app.cli.command('db_create')
def db_create():
    do_db_create()    


@app.cli.command('db_drop')
def db_drop():
    do_db_drop()
    

@app.cli.command('db_seed')  # Populate db with an initial set of data
def db_seed():
    do_db_seed()
    
