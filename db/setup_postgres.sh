# Script n está funcional. Ainda é preciso criar um .pgpass com a senha do postgres
db_name="db_clube_esportivo"
user_name="clube_dba"
user_password="1234567"

# Criar role, caso nao exista.
psql -U postgres -tc "SELECT 1 FROM pg_user WHERE usename = $db_owner" | grep -q 1 || psql -U postgres -c "CREATE ROLE $db_owner with PASSWORD '$user_password' CREATEDB LOGIN"

# Criar banco de dados, caso nao exista.
psql -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = $db_name;" | grep -q 1 || psql -U postgres -c "CREATE DATABASE $db_name with OWNER $user_name"
