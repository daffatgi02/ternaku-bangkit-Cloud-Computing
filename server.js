const express = require('express');
const app = express();
const articleRoutes = require('./routes/articleRoutes');

// Middleware untuk parsing body request sebagai JSON
app.use(express.json());

// Menghubungkan rute-rute artikel ke aplikasi
app.use('/api', articleRoutes);

// Menjalankan server
const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Server berjalan di http://localhost:${port}`);
});
