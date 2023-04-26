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
    '200': {
        'summary': 'Example Success',
        'value': {'message': 'Data Init Complete'}
    }
}


clearOutExample = {
    '200': {
        'summary': 'Example Success',
        'value': {'message': 'Data Flushed'}
    }
}
