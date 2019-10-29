CREATE USER mysite_prod;
CREATE DATABASE mysite_prod OWNER mysite_prod;
GRANT ALL PRIVILEGES ON DATABASE mysite_prod TO mysite_prod;
ALTER USER mysite_prod CREATEDB;
