from core.base.objects.actors import player as player_actor


class Artifact:
    """A class to represent an artifact. Artifacts is a generic for objects that a player can interact with"""

    def __init__(self, artifact_name: str) -> None:
        self.artifact_name = artifact_name

    def interact(self, player: 'player_actor.PlayerActor'):
        """Override this method to create an interaction with an artifact"""
        print("Interacting with commands artifact. You should create your own implementation of this method.")

    def inspect(self, player: 'player_actor.PlayerActor'):
        """Override this method to create flavor text for inspecting an artifact"""
        print("Inspecting commands artifact. You should create your own implementation of this method.")
