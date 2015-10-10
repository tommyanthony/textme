from schema import ReceivedSms, Response, Endpoints, create_db_session

db_session = create_db_session()
GMAPS_API = "http://127.0.0.1:5000/directions/{1}/{2}"

def insert_test_data():
    db_session.add(
        Endpoints(service='google',
                  grammar='{str:}, {str:"regex";"alt_regex"},[int:1;2]',
                  endpoint=GMAPS_API)
    )
    db_session.commit()

if __name__ == "__main__":
    insert_test_data()
