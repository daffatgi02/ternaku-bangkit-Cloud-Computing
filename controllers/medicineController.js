const Medicine = require('../models/Medicine');

// Controller untuk mendapatkan daftar semua obat-obatan
const getAllMedicines = async (req, res) => {
  try {
    const medicines = await Medicine.findAll();
    res.json(medicines);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Internal server error' });
  }
};

// Controller untuk mendapatkan detail obat-obatan berdasarkan ID
const getMedicineById = async (req, res) => {
  const { id } = req.params;
  try {
    const medicine = await Medicine.findByPk(id);
    if (!medicine) {
      return res.status(404).json({ message: 'Medicine not found' });
    }
    res.json(medicine);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Internal server error' });
  }
};

module.exports = {
  getAllMedicines,
  getMedicineById,
};
