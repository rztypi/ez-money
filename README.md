<div align="center">
    <h1>💵 EZ Money</h1>
    <p>An <a href="https://www.dictionary.com/browse/ez">EZ</a> money tracker.</p>
</div>

## About

**EZ Money** is a [Flask](https://flask.palletsprojects.com/en/3.0.x/)-based income/expense tracker that's simple to use. 

#### Features:

- Responsive web design using [Bootstrap](https://getbootstrap.com/)
- Google OAuth 2.0 authentication using [Authlib](https://authlib.org/)
- Data management using [SQLite](https://docs.python.org/3/library/sqlite3.html)
- Data visualization using [Chart.js](https://www.chartjs.org/)
- Currency format changer using [currencies](https://pypi.org/project/currencies/)

> *This is my final project for [CS50x](https://cs50.harvard.edu/x/).*

## Setup

It's fairly easy to get it started:

1. Clone or download this repository.
1. Set up and activate a [venv](https://docs.python.org/3/library/venv.html) on the repository.
1. Install the `ezmoney` package.

    ```console
    $ pip install .
    ```

1. Get your [Google API client ID](https://developers.google.com/identity/gsi/web/guides/get-google-api-clientid).

    - The scope must include **userinfo.email**, **userinfo.profile**, and **openid**.
    - Take note of your **client id** and **client secret**.

1. Add the following redirect URIs to your client ID's **Authorized redirect URIs**:

    - `http://localhost/auth/authorize`
    - `http://127.0.0.1/auth/authorize`

1. Create a **.env** file on the repository and set up the following environment variables:

    ```shell
    GOOGLE_CLIENT_ID="your google client id"
    GOOGLE_CLIENT_SECRET="your google client secret"
    ```

1. Run the Flask server.

    ```console
    $ flask --app ezmoney run
    ```