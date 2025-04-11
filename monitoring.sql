CREATE TABLE IF NOT EXISTS sonde_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sonde_name TEXT NOT NULL,
    server TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    data NUMERIC NOT NULL
);

CREATE TABLE IF NOT EXISTS alertes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    link TEXT NOT NULL,
    description TEXT NOT NULL
);