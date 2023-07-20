from pydantic import BaseModel, ValidationError


class User(BaseModel):

    
    chat_id: int = 0 
    full_name: str = ''
    gender: bool = None
    user_state: str = ''
    age: int = 0
    balance: int = 0
    tgusr: str = ''

