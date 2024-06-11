from pydantic import BaseModel


class Course(BaseModel):
    id: int
    name: str

class Discussion(BaseModel):
    id: int
    title: str

class DiscusssionEntry(BaseModel):
    message: str


class Assignment(BaseModel):
    id: int
    name: str


class AssignmentSubmission(BaseModel):
    get_hub_link: str