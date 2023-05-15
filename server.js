const express = require('express');
const cors = require('cors');
const app = express();
const port = 3000;

app.use(cors()); // Menggunakan middleware cors


app.listen(port, () => {
  console.log(`App listening on port http://localhost:${port}`);
});
