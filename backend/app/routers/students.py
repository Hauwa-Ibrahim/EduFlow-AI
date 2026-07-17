from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentResponse

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)



@router.get("/", response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    return db.query(Student).all()


@router.post("/", response_model=StudentResponse)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    new_student = Student(
        first_name=student.first_name,
        last_name=student.last_name,
        email=student.email,
        institution=student.institution,
        programme=student.programme,
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student
@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student
@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    updated_student: StudentCreate,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.id == student_id).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    student.first_name = updated_student.first_name
    student.last_name = updated_student.last_name
    student.email = updated_student.email
    student.institution = updated_student.institution
    student.programme = updated_student.programme

    db.commit()
    db.refresh(student)

    return student

@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db.delete(student)
    db.commit()

    return {"message": "Student deleted successfully"}