const express = require('express');
const app = express();
const db = require('./config/database');
const articleRoutes = require('./routes/articleRoutes');
const medicineRoutes = require('./routes/medicineRoutes');
const authRoutes = require('./routes/authRoutes');
const userRoutes = require('./routes/userRoutes');

// Menghubungkan ke database
db.authenticate()
  .then(() => {
    console.log('Connected to the database');
  })
  .catch((error) => {
    console.error('Unable to connect to the database:', error);
  });

// Middleware untuk mengizinkan parsing JSON
app.use(express.json());

// Mengatur rute-rute API
app.use('/api', articleRoutes);
app.use('/api', medicineRoutes);
app.use('/api/auth', authRoutes);
app.use('/api/users', userRoutes);

// Menjalankan server
const port = 3000;
app.listen(port, () => {
  console.log(`Server is running on port http://localhost:${port}`);
});
