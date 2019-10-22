CREATE USER mysite_dev;
CREATE DATABASE mysite_dev OWNER mysite_dev;
GRANT ALL PRIVILEGES ON DATABASE mysite_dev TO mysite_dev;
ALTER USER mysite_dev CREATEDB;
