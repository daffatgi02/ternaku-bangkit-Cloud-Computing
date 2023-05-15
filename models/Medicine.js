const { DataTypes } = require('sequelize');
const db = require('../config/database');

const Medicine = db.define('Medicine', {
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true,
  },
  title: {
    type: DataTypes.STRING,
    allowNull: false,
  },
  content: {
    type: DataTypes.TEXT,
    allowNull: false,
  },
  image: {
    type: DataTypes.STRING,
    allowNull: true,
  },
}, {
  timestamps: false, // Menonaktifkan kolom createdAt dan updatedAt
});

module.exports = Medicine;
