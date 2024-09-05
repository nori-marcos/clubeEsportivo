# O script ainda não está funcional.
db_name='db_clube_esportivo'
psql -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = $db_name;" | grep -q 1 || psql -U postgres -c "CREATE DATABASE $db_name"
"CREATE ROLE clube_dba WITH PASSWORD '1234567' CREATEDB LOGIN;"
"CREATE DATABASE db_clube_esportivo;"
