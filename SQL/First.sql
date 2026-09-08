DROP DATABASE IF EXISTS test_db;
CREATE DATABASE test_db;
USE test_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY, 
    name VARCHAR(50)
);

INSERT INTO users (name) VALUES ('Aditya') , ('Rahul') , ('Kanha');
insert into users (name) VALUES ("Miral");
COMMIT;
ROLLBACK;

SELECT * FROM test_db.users;

delete from users where id = 5;