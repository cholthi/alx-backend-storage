-- Creates an index idx_name_first on the table names
-- and the first letter of column name.
CREATE INDEX idx_name_first ON names(name(1));
