# Howto
create a postgres database with the following command:

```
username=sherlock
dbname=sherlock
sudo -u postgres createuser -D -A -P $username
sudo -u postgres createdb -O $username $dbname
psql -U $username $dbname < create_db_postgres.sql
psql -U $username $dbname < create_spot_view.sql
```
