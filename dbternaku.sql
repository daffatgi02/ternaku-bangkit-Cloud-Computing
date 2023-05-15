CREATE TABLE medicines (
  id INT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  description VARCHAR(255) NOT NULL,
  price DECIMAL(10, 2) NOT NULL
);

INSERT INTO medicines (id, name, description, price)
VALUES
  (1, 'Paracetamol', 'Obat penurun demam dan pereda nyeri', 5000), 
  (2, 'Amoxicillin', 'Antibiotik untuk infeksi bakteri', 10000),
  (3, 'Loratadine', 'Obat alergi dan antihistamin', 8000);

CREATE TABLE Articles (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  content TEXT NOT NULL,
  image VARCHAR(255)
);

INSERT INTO Articles (title, content, image) VALUES
('Peternakan Sapi: Panduan untuk Petani Pemula', 'Artikel ini memberikan panduan langkah demi langkah bagi petani pemula yang ingin memulai peternakan sapi. Anda akan belajar tentang persiapan lahan, pemilihan bibit sapi, pakan yang tepat, serta perawatan dan manajemen yang diperlukan.', 'gambar-sapi.jpg'),
('Cara Efektif Merawat Sapi Anda', 'Artikel ini memberikan tips dan trik tentang cara merawat sapi Anda dengan efektif. Mulai dari memberikan pakan yang seimbang, menjaga kebersihan kandang, hingga menjaga kesehatan sapi Anda. Dapatkan informasi berharga di sini!', 'sapi-merawat.jpg');
