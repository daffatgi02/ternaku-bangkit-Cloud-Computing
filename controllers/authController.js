const bcrypt = require('bcrypt');
const User = require('../models/User');
const { Op } = require('sequelize');


// Controller untuk signup
const signup = async (req, res) => {
  const { email, username, password } = req.body;

  try {
    // Periksa apakah pengguna dengan email atau username yang sama sudah ada
    const existingUser = await User.findOne({
      where: {
        [Op.or]: [{ email }, { username }],
      },
    });

    if (existingUser) {
      return res.status(400).json({ message: 'Email atau username sudah digunakan' });
    }

    // Enkripsi password menggunakan bcrypt
    const hashedPassword = await bcrypt.hash(password, 10);

    // Buat pengguna baru
    const newUser = await User.create({
      email,
      username,
      password: hashedPassword,
    });

    res.status(201).json(newUser);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Terjadi kesalahan saat mendaftar pengguna' });
  }
};

// Controller untuk signin
const signin = async (req, res) => {
  const { email, password } = req.body;

  try {
    // Cari pengguna berdasarkan email
    const user = await User.findOne({ where: { email } });

    if (!user) {
      return res.status(404).json({ message: 'Email atau password salah' });
    }

    // Periksa kecocokan password
    const isPasswordMatched = await bcrypt.compare(password, user.password);

    if (!isPasswordMatched) {
      return res.status(400).json({ message: 'Email atau password salah' });
    }

    res.status(200).json({ message: 'Signin berhasil' });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Terjadi kesalahan saat proses signin' });
  }
};

module.exports = {
  signup,
  signin,
};
