phone_book_manager | [![Build Status](https://travis-ci.org/7CStudio/phone_book_manager.svg?branch=master)](https://travis-ci.org/7CStudio/phone_book_manager)
Python API server to manage user phone book contacts

Phone book manager is a Python web application to manage user contacts.

Setup
=====

It is advised to install all the requirements inside [virtualenv], use [virtualenvwrapper] to manage virtualenvs.

[virtualenv]: https://virtualenv.pypa.io/en/latest/
[virtualenvwrapper]: https://virtualenvwrapper.readthedocs.org/en/latest/

```
sudo apt-get install libpq-dev python-dev  # ubuntu
pip install -r requirements-dev.txt
```

Running local dev server
====

``` bash
# Use any database of your choice. This is for postgres
createdb pbm
export SQLALCHEMY_DATABASE_URI='postgresql://:@localhost/pbm'
export APP_TOKEN='dklsvjkjflfkldklf'
python app.py
```

API
===

The application is stand alone and manages only contacts of the user. User management isn't part of the application. For documentation purpose, we will call application as `contact server`.  We will call the server managing user details  as `auth server`.

The app has two endpoints, `user endpoint: /api/v1/phonebook/user` and `sync endpoint: /api/v1/phonebook/sync`.

`user endpoint` is for auth server to post the details of the users in the system. When a new user joins the system, the auth server should post the user details to this endpoint.

To confirm the permission of the requester, server or worker should post the `APP_TOKEN`. `APP_TOKEN` is set in the environment variable. Here is a sample curl request.

```bash
curl -X POST https://pbm.herokuapp.com/api/v1/phonebook/user -H "Authorization: <app_token>" -d '{"phone": "+911234567890", "access_token": "kdsjfkvjfkhdjfhsdkfhjdkf"}' -H "Content-Type: application/json"
```

Response:

```bash
{"access_token": "kdsjfkvjfkhdjfhsdkfhjdkf", "id": 1, "phone": "+911234567890"}
```

The response status code is `201` when for the new user. Status code `200` for existing user in the system.

The Client can sync the contact using `sync endpoint`. The Client should send user `access_token` in the header. If the `access_token` is incorrect, the client receives `401` status code. Here is a sample curl request.

```bash
krace@Kracekumars-MacBook-Pro ~/c/>
curl -X POST https://pbm.herokuapp.com/api/v1/phonebook/sync -H "Authorization: kdsjfkvjfkhdjfhsdkfhjdkf" -d '{"contacts": [{"phone": "+911234567890", "name": "foo"}]}' -H "Content-Type: application/json"
```

Response:

``` bash
[{"is_user": false, "name": "foo", "phone": "+911234567890"}]
```

- The contact server doesn't limit the number of contacts to receive. For performance reason, the client should paginate entire contacts. Idle size is `50 - 100`.


Heroku:
=====
- Demo application is available in heroku.
- User Endpoint: `https://pbm.herokuapp.com/api/v1/phonebook/user`
- Sync Endpoint: `https://pbm.herokuapp.com/api/v1/phonebook/sync`
- Demo APP Token: `sc.ewfjfjfsfsdjwcerfg`
- Demo User Access Token: `kdsjfkvjfkhdjfhsdkfhjdkf`

Deployment
===

Before deploying the code, create DB schema by running `invoke create_schema`. Don't forget to set environment variables.

You can deploy the app along with existing server and `nginx` config looks like

```

upstream pbm {

    # server unix:///path/to/your/mysite/mysite.sock; # for a file socket

    server 127.0.0.1:8001;

}

...

location /pbm/ {

    uwsgi_pass pbm;

    include /path/to/your/mysite/uwsgi_params;

}

```

Sample `uwsgi` config is available as `uwsgi.ini`.
