<div align="center">
    <h1>💵 EZ Money</h1>
    <p>An <a href="https://www.dictionary.com/browse/ez">EZ</a> money tracker.</p>
    <a href="https://youtu.be/RX3WES8dKO0"><em>🎥 See it in action!</em></a>
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

## Usage

### Logging In

EZ Money uses Google OAuth 2.0 for authentication, so you can use any Google account to log in and use the application.

### Transaction Operations

#### Add

You can add an income or an expense by pressing the `Add Transaction` button.

Add an income by inputting a positive number. Add an expense by inputting a negative number. You can only input numbers between -1 billion and 1 billion, and with no more than 2 decimal places. A description and date must also be provided. The date must also be valid, and the app will not accept dates that are greater than the current date.

#### Edit

Hover over a transaction and press the `Edit` (✏️) button to edit it. The same rules for adding apply.

#### Delete

Hover over a transaction and press the `Delete` (🗑️) button to delete it.

### Sorting Transactions

You can sort transactions by week, month, and year via the `Sort by` dropdown menu. It defaults to "All time."

### Settings

#### Changing Currency Format

You can change the format of the currency via the currency selector. It uses the [currencies](https://pypi.org/project/currencies/) Python package to do this.

#### Graph Visibility

You can toggle the visibility of the graph by toggling the graph visibility switch.

#### Deleting All Transactions

If you want to delete all of your transactions, you can do so by clicking the `Delete All Transactions` button. Be careful! You can not undo this process.