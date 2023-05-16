const User = require('../models/User');

// Controller untuk mendapatkan semua pengguna
const getAllUsers = async (req, res) => {
  try {
    const users = await User.findAll();
    res.status(200).json(users);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Terjadi kesalahan saat mengambil pengguna' });
  }
};

// Controller untuk mendapatkan pengguna berdasarkan ID
const getUserById = async (req, res) => {
  const { id } = req.params;

  try {
    const user = await User.findByPk(id);

    if (!user) {
      return res.status(404).json({ message: 'Pengguna tidak ditemukan' });
    }

    res.status(200).json(user);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Terjadi kesalahan saat mengambil pengguna' });
  }
};

// Controller untuk membuat pengguna baru
const createUser = async (req, res) => {
  const { username, email, password } = req.body;

  try {
    // Periksa apakah pengguna dengan email yang sama sudah ada
    const existingUser = await User.findOne({ where: { email } });
    if (existingUser) {
      return res.status(400).json({ message: 'Email already exists' });
    }

    // Buat pengguna baru
    const newUser = await User.create({ username, email, password });

    res.status(201).json(newUser);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Internal server error' });
  }
};

// Controller untuk memperbarui pengguna
const updateUser = async (req, res) => {
  const { id } = req.params;
  const { username, email, password } = req.body;

  try {
    // Periksa apakah pengguna dengan ID yang diberikan ada
    const user = await User.findByPk(id);
    if (!user) {
      return res.status(404).json({ message: 'User not found' });
    }

    // Perbarui data pengguna
    user.username = username;
    user.email = email;
    user.password = password;

    await user.save();

    res.status(200).json(user);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Internal server error' });
  }
};

// Controller untuk menghapus pengguna
const deleteUser = async (req, res) => {
  const { id } = req.params;

  try {
    // Periksa apakah pengguna dengan ID yang diberikan ada
    const user = await User.findByPk(id);
    if (!user) {
      return res.status(404).json({ message: 'User not found' });
    }

    // Hapus pengguna
    await user.destroy();

    res.status(200).json({ message: 'User deleted successfully' });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Internal server error' });
  }
};

module.exports = {
  getAllUsers,
  getUserById,
  createUser,
  updateUser,
  deleteUser,
};
