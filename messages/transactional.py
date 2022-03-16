from flask import abort
from functools import wraps
from messages import db
from sqlalchemy import exc




def transactional(function):
    
    @wraps(function)
    def transactional_wrapper(*args, **kwargs):
        try:
            with db.session.begin():                
                result = function(*args, **kwargs)
                db.session.commit()
                return result
        except exc.SQLAlchemyError as error:
            db.session.rollback()
            raise error
        finally:
            db.session.flush() 
    
    return transactional_wrapper
    
    
