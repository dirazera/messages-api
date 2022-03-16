
from sqlalchemy import Column, DateTime, String, Boolean, Text
from messages import db, ma


class MessageDB(db.Model):
    __tablename__ = 'messages'
    id = Column(String, primary_key=True)
    creation_date = Column(DateTime)
    sender = Column(String, nullable=False) 
    recipient = Column(String, nullable=False) 
    subject = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    new = Column(Boolean, nullable=False)


class MessageDBSchema(ma.Schema):
    class Meta:
        fields = ('id','creation_date','sender','recipient','subject','content','new')

message_schema = MessageDBSchema()
messages_schema = MessageDBSchema(many=True) # Several message entries to be retrieved



