const express = require('express');
const router = express.Router();
const articleController = require('../controllers/articleController');

// Route untuk mendapatkan semua artikel
router.get('/articles', articleController.getAllArticles);

// Route untuk mendapatkan artikel berdasarkan ID
router.get('/articles/:id', articleController.getArticleById);

module.exports = router;
