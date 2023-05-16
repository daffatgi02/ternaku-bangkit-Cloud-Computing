const express = require('express');
const router = express.Router();
const userController = require('../controllers/userController');

// Route untuk mendapatkan semua pengguna
router.get('/', userController.getAllUsers);

// Route untuk mendapatkan pengguna berdasarkan ID
router.get('/:id', userController.getUserById);

// Route untuk membuat pengguna baru
router.post('/', userController.createUser);

// Route untuk mengupdate pengguna berdasarkan ID
router.put('/:id', userController.updateUser);

// Route untuk menghapus pengguna berdasarkan ID
router.delete('/:id', userController.deleteUser);

module.exports = router;
