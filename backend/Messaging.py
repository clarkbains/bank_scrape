class Status():
    """A simple class to return messages to the frontend."""
    JSON = 6
    def json (json):
        return {'status':'json','info':'Check the json parameter for the payload','id':6,'json':json}

    ERROR = 5
    def error (msg):
        return {'status':'error','info':msg,'id':5}

    WARN = 4
    def warn (msg):
        return {'status':'warn','info':msg,'id':4}

    OK = 3
    def ok (msg):
        return {'status':'ok','info':msg,'id':3}

    NOT_AUTHORIZED = 2
    def not_authorized (msg):
        return {'status':'not_authorized','info':msg,'id':2}

    AUTHORIZED = 1
    def authorized (msg,token):
        return {'status':'authorized','info':msg,'token':token,'id':1}

    def assertStatus (status,statuscode):
        return status['id']==statuscode