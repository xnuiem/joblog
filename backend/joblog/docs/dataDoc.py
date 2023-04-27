from apiflask import Schema
from apiflask.fields import String


class InitDataOut(Schema):
    message = String(
        required=True,
        metadata={'description': 'Return Message'}
    )

class JobSchema(Schema):
    pass

jobDataExample = {
    "id": "dc3f3d5d-888c-4d5e-bcb3-acce40a4e469",
    "title": "VP of Engineering",
    "status": "Applied",
    "source": "Source",
    "company": "Company",
    "recruiter": "Recruiter",
    "last_activity": "datetime",
    "offer_date": "date",
    "notes": "Notes",
    "interviews": [{
        "id": "date"
    }
    ]
}


dataOutExample = {
    'message': 'Data Init Complete'
}

dataInvalidKeyExample = {
    'message': 'Invalid Key'
}

clearOutExample = {
    'message': 'Data Flushed'
}
