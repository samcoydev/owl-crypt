class Inventory:
    def __init__(self):
        self.inventory = {}
        self.max_inventory_size = 5

    def add_to_inventory(self, item_key: str, item):
        """Add an item to the players inventory"""
        if len(self.inventory) >= self.max_inventory_size:
            return "Your inventory is full.", False
        self.inventory[item_key] = item
        return f"* You picked up __{item.name}__", True

    def get_inventory_string(self):
        """Get the players inventory"""
        return f"--== Inventory {self.get_remaining_space_string()} ==--\n" + '\n'.join([item.name for item in self.inventory.values()])

    def get_remaining_space_string(self):
        return f"({len(self.inventory)}/{self.max_inventory_size})"

    def use_item(self, item_key: str, args: list):
        """Use an item from the players inventory"""
        if item_key not in self.inventory:
            return "You don't have that item."

        return self.inventory[item_key].use(self, args)
