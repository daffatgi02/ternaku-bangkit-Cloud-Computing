const passport = require('passport');

// Fungsi untuk menginisialisasi proses otentikasi Google
exports.authenticateGoogle = passport.authenticate('google', { scope: ['profile', 'email'] });

// Fungsi yang dipanggil setelah pengguna berhasil mengotentikasi dengan Google
exports.googleCallback = passport.authenticate('google', {
  successRedirect: '/',
  failureRedirect: '/login',
});

// Fungsi untuk memeriksa apakah pengguna telah login
exports.checkAuthenticated = (req, res, next) => {
  if (req.isAuthenticated()) {
    return next();
  }

  res.redirect('/login');
};

// Fungsi untuk logout pengguna
exports.logout = (req, res) => {
  req.logout();
  res.redirect('/');
};
