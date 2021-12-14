import psycopg2


con=psycopg2.connect("dbname='project2017' user='postgres' host='localhost' password='gs200697'")
cur = con.cursor()
cur.execute("""select id , name , nonull::float/ withnull as avr_per_dep
from 
	(SELECT id , name, count(patientamka) AS nonull
	FROM(	SELECT departments.id ,departments.name ,appointments.patientamka ,count(*)
		FROM appointments
		INNER JOIN doctor ON appointments.doctoramka=doctor.doctoramka
		INNER JOIN departments ON doctor.speciality=departments.id
		WHERE appointments.diagnosis is not NULL
		GROUP BY departments.id ,departments.name ,appointments.patientamka 
		ORDER BY 1 ) AS A
	GROUP BY id, name
	ORDER BY 1  )AS A
INNER JOIN 	
	(SELECT id , name, count(patientamka) AS withnull
	FROM(	SELECT departments.id ,departments.name ,appointments.patientamka ,count(*)
		FROM appointments
		INNER JOIN doctor ON appointments.doctoramka=doctor.doctoramka
		INNER JOIN departments ON doctor.speciality=departments.id
		GROUP BY departments.id ,departments.name ,appointments.patientamka 
		ORDER BY 1 ) AS B
	GROUP BY id, name
	ORDER BY 1  ) AS B USING (id,name);
""")
 
rows = cur.fetchall()
for r in rows:
    print r