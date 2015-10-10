from schema import ReceivedSms, Response, Endpoint, create_db_session

class DatabaseConnector():
    def __init__(self):
        self.session = create_db_session()

    def add(self, obj):
        self.session.add(obj)

    def add_received_sms(self, **kwargs):
        self.add(ReceivedSms(**kwargs))

    def add_response(self, **kwargs):
        self.add(Response(**kwargs))

    def add_endpoint(self, **kwargs):
        self.add(Endpoint(**kwargs))

    def add_all(self, objs):
        for obj in objs:
            self.add(obj)

    def query_sms(self, id=None, from_num=None, resolved=False):
        return self.session.query(ReceivedSms)

    def query_endpoints(self, endpoint=None):
        queries = self.session.query(Endpoint)
        if endpoint:
            queries.filter(Endpoint.service == endpoint)
        return queries.all()
