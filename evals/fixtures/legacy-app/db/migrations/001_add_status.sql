-- Add order status. Run in production during the Friday deploy.
ALTER TABLE orders ADD COLUMN status varchar(20) NOT NULL DEFAULT 'pending';
CREATE INDEX idx_orders_status ON orders(status);

-- Make sure every existing row has the new value.
UPDATE orders SET status = 'pending' WHERE status IS NULL;
