import os

from dotenv import load_dotenv
import requests
from fastapi import FastAPI

from models import Course, Discussion, DiscusssionEntry, AssignmentSubmission, Assignment


#/courses/:course_id/discussion_topics

load_dotenv()

app = FastAPI()

access_token = os.getenv("ACCESS_TOKEN")

base_url = "https://dixietech.instructure.com/api/v1"

headers: dict[str, str] = {
    "Authorization": f"Bearer {access_token}"
}




@app.get("/courses")
async def get_courses() -> list[Course]:
    response = requests.get(url=f"{base_url}/courses", headers=headers)
    r_json = response.json()

    courses: list[Course] = []
    for course_json in r_json:
        try:
            course = Course(id=course_json["id"], name=course_json["name"])
            courses.append(course)
        except KeyError:
            continue
    return courses

@app.get("/discussions")
async def get_discussions(course_id: int) -> list:
    response = requests.get(url=f"{base_url}/courses/{course_id}/discussion_topics", headers=headers)
    r_json = response.json()

    discussions: list[Discussion] = []
    for discussion_json in r_json:
        discussion = Discussion(id=discussion_json["id"], title=discussion_json["title"])
        discussions.append(discussion)    
    return discussions

@app.post("/discussion/entries")
async def discussion_entry(course_id: int, topic_id: int, body: DiscusssionEntry):
    
    response = requests.post(url=f"{base_url}/courses/{course_id}/discussion_topics/{topic_id}/entries", headers=headers, data=body.model_dump())
    r_json = response.json()
    return

@app.get("/assignment")
async def get_assignmanet(course_id: int):
    response = requests.get(url=f"{base_url}/courses/{course_id}/assignments")
    r_json = response.json()

    assignments: list[Assignment]
    for key in r_json:
        assignment = Assignment(id=key["id"], name=key["name"])
        assignments.append(assignment)
    return assignment

@app.post("/assignment/entry")
async def assignment_entry(course_id: int, assignment_id: int, body: AssignmentSubmission):
    payload = {"submission[submission_type]": "online_url",
               "submission[url]": body.get_hub_link}
    responce = requests.post(url=F"{base_url}/courses/{course_id}/assignments/{assignment_id}/submissions", headers=headers, data=payload)
    r_json = responce.json()
    return 





