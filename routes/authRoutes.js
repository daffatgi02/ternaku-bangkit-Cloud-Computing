const express = require('express');
const router = express.Router();
const authController = require('../controllers/authController');

// Rute untuk menginisialisasi proses otentikasi Google
router.get('/auth/google', authController.authenticateGoogle);

// Rute callback setelah pengguna berhasil mengotentikasi dengan Google
router.get('/auth/google/callback', authController.googleCallback);

// Rute untuk logout pengguna
router.get('/logout', authController.logout);

module.exports = router;
