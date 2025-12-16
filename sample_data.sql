-- ==========================================
-- SQL DML Statements
-- Sample Data for Painters & Paintings Database
-- ==========================================

-- Insert Countries (at least 10)
INSERT INTO country (iso, country_name) VALUES
('IT', 'Italy'),
('FR', 'France'),
('ES', 'Spain'),
('NL', 'Netherlands'),
('US', 'United States'),
('GB', 'United Kingdom'),
('AT', 'Austria'),
('DE', 'Germany'),
('RU', 'Russia'),
('NO', 'Norway'),
('MX', 'Mexico'),
('BR', 'Brazil');

-- Insert Cities (at least 10)
INSERT INTO city (zipcode, name, country_iso) VALUES
('50122', 'Florence', 'IT'),
('00186', 'Rome', 'IT'),
('20121', 'Milan', 'IT'),
('75001', 'Paris', 'FR'),
('28013', 'Madrid', 'ES'),
('1012', 'Amsterdam', 'NL'),
('10001', 'New York', 'US'),
('SW1A', 'London', 'GB'),
('1010', 'Vienna', 'AT'),
('80331', 'Munich', 'DE'),
('101000', 'Moscow', 'RU'),
('0150', 'Oslo', 'NO');

-- Insert Artists (at least 10)
INSERT INTO artist (first_name, last_name, birth_year, death_year) VALUES
('Leonardo', 'da Vinci', 1452, 1519),
('Michelangelo', 'Buonarroti', 1475, 1564),
('Raphael', 'Sanzio', 1483, 1520),
('Sandro', 'Botticelli', 1445, 1510),
('Caravaggio', 'Merisi', 1571, 1610),
('Claude', 'Monet', 1840, 1926),
('Vincent', 'van Gogh', 1853, 1890),
('Pablo', 'Picasso', 1881, 1973),
('Salvador', 'Dalí', 1904, 1989),
('Frida', 'Kahlo', 1907, 1954),
('Rembrandt', 'van Rijn', 1606, 1669),
('Johannes', 'Vermeer', 1632, 1675),
('Diego', 'Velázquez', 1599, 1660),
('Edvard', 'Munch', 1863, 1944);

-- Insert Paintings (at least 10)
INSERT INTO painting (title, style_type, year_created, wikipedia_url) VALUES
('Mona Lisa', 'Renaissance', 1503, 'https://en.wikipedia.org/wiki/Mona_Lisa'),
('The Last Supper', 'Renaissance', 1498, 'https://en.wikipedia.org/wiki/The_Last_Supper_(Leonardo)'),
('The Creation of Adam', 'Renaissance', 1512, 'https://en.wikipedia.org/wiki/The_Creation_of_Adam'),
('David', 'Renaissance', 1504, 'https://en.wikipedia.org/wiki/David_(Michelangelo)'),
('The School of Athens', 'Renaissance', 1511, 'https://en.wikipedia.org/wiki/The_School_of_Athens'),
('The Birth of Venus', 'Renaissance', 1486, 'https://en.wikipedia.org/wiki/The_Birth_of_Venus'),
('Primavera', 'Renaissance', 1482, 'https://en.wikipedia.org/wiki/Primavera_(Botticelli)'),
('The Calling of St Matthew', 'Baroque', 1600, 'https://en.wikipedia.org/wiki/The_Calling_of_St_Matthew_(Caravaggio)'),
('Water Lilies', 'Impressionism', 1906, 'https://en.wikipedia.org/wiki/Water_Lilies_(Monet_series)'),
('Impression Sunrise', 'Impressionism', 1872, 'https://en.wikipedia.org/wiki/Impression,_Sunrise'),
('The Starry Night', 'Post-Impressionism', 1889, 'https://en.wikipedia.org/wiki/The_Starry_Night'),
('Sunflowers', 'Post-Impressionism', 1888, 'https://en.wikipedia.org/wiki/Sunflowers_(Van_Gogh_series)'),
('Guernica', 'Cubism', 1937, 'https://en.wikipedia.org/wiki/Guernica_(Picasso)'),
('Les Demoiselles d''Avignon', 'Cubism', 1907, 'https://en.wikipedia.org/wiki/Les_Demoiselles_d%27Avignon'),
('The Persistence of Memory', 'Surrealism', 1931, 'https://en.wikipedia.org/wiki/The_Persistence_of_Memory'),
('The Two Fridas', 'Surrealism', 1939, 'https://en.wikipedia.org/wiki/The_Two_Fridas'),
('Self-Portrait with Thorn Necklace', 'Surrealism', 1940, 'https://en.wikipedia.org/wiki/Self-Portrait_with_Thorn_Necklace_and_Hummingbird'),
('The Night Watch', 'Baroque', 1642, 'https://en.wikipedia.org/wiki/The_Night_Watch'),
('Girl with a Pearl Earring', 'Baroque', 1665, 'https://en.wikipedia.org/wiki/Girl_with_a_Pearl_Earring'),
('Las Meninas', 'Baroque', 1656, 'https://en.wikipedia.org/wiki/Las_Meninas'),
('The Scream', 'Expressionism', 1893, 'https://en.wikipedia.org/wiki/The_Scream');

