Alter user 'wang'@'%' IDENTIFIED WITH mysql_native_password BY 'wang';
GRANT ALL PRIVILEGES ON blogsite.* TO 'wang'@'%';
FLUSH PRIVILEGES;