INSERT INTO user (id, email, given_name, family_name)
VALUES ('thisisatestid', 'hello_world@gmail.com', 'Hello', 'World');

INSERT INTO transactions (user_id, description, amount, created)
VALUES ('thisisatestid', 'this is an expense', -1000, date('now'));

INSERT INTO transactions (user_id, description, amount, created)
VALUES ('thisisatestid', 'this is an income', 1000, date('now'));

INSERT INTO user (id, email, given_name, family_name)
VALUES ('notransactions', 'no_transactions@gmail.com', 'No', 'Transactions');