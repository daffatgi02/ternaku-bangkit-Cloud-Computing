const bcrypt = require('bcrypt');
const User = require('../models/User');

// Controller untuk melakukan proses signup (registrasi pengguna baru)
const signup = async (req, res) => {
  const { username, password } = req.body;

  try {
    // Periksa apakah username sudah terdaftar
    const existingUser = await User.findOne({ where: { username } });
    if (existingUser) {
      return res.status(400).json({ message: 'Username already exists' });
    }

    // Enkripsi password sebelum disimpan ke database
    const hashedPassword = await bcrypt.hash(password, 10);

    // Buat user baru dalam database
    const newUser = await User.create({ username, password: hashedPassword });

    res.status(201).json({ message: 'User registered successfully' });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Internal server error' });
  }
};

// Controller untuk melakukan proses signin (autentikasi pengguna)
const signin = async (req, res) => {
  const { username, password } = req.body;

  try {
    // Periksa apakah username valid
    const user = await User.findOne({ where: { username } });
    if (!user) {
      return res.status(401).json({ message: 'Invalid username or password' });
    }

    // Periksa kecocokan password
    const isPasswordValid = await bcrypt.compare(password, user.password);
    if (!isPasswordValid) {
      return res.status(401).json({ message: 'Invalid username or password' });
    }

    // TODO: Generate and return authentication token

    res.json({ message: 'Signin successful' });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Internal server error' });
  }
};

// Controller untuk melakukan proses logout (menghapus session/token)
const logout = (req, res) => {
  // TODO: Implement logout functionality (e.g., invalidate token, clear session)

  res.json({ message: 'Logout successful' });
};

// Controller untuk menghandle forgot password
const forgotPassword = (req, res) => {
  // TODO: Implement forgot password functionality (e.g., send reset password email)

  res.json({ message: 'Forgot password request received' });
};

module.exports = {
  signup,
  signin,
  logout,
  forgotPassword,
};
