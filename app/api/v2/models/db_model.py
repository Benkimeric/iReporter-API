from werkzeug.security import generate_password_hash, check_password_hash


class Database():
    """Database class"""

    def db_query(self):
        users = """CREATE TABLE IF NOT EXISTS users(
        user_id serial PRIMARY KEY NOT NULL,
        first_name character varying(50) NOT NULL,
        last_name character varying(50) NOT NULL,
        other_names character varying(50) NOT NULL,
        username character varying(50) NOT NULL UNIQUE,
        email character varying(50) NOT NULL UNIQUE,
        phone_number character varying(13) NOT NULL UNIQUE,
        is_admin BOOLEAN NOT NULL DEFAULT FALSE,
        registered timestamp with time zone DEFAULT \
        ('now'::text):: date NOT NULL,
        password character varying(500) NOT NULL
            )"""

        incidents = """CREATE TABLE IF NOT EXISTS incidents(
        incident_id serial PRIMARY KEY NOT NULL,
        created_on timestamp with time zone DEFAULT\
         ('now'::text):: date NOT NULL,
        created_by integer NOT NULL REFERENCES users(user_id),
        type character varying(50),
        location character varying(100) NOT NULL,
        status character varying(20),
        comment character varying(2000) NOT NULL,
        images character varying(20),
        video character varying(20)
            )"""

        self.query = [users, incidents]
        return self.query

    admin_pass = generate_password_hash('admin@123')

    def add_admin(self):
            admin = """INSERT INTO users(first_name, last_name, other_names,\
            username, email, phone_number, is_admin, password) VALUES \
            ('admin', 'admin', 'admin', 'admin', 'admin@email.com',
            '0727501177', True, """ + """  \
            '""" + generate_password_hash('admin@123') + """' """ + """)"""
            return admin

    def drop_query(self):
            drop_users = """DROP TABLE IF EXISTS users"""

            drop_incidents = """DROP TABLE IF EXISTS incidents CASCADE"""

            self.query = [drop_users, drop_incidents]

            return self.query
