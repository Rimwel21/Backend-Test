from enum import Enum

# Role Enum (Student, Teacher, Admin):
class RoleEnum(str, Enum):
    student = "student"
    teacher = "teacher"
    admin = "admin"
    
# student type enum:
class StudentType(str, Enum):
    regular = "regular"
    HI = "hearing impaired"

class FileCategory(str, Enum):
    PROFILE_IMAGE = "PROFILE_IMAGE"
    LEARNING_MATERIAL = "LEARNING_MATERIAL"