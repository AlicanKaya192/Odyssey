CREATE TABLE tickets (
    id INT IDENTITY(1,1) PRIMARY KEY,
    title NVARCHAR(60) NOT NULL,
    status NVARCHAR(20) NOT NULL DEFAULT 'open'
);

INSERT INTO tickets (title) VALUES
    ('Printer is offline'),
    ('VPN is slow');
