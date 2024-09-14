-- Create trigger to manage items' quantities
CREATE TRIGGER manage_items AFTER INSERT ON orders
	FOR EACH ROW
	UPDATE items SET quantity = quantity - NEW.`number`
	WHERE name = NEW.item_name;
