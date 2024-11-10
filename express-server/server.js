const express = require('express');
const { sequelize, Job } = require('/models');
const app = express();
const port = 3002;

sequelize.authenticate()
  .then(() => {
    console.log('Connection has been established successfully.');
  })
  .catch(err => {
    console.error('Unable to connect to the database:', err);
  });

app.get('/api/data', async (req, res) => {
  try {
    const jobs = await Job.findAll({ attributes: ['title', 'abstract'] });
    res.json(jobs);
  } catch (err) {
    res.status(500).send(err);
  }
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});