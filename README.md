# Finglish to Persian Converter Telegram Bot
This telegram bot provides a Finglish-to-Persian convertor.

# How to Use:
Just add the [Telegram Bot](http://t.me/fintranslatebot) to your group as an Admin.

**NOTE**: Robot will automatically translate finglish messages and sends a message containing this information:
```
---------------------------
| name (@username):       |
|                         |
| <translated_message>    |
---------------------------
```


# Database
PostgreSQL is used to store information about users and messages.
## How to install
Install and update `Pip3`:

```
sudo apt install python3-pip
sudo pip3 install --upgrade pip
sudo pip3 install --upgrade setuptools
```

Now launch the installation command for `psycopg2`:
```
sudo pip3 install psycopg2
```
If it returns the following error:

`Command “python setup.py egg_info” failed with error code 1 in /tmp/pip-build-16pukcwj/psycopg2/`

Launch this other command:
```
sudo apt-get build-dep python3-psycopg2
```
And then try again with:
```
sudo pip3 install psycopg2
```

### Install PostgreSQL client
```
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
```