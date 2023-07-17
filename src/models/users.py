from pydantic import BaseModel, ValidationError, field_validator

class User(BaseModel):
    chat_id: int
    full_name: str
    gender: bool
    user_state: str
    age: int
    balance: int

    @field_validator('age')
    def age_must_correct(cls,v):
        if v < 12 or v > 122:
            raise ValueError(' Возраст должен быть больше 12 и меньше 122')
        return v
    
    @field_validator('full_name')
    def name_must_be_not_number(cls,v):
        if not v.isalpha():
            raise ValueError("Имя не может содержать цифры и т.д.")
        return v.title()
        