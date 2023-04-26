from apiflask import Schema
from apiflask.fields import String


class InitDataOut(Schema):
    message = String(
        required=True,
        metadata={'description': 'Return Message'}
    )


class ClearDataOut(Schema):
    message = String(
        example='Data Flushed',
        description='Message returned',
        title='Message'
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
