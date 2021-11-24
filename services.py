from .models import Student
from django.http import Http404

def create_student(*,name: str, father_name: str, standard:int):
    student = Student.objects.create(name=name, father_name=father_name, standard=standard)
    return student

def get_students():
    students = Student.objects.all()
    return students

def get_student_object(*,pk: int):
    try:
        return Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        raise Http404

def update_student(instance,data):
            instance.name = data.get("name")
            instance.father_name = data.get("father_name")
            instance.standard = data.get("standard")
            instance.save()
            return instance


def update_student(*, student=Student, name: str, father_name: str, standard:int):
    student.name = name
    student.father_name = father_name
    student.standard = standard
    student.save()
    return student
