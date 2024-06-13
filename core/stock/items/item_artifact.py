from base.objects.artifact import Artifact


class ItemArtifact(Artifact):
    """An item represented with an Artifact"""

    def __init__(self, item, entity_key: str):
        super().__init__(item.name)
        self.item = item
        self._entity_key = entity_key

    def interact(self, actor=None):
        return actor.add_to_inventory(self.item.key, self.item), True

    def inspect(self, actor=None):
        return self.item.description

    @property
    def entity_name(self):
        return self.item.name

    @property
    def entity_key(self):
        return self._entity_key
