-- Stock metadata
CREATE TABLE IF NOT EXISTS stock_metadata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT UNIQUE NOT NULL
);

-- Daily stock prices
CREATE TABLE IF NOT EXISTS daily_stock_prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stock_id INTEGER NOT NULL,
    date DATE NOT NULL,
    open_price REAL,
    high_price REAL,
    low_price REAL,
    close_price REAL,
    volume INTEGER,
    market_cap REAL,
    FOREIGN KEY(stock_id) REFERENCES stock_metadata(id),
    UNIQUE(stock_id, date)
);

-- Index compositions
-- Table to store the composition of the index for each date
CREATE TABLE IF NOT EXISTS index_compositions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    stock_id INTEGER NOT NULL,
    weight REAL NOT NULL,
    FOREIGN KEY (stock_id) REFERENCES stock_metadata(id),
    UNIQUE (date, stock_id)
);

-- Table to store index performance per date
CREATE TABLE IF NOT EXISTS index_performance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL UNIQUE,
    index_level REAL NOT NULL,
    daily_return REAL,
    cumulative_return REAL
);