-- Insert Painted relationships (Artist → Painting)
INSERT INTO painted (artist_id, painting_serial_number) VALUES
(1, 1),   -- Leonardo → Mona Lisa
(1, 2),   -- Leonardo → The Last Supper
(2, 3),   -- Michelangelo → The Creation of Adam
(2, 4),   -- Michelangelo → David
(3, 5),   -- Raphael → The School of Athens
(4, 6),   -- Botticelli → The Birth of Venus
(4, 7),   -- Botticelli → Primavera
(5, 8),   -- Caravaggio → The Calling of St Matthew
(6, 9),   -- Monet → Water Lilies
(6, 10),  -- Monet → Impression Sunrise
(7, 11),  -- van Gogh → The Starry Night
(7, 12),  -- van Gogh → Sunflowers
(8, 13),  -- Picasso → Guernica
(8, 14),  -- Picasso → Les Demoiselles d'Avignon
(9, 15),  -- Dalí → The Persistence of Memory
(10, 16), -- Kahlo → The Two Fridas
(10, 17), -- Kahlo → Self-Portrait with Thorn Necklace
(11, 18), -- Rembrandt → The Night Watch
(12, 19), -- Vermeer → Girl with a Pearl Earring
(13, 20), -- Velázquez → Las Meninas
(14, 21); -- Munch → The Scream

-- Insert Visitable relationships (City → Painting)
INSERT INTO visitable (city_country_iso, city_zipcode, painting_serial_number) VALUES
('FR', '75001', 1),   -- Paris → Mona Lisa
('IT', '20121', 2),   -- Milan → The Last Supper
('IT', '00186', 3),   -- Rome → The Creation of Adam
('IT', '50122', 4),   -- Florence → David
('IT', '00186', 5),   -- Rome → The School of Athens
('IT', '50122', 6),   -- Florence → The Birth of Venus
('IT', '50122', 7),   -- Florence → Primavera
('IT', '00186', 8),   -- Rome → The Calling of St Matthew
('FR', '75001', 9),   -- Paris → Water Lilies
('FR', '75001', 10),  -- Paris → Impression Sunrise
('NL', '1012', 11),   -- Amsterdam → The Starry Night
('NL', '1012', 12),   -- Amsterdam → Sunflowers
('ES', '28013', 13),  -- Madrid → Guernica
('FR', '75001', 14),  -- Paris → Les Demoiselles d'Avignon
('FR', '75001', 15),  -- Paris → The Persistence of Memory
('US', '10001', 16),  -- New York → The Two Fridas
('US', '10001', 17),  -- New York → Self-Portrait with Thorn Necklace
('NL', '1012', 18),   -- Amsterdam → The Night Watch
('NL', '1012', 19),   -- Amsterdam → Girl with a Pearl Earring
('ES', '28013', 20),  -- Madrid → Las Meninas
('NO', '0150', 21);   -- Oslo → The Scream
