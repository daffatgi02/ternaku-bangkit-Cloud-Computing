const Article = require('../models/Article');

// Handler untuk mendapatkan semua artikel
const getAllArticles = async (req, res) => {
  try {
    const articles = await Article.findAll();
    res.status(200).json(articles);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Terjadi kesalahan saat mengambil artikel' });
  }
};

// Handler untuk mendapatkan artikel berdasarkan ID
const getArticleById = async (req, res) => {
  const { id } = req.params;

  try {
    const article = await Article.findByPk(id);

    if (!article) {
      return res.status(404).json({ message: 'Artikel tidak ditemukan' });
    }

    res.status(200).json(article);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Terjadi kesalahan saat mengambil artikel' });
  }
};

module.exports = {
  getAllArticles,
  getArticleById,
};
