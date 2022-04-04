CREATE SCHEMA messaging;
CREATE TABLE messaging.users
(
    id serial PRIMARY KEY,
    first_name varchar(32),
    last_name varchar(32),
    user_name varchar(32) UNIQUE,
    email varchar(254) UNIQUE,
    mfa BOOLEAN NOT NULL,
    created_at TIMESTAMP,
    modified_at TIMESTAMP
);

CREATE INDEX user_name_idx ON messaging.users ("user_name");

CREATE SEQUENCE messaging.messaging_sequence START 1;

CREATE TABLE messaging.messages
(
    id INT DEFAULT nextval('messaging.messaging_sequence'::regclass) NOT NULL,
    sender_id INT NOT NULL,
    recipient_id INT NOT NULL,
    body text NOT NULL,
    created_at TIMESTAMP,
    timestamp_sent TIMESTAMP,
    timestamp_delivered TIMESTAMP,
    timestamp_read TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES messaging.users (id),
    FOREIGN KEY (recipient_id) REFERENCES messaging.users (id)
);

INSERT INTO messaging.users(
    id,
    first_name,
    last_name,
    user_name,
    email,
    mfa,
    created_at,
    modified_at
) VALUES
 (1, 'Rebecca', 'DiBari', 'rdibari', 'someemail@gmail.com', false, now(), null),
 (2, 'Bugs', 'Bunny', 'bugs', 'whatupdoc@gmail.com', false, now(), null),
 (3, 'Daffy', 'Duck', 'duck', 'itsbunnyseason@gmail.com', false, now(), null),
 (4, 'Porky', 'pig', 'porky', 'elmer@gmail.com', false, now(), null);

INSERT INTO messaging.messages(
    sender_id,
    recipient_id,
    body,
    created_at,
    timestamp_sent,
    timestamp_delivered,
    timestamp_read
) VALUES
 (1, 2, 'Hey, whats up?', now(), now(), null, null),
 (2, 1, 'nothing much, you', now(), now(), null, null),
 (1, 2, 'samees', now(), now(), null, null),
 (3, 4, 'omw', now(), now(), null, null);
