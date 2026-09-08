CREATE TABLE setup (
    id INT PRIMARY KEY,
    status NVARCHAR(20) NOT NULL
);

INSERT INTO setup (id, status) VALUES (1, 'ready');
