The purpose of my application is to manage a library.

# Database Design

Bolded attributes are primary keys, italicized attributes are 
foreign keys with relation paranthesized. 

Authors(**author_id**, name)
Books(**book_id**, *author_id* (Authors), title, pub_year, loan_count)

# SQL Injection Protection Method: Prepared Statements with ORM
All queries are formulated using SQLAlchemy ORM interface. Under
the hood, SQLAlchemy will build a prepared statement by
taking the user input as a string argument to a query. 

# Transactions
Transaction 1: Adding a book
Operations:
SELECT from Authors to see if the name exists.
INSERT into Authors (only if the name is new).
INSERT into Books using the author_id from the previous step.
Requires atomicity - if system crashes after creating Author but before saving book. 

Transaction 2: Borrowing a book
Operations:
SELECT the current loan_count for a specific book_id.
UPDATE the loan_count by adding 1.
Need transaction to help prevent data race when two users try to borrow at the same time.

Transaction 3: Deleting a book
Operations:
SELECT to verify the book exists.
DELETE the row from the Books table.
Requires atomicity, either book is fully removed or not at all.

# Isolation Level
We use SQLite default level, which is serializable. 
This is because there can be data races (consider two people borrowing book 
at same time) which means that the isolation level must be at least repeatable read.
In addition, there can be a phantom data problem when two people adding two books
for the same, new author if we only lock rows, where basically
because we are adding a new row, writing to it will not be locked and so 
the table may have discrepancies when the second person tries to 
read to see if an author exists.

# AI Usage

## Which AI Tools Were Used

Google Gemini.

## What Tasks the AI Assisted With
The task the LLM assisted with 
was coming up with the first draft of the 
non-database related code, essentialy
the HTML files and setup for the Flask application. 
I also used it to clarify concepts (this did not generate any output).

## How the student verified or modified the AI-generated output

The workflow I used is that I came up with the high-level ideas for the project, including (but not limited to): 
* Schema for database
* Operations on database
* Choice of isolation levels, sql injection
* GUI design 

I would then ask the LLM to generate the first draft of code 
that I regarded as "boilerplate", e.g. not related to 
the manipulation of the actual database. For example, I asked to
generate the HTML files which determined how the GUI would look. I would manually inspect and test LLM-generated code
by running it on different cases and looking up any 
code that I did not understand on the respective documentation
(for example, for HTML I used https://developer.mozilla.org/en-US/) to see if the LLM use made sense. I would then 
manually edit the code if there were parts of the code 
that I was unhappy with, such as if there were parts of the GUI that was not to my liking.

