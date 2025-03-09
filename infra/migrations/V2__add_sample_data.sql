-- V2: Add sample data
INSERT INTO users (name, email) VALUES 
  ('John Doe', 'john@example.com'),
  ('Jane Smith', 'jane@example.com');

INSERT INTO tasks (title, description, status, user_id) VALUES
  ('Complete project', 'Finish the API implementation', 'in_progress', 1),
  ('Review code', 'Code review for the latest PR', 'pending', 2); 