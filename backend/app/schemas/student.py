from pydantic import BaseModel, EmailStr


class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    institution: str
    programme: str


class StudentResponse(StudentCreate):
    id: int
    status: str

    class Config:
        from_attributes = True