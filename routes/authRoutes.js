const express = require('express');
const router = express.Router();
const authController = require('../controllers/authController');

// Route untuk signup
router.post('/signup', authController.signup);

// Route untuk signin
router.post('/signin', authController.signin);

module.exports = router;
