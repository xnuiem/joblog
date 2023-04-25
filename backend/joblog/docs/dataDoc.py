from apiflask import Schema
from apiflask.fields import String


class InitDataOut(Schema):
    message = String(
        example='Data Init Complete',
        description='Message returned',
        title='Message'
    )


class ClearDataOut(Schema):
    message = String(
        example='Data Flushed',
        description='Message returned',
        title='Message'
    )


dataOutExamples = {
    'example 200': {
        'summary': 'Example Success',
        'value': {'message': 'Data Init Complete'}
    }
}

clearOutExamples = {
    'example 200': {
        'summary': 'Example Success',
        'value': {'message': 'Data Flushed'}
    }
}
