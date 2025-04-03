-- Only create database if it doesn't exist
SELECT 'CREATE DATABASE contacts_docker' 
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'contacts_docker')\gexec

-- Update password for existing postgres user
ALTER USER postgres WITH PASSWORD 'docker-contacts';

-- Grant privileges (works whether database existed or not)
GRANT ALL PRIVILEGES ON DATABASE contacts_docker TO postgres;