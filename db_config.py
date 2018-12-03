import psycopg2

url = "dbname ='ireporter' host='localhost' post='5432' user='postgres' password= 'kali12'"
test_url = "dbname ='ireporter' host='localhost' post='5432' user='postgres' password= 'kali12'"

def connection(connect_url):
    conn = psycopg2.connect(connect_url)
    return conn

def init_db():
    conn = connection(url)
    return conn

def create_tables():
    conn = psycopg2.connect(url)
    curr = conn.cursor()
    queries = tables()

    for query in queries:
        curr.execute(query)
    conn.commit()

def destroy_tables():
    pass

def tables():
    users = """ CREATE TABLE IF NOT EXISTS users(
        user_id serial PRIMARY KEY NOT NULL,
        first_name character varying(50) NOT NULL,
        other_name character varying(50) NOT NULL,
        last_name character varying(50) NOT NULL,
        username character varying(50) NOT NULL,
        date_created timestamp with time zone DEFAULT ('now'::text):: date NOT NULL,
        password character varying(50) NOT NULL
    )"""

    incidents = """CREATE TABLE IF NOT EXISTS incidents(
        incident_id serial PRIMARY KEY NOT NULL,
        created_by numeric NOT NULL,
        type character varying(50) NOT NULL,
        status character varying(20) DEFAULT draft,
        location character varying(100) NOT NULL,
        created_on timestamp with time zone DEFAULT ('now'::text):: date NOT NULL,
    )"""

    queries = [users, incidents]
    return queries