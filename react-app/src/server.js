const express = require('express');
const mysql = require('mysql2');
const app = express();
const port = 3002;
const { DB_USER, DB_PASSWORD, DB_HOST, DB_NAME, DB_PORT } = process.env;

if (![DB_USER, DB_PASSWORD, DB_HOST, DB_NAME, DB_PORT].every(Boolean)) {
  console.error('ERROR: Database environment variables are not all set.');
  process.exit(1);
}

const dbUser = DB_USER;
const dbPassword = DB_PASSWORD;
const dbHost = DB_HOST;
const dbName = DB_NAME;
const dbPort = DB_PORT;

const connection = mysql.createConnection({
  host: dbHost,
  port: dbPort,
  user: dbUser,
  password: dbPassword,
  database: dbName
});

connection.connect(err => {
  if (err) {
    console.error('Error connecting to the database:', err);
    return;
  }
  console.log('Connected to the MySQL database.');
});

app.get('/api/data', (req, res) => {
  connection.query('SELECT title, abstract FROM Job', (err, results) => {
    if (err) {
      res.status(500).send(err);
      return;
    }
    res.json(results);
  });
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});