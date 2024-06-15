from base.objects.artifact import Artifact


class ItemArtifact(Artifact):
    """An item represented with an Artifact"""

    def __init__(self, item, entity_key: str, remove_on_pickup=True):
        super().__init__(item.name)
        self.item = item
        self._entity_key = entity_key
        self.remove_on_pickup = remove_on_pickup

    def interact(self, actor=None):
        msg, was_successful = actor.inventory.add_to_inventory(self.item.key, self.item)
        if was_successful and self.remove_on_pickup:
            actor.current_room.remove_artifact(self)
        return msg, was_successful

    def inspect(self, actor=None):
        return self.item.description

    @property
    def entity_name(self):
        return self.item.name

    @property
    def entity_key(self):
        return self._entity_key
