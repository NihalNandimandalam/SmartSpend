show databases;
create database expense_manager;
use expense_manager;
show tables;
create table transactions (
transaction_id integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
 customer_id int,
transaction_date date,
transaction_description varchar(200),
amount float,
category SET("Rent", "Grocery", "Food", "Entertainment", "Bills", "Medical", "Miscellaneous", "Investment", "Uncategorized") default "Miscellaneous",
tag SET("Income","Expense")
);
select * from transactions;
create table customer(
id int AUTO_INCREMENT NOT NULL PRIMARY KEY,
user_id int
);
select * from customer;

create table statements(
id integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
customer_id int,
monthly_statement blob
);
select * from statements;
drop table transactions;