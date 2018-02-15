import threading

from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func

from tg_bot.modules.sql import SESSION, BASE

class UserInfo(BASE):
    __tablename__ = 'user_logger_data'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)
 
 
class MessageLogs(BASE):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_logger_data.id'), nullable=False)
    message = Column(String)
    # Use default=func.now() to set the default hiring time
    # of an Employee to be the current time when an
    # Employee record was created
    time = Column(DateTime, default=func.now())
    
UserInfo.__table__.create(checkfirst=True)
MessageLogs.__table__.create(checkfirst=True)

def id_exists(id_value):
    s = SESSION
    bool_set = False
    for id1 in s.query(UserInfo.id).filter_by(id=id_value):
        if id1:
            bool_set = True
            
    s.close()
    
    return bool_set
    
def log_message(user_id, user_message):

    try:
        s = SESSION
        msg1 = MessageLogs(user_id=user_id,message=user_message)
        s.add(msg1)
        s.commit()
        s.close()
    
    except Exception as e:
        print(e)
        
def add_user(user_id, first_name, last_name, username):
    try:
        s = SESSION
        bool_set = False
        user = UserInfo(id=user_id, first_name = first_name, last_name = last_name, username = username)
        s.add(user)
        s.commit()
        s.close()
        
        if id_exists(user_id) == True:
            bool_set = True
        
        return bool_set
        
    except Exception as e:
        print(e)
