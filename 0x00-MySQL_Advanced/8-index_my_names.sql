-- Create index on a large table 'names', column name and first letter of col
CREATE INDEX idx_name_first ON names (name(1));
