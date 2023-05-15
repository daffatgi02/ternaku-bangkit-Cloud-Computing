const express = require('express');
const router = express.Router();
const medicineController = require('../controllers/medicineController');

// Rute untuk mendapatkan semua obat-obatan
router.get('/medicines', medicineController.getAllMedicines);

// Rute untuk mendapatkan detail obat-obatan berdasarkan ID
router.get('/medicines/:id', medicineController.getMedicineById);

module.exports = router;
