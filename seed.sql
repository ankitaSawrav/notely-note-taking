-- TRUNCATE TABLE users;
-- TRUNCATE TABLE notes;

-- ALTER SEQUENCE user_id_seq RESTART WITH 1;
-- ALTER SEQUENCE notes_id_seq RESTART WITH 1;
-- user_id SERIAL PRIMARY KEY,user_name TEXT, user_email TEXT,password_hash VARCHAR(50)

INSERT INTO users (user_name, user_email , password_hash) VAlUES ('Bob','bob@gmail.com', '$2b$12$fgVGsHQ75g4fxwiSjVQ7eO3r2/4KTHva2Iq0LOwdF63NvLi63BwqC');
INSERT INTO users (user_name, user_email , password_hash) VAlUES ('sally','sally@gmail.com', '$2b$12$376oOWBCeEM.RV6LezM6MeqHj6oADbIJQXarZEIemr/W0dfqQ99iS');
INSERT INTO users (user_name, user_email , password_hash) VAlUES ('ankita','ankita@gmail.com', '$2b$12$6rPlJT7zvKVIV/snjei7eeGo72ZLRZbbxNCt8R98cbefrgp95c3H6');

-- -- -notes_id SERIAL PRIMARY KEY,user_id INTEGER REFERENCES users(user_id),title varchar(50),notes_description TEXT 
-- INSERT INTO users (user_id, user_email , password_hash) VAlUES ('Bob','bob@gmail.com', 'hello');

insert into notes(user_id, title , notes_description,likes,dislikes) VAlUES (1,'test data' , 'adding test data',1,4);
insert into notes(user_id,title,notes_description,likes,dislikes) VAlUES (2,'test new data', 'adding sally data',8,2);
insert into notes(user_id,title,notes_description,likes,dislikes) VAlUES (2,'test 3rd set data ', 'adding sally second data',0,1);
insert into notes(user_id,title,notes_description,likes,dislikes) VAlUES (3,'steps to start python app ', 'python -m venv venv source venv/bin/activate pip install Flask pip install requests',3,0);





