from apiflask import Schema
from apiflask.fields import String


class InitDataOut(Schema):
    message = String(
        required=True,
        metadata={'description': 'Return Message'}
    )


dataOutExample = {
    'message': 'Data Init Complete'
}

dataInvalidKeyExample = {
    'message': 'Invalid Key'
}

clearOutExample = {
    'message': 'Data Flushed'
}
