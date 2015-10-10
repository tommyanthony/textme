from schema import ReceivedSms, Response, Endpoints, create_db_session

db_session = create_db_session()

def insert_test_data():
    db_session.add(
        Endpoints(service='google',
                 grammar='{str:}, {str:"regex";"alt_regex"},[int:1;2]',
                 endpoint='https://www.uber.com/pickup/{0}'))
    db_session.commit()

if __name__ == "__main__":
    insert_test_data()
