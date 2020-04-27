from createTables import create_tables
from createDB import create_db
from insertCountry import insert_country
from insertPatient import insert_patient
from dropDB import drop_db
from insertStatus import insert_status


create_db()
create_tables()
insert_country()
insert_patient()
insert_status()
