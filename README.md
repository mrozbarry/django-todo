# Django Todo App

## Setup

### Snakey things

 - Install `python 2.7.5`. I used pyenv (`brew install pyenv` on Mac), but potentially just using the system Python 2.x is fine?
 - Install `pip` (`bre install pip` on Mac)
 - Install app requirements using `pip -r ./requirements.txt`

### Environment

 - Install Postgres 9.x
 - Create a new postgres user for your app, `$ createuser django_todo`
 - Create the database, set your user's password, add user to the database:

```sql
$ psql
---
# CREATE DATABASE django_todo;
# ALTER USER django_todo SET PASSWORD 'super secret thing here' VALID UNTIL 'infinity';
# GRANT ALL PRIVILEGES ON DATABASE django_todo TO django_todo;
# \q
```

 - Set up the environment. `cp .env.example .env`
 - Configure the database information in the `.env` file.
 - I've also set things up so doing something like `DJANGO_ENV=production python manage.py runserver` sets the server environment. The environment defaults to `"development"`

### Running the server

```python
$ python manage.py runserver
```


## Brief

### The Plan

 - [x] Figure out the basics, lay some foundation.
 - [ ] Create a `TodoList` model, which has many `TodoListItem`s, and the following attributes:
  - id:integer
  - code:string, will be used for urls. Could replace id, but that ends up being less standard. Should be auto-generated on create.
  - name:string
  - public:boolean
 - [ ] Create `TodoListItem`, with the following attributes:
  - id:integer, regular index
  - todo_list_id:integer
  - position:integer, for re-ordering the list
  - name:string
  - done_at:datetime, can be null
 - [ ] Add a view for public todo lists.
 - [ ] Add a view for showing/editing a todo list.
 - [ ] Add a link to create a new empty todo list from the public list.
 - [ ] Figure out how to deploy this to heroku or a similar service.

### Execution

 1. Get the basics up and running using buttons, no javascript or anything fancy.
 2. Once "complete", branch to "boring-html" to preserve that state.
 3. Create a new branch "spicy-react" for react-based drag and drop version, make it spicy.
 4. ???
 5. Profit, or just learn stuff.
