import sqlite3
import atexit
from qaDBtools import Dao


# DTO
# Data Transfer Objects:
class Vaccine(object):
    def __init__(self, id, date, supplier, quantity):
        self.id = id
        self.date = date
        self.supplier = supplier
        self.quantity = quantity


class Supplier(object):
    def __init__(self, id, name, logistic):
        self.id = id
        self.name = name
        self.logistic = logistic


class Clinic(object):
    def __init__(self, id, location, demand, logistic):
        self.id = id
        self.location = location
        self.demand = demand
        self.logistic = logistic


class Logistic(object):
    def __init__(self, id, name, count_sent, count_received):
        self.id = id
        self.name = name
        self.count_sent = count_sent
        self.count_received = count_received


class _Vaccine:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, vaccines):
        self._conn.execute("""
                INSERT INTO students (id, date ,supplier,quantity) VALUES (?, ?, ?, ?)
           """, [vaccines.id, vaccines.date, vaccines.supplier, vaccines.quantity])

    def find(self, vaccine_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT id, name FROM Vaccine WHERE id = ?
        """, [vaccine_id])

        return Vaccine(*c.fetchone())


class _Suppliers:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, supplier):
        self._conn.execute("""
                INSERT INTO assignments (id, name,logistic) VALUES (?, ?, ?)
        """, [supplier.id, supplier.name, supplier.logistic])

    # def find(self, num):
    #     c = self._conn.cursor()
    #     c.execute("""
    #             SELECT num,expected_output FROM assignments WHERE num = ?
    #         """, [num])
    #
    #     return Supplier(*c.fetchone())


class _Clinics:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, clinic):
        self._conn.execute("""
            INSERT INTO grades (id, location, demand,logistic) VALUES (?, ?, ?, ?)
        """, [clinic.id, clinic.location, clinic.demand, clinic.logistic])

    # def find_all(self):
    #     c = self._conn.cursor()
    #     all = c.execute("""
    #         SELECT student_id, assignment_num, grade FROM grades
    #     """).fetchall()
    #
    #     return [Grade(*row) for row in all]


class _Logistics:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, logistic):
        self._conn.execute("""
            INSERT INTO grades (id, name, count_seny,count_received) VALUES (?, ?, ?, ?)
        """, [logistic.id, logistic.name, logistic.count_sent, logistic.count_received])


# Repository
class Repository(object):
    def __init__(self):
        self._conn = sqlite3.connect('database.db')
        self._conn.text_factory = str  # bytes
        self.Vaccine = Dao(Vaccine, self._conn)
        self.Supplier = Dao(Supplier, self._conn)
        self.Clinic = Dao(Clinic, self._conn)
        self.Logistic = Dao(Logistic, self._conn)

    def _close(self):
        self._conn.commit()
        self._conn.close()

    def create_tables(self):
        self._conn.executescript("""CREATE TABLE vaccines (
                id              INTEGER         PRIMARY KEY,
                date            DATE        NOT NULL,
                supplier    INTEGER ,
                quantity          INTEGER        NOT NULL,
                FOREIGN KEY(supplier) REFERENCES suppliers(id)
                   
             );
             CREATE TABLE suppliers (
                id                   INTEGER    PRIMARY KEY,
                name                 STRING       NOT NULL,
                logistic   INTEGER  ,

                 FOREIGN KEY(logistic) REFERENCES logistic(id)
            );

            CREATE TABLE clinics (
                id          INTEGER PRIMARY KEY,
                location STRING    NOT NULL,
                 demand       INTEGER NOT NULL,
                logistic    INTEGER ,
                 FOREIGN KEY(logistic) REFERENCES logistic(id)

            );

            CREATE TABLE logistics (
                id                  INTEGER     PRIMARY KEY,
                name            STRING         NOT NULL,
                count_sent INTEGER NOT NULL ,
                count_received INTEGER  NOT NULL 

            );
        """)

    def execute_command(self, script):
        return self._conn.cursor().execute(script).fetchall()


# singleton
repo = Repository()
atexit.register(repo._close)
