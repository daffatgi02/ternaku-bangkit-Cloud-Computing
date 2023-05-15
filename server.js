const express = require('express');
const bodyParser = require('body-parser');
const session = require('express-session');
const passport = require('passport');
const db = require('./config/database');
const articleRoutes = require('./routes/articleRoutes');
const medicineRoutes = require('./routes/medicineRoutes');
const authRoutes = require('./routes/authRoutes');
require('dotenv').config();
require('./config/passport');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// Express session
app.use(
  session({
    secret: process.env.SESSION_SECRET,
    resave: false,
    saveUninitialized: false,
  })
);

// Passport middleware
app.use(passport.initialize());
app.use(passport.session());

// Routes
app.use('/articles', articleRoutes);
app.use('/medicines', medicineRoutes);
app.use('/auth', authRoutes);

// Database connection
db.authenticate()
  .then(() => console.log('Database connected...'))
  .catch((err) => console.error('Database connection error:', err));

// Start the server
app.listen(PORT, () => console.log(`Server started on port http://localhost:${PORT}`));
