from pydantic import BaseModel, Field, validator


class UserRegistrationDTO(BaseModel):
    chat_id: str
    age: str = Field(..., title="Возраст")


class ValidatedUserRegistrationDTO(UserRegistrationDTO):
    @validator('age')
    def validate_age(cls, age):
        try:
            age = int(age)
            if age < 12 or age > 122:
                raise ValueError("Возраст должен быть не меньше 12 лет и не больше максимума.")
        except (ValueError, TypeError):
            raise ValueError("Возраст должен быть числом.")
        return age
