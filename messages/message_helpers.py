import uuid
from datetime import datetime
from sqlalchemy import func
from messages import db
from messages.models import MessageDB, message_schema, messages_schema
from messages.transactional import transactional


@transactional
def create_message(sender,recipient,subject,content):
    new_message = MessageDB(sender=sender,recipient=recipient,subject=subject,content=content,id=str(uuid.uuid4()),creation_date=datetime.now(),new=True)
    db.session.add(new_message)
    result = message_schema.dump(new_message)
    return result


def __get_messages_subset(recipient,all):
    if all:
        return MessageDB.query.filter_by(recipient=recipient)

    return MessageDB.query.filter_by(new=True,recipient=recipient)


@transactional
def get_messages(recipient,all,page,page_size):
    messages_list = __get_messages_subset(recipient,all).order_by(func.datetime(MessageDB.creation_date))

    if page is not None:
        if page_size is None:
            page_size = 5
    
        messages_list = messages_list.offset(page*page_size).limit(page_size)
    else:
        messages_list = messages_list.all()

    result = messages_schema.dump(messages_list) # Deserialize the data retrieved from db
    if result and not all:        
        for message in messages_list:
            message.new=False

    return result


def get_message_by_id(recipient,message_id):
    message = MessageDB.query.filter_by(recipient=recipient,id=message_id).first()
    result = message_schema.dump(message)
    return result


@transactional
def delete_messages_by_id(recipient,ids): 
    deleted_messages_count = MessageDB.query.filter_by(recipient=recipient).filter(MessageDB.id.in_(ids)).delete()
    return deleted_messages_count




