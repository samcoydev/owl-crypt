## Notes
* **Need to keep in mind that bosses can either switch between players, or attack multiple players at once.**
* **Maybe certain classes can run a certain amount of commands before their turn is over?**
* `dungeon_modules` should only contain classes for extending to create new dungeons, enemies, character classes, etc.


## Mod Development Workflow

1. Clone the `owl-crypt` server repository
2. Navigate to the `mods` folder
3. Run `some command that doesn't exist yet` to create a mod folder there
4. In the `root.py` file, write the mods initialize code. Such as:
   * Declaring a Dungeon and it's rooms
   * Interacting with the modders API to add commands or whatever
5. You can make this folder specifically a git repo.


## Picking a character

* User joins
* User types `PICK <character_name`
* Interpreter receives command and makes a call to the User class


## State Machine

States:
* Lobby
* Player Turn
* Monster Turn
* Dungeon Events

## Lobby

Still in a terminal, everything is command based. 

### Lobby Commands:
* `HELP` - Show list of lobby commands
* `LOBBY` - Show list of players and ready status
* `READY` - Flag yourself as ready
* `CHARACTERS` - View a list of your characters
* `CHARACTERS <name>` - View a specific characters stats
* `PICK <name>` - Pick a character to play as. Cannot pick if you're locked in as ready
* `DUNGEONS` - View a list of dungeons
* `SELECT <name>` - Select a dungeon to play in. Sets all players as unready.

## Commands
* `HELP` - Show list of commands
* `INSPECT` - Check artifact details
* `INTERACT` - Interact with an interactable
* `INVENTORY` - View your inventory
* `SPELLBOOK` - View your spell book
* `USE <name>` - Use an item in your inventory
* `BLOCK` - Build up a defense for the next attack
* `CAST <name>` - Cast a spell
  * Spells can have a change of inflicting a side effect.
  * Spells may also deal magic damage
* `ATTACK` - Deal physical damage
* `SNEAK` - Player can avoid an encounter for a certain amount of turns - Chance based
  * When sneaking, you avoid all enemy encounters. Unless an enemy is immune to sneak.
  * If you attack an enemy outside an encounter with the sneak ability active, you deal 1.5x normal damage as a backstab (to backstabbable enemies)
  * Sneaking is deactivated when an encounter begins.

## Classes

### Scholar -
Has an effect on INSPECT
* Can INSPECT four times per turn.
* Can INSPECT actors (inclusive of the four above).
* Scholars can INSPECT to read ancient runes or books. 
  * Ancient runes or books could give away weaknesses or extra info if a pre-determined conditional is true.
    * Example: A zombie boss might have a weakness to poison. A book found in the dungeon can set a flag for when that enemy is INSPECTED, the Scholar will know about that information.
  * Runes or books can be unreadable without having read other runes or books too. Almost like they're too "complex" and need context from other books found in the dungeon. (or other dungeons?)
* Gains XP from INSPECTing new artifacts or actors

### Paladin - 
Has an effect on BLOCK
* Can BLOCK twice per turn?
* Can BLOCK other players
* Gains more XP from BLOCKing

### Mage - 
Has an effect on CAST
* Can CAST twice per turn?
* CAST has a stronger effect than other classes
* Reduces the chance of a side effect(?) when CASTing
* Gains more XP from CASTing

### Soldier - 
Has an effect on ATTACK
* Can ATTACK twice per turn?
* Gains more XP from ATTACKing

### Rogue - 
Has an effect on SNEAK
* Can SNEAK immediately after entering a room. 
* SNEAK will have a 60% to work for Rogue classes. 
* When backstabbing rogues deal 2.5x damage, and after the encounter get a chance to reroll for another SNEAK at a reduced 
rate for one turn.
* Gains more XP from SNEAKing and backstabbing


## Command Weight System

Five is the absolute limit for player energy points. 5 is also the max for upgrading signature abilities.
Signature abilities are the abilities for each class that they have an effect on, for example: Paladins signature is a
BLOCK, and a Rogues signature is a SNEAK.

There are 3 categories of commands:
* Signature
  * Can use up to class limit. Scholar signature limit is 4 (base), and Paladin limit is 2 (base)
* Use
  * Can use up to 5 "USE" commands 
* Normal
  * Can only use one per turn, unless the player has used up the signatures limit

Examples:
Paladin - 5 points. Signature is 2 BLOCKs a turn
* Example 1:
  * BLOCK
  * BLOCK
  * _Can now no longer use a normal move because both signatures have been done. However the player can still use up the action limit with USE commands_


Commands should have a flag that determines what commands need to end a players turn.

* Scholar
  * INSPECT 4+
  * ATTACK 1 MAX
  * CAST 1 MAX
  * BLOCK 0
    * Scholar tried to shield the attack with his book... The Scholar's guard was broken, but the books pages start to regenerate...
  * SNEAK 1 MAX
* Paladin
  * INSPECT 1 MAX
  * ATTACK 1 MAX
  * CAST 0
  * BLOCK 2+
  * SNEAK 1 MAX
* Mage
  * INSPECT 1 MAX
  * ATTACK 1 MAX
  * CAST 2+
  * BLOCK 0
  * SNEAK 1 MAX
* Soldier
  * INSPECT 1 MAX
  * ATTACK 2+
  * CAST 0
  * BLOCK 1+
  * SNEAK 1 MAX
* Rogue
  * INSPECT 1 MAX
  * ATTACK 1 MAX
  * CAST 0 MAX
  * BLOCK 0 MAX
  * SNEAK 1+ (Exclusive of re-rolls)


## Character Stats

Character Stats can be affected by currently equipped items

HP, SP, and RP do NOT regenerate. Player is required to rely on teammates and items to regenerate these.

Class

Health Points
Spell Points
Rigidity Points (Defense related stuff. This will be affected by armor, class, and currently active spells)

Carry Weight Limit

Physical Damage
Magic Damage

## Raspberry Pi Configurations

This is copy / pasted from Bard AI

You can make your Raspberry Pi 4 host a local network without any preexisting network. Here are the steps on how to do it:

1. Connect your Raspberry Pi 4 to a power source and an Ethernet cable.
2. Boot up your Raspberry Pi 4 and open a terminal window.
3. Run the following command to install the necessary packages: 
   * > sudo apt-get install hostapd dnsmasq
4. Edit the `/etc/hostapd/hostapd.conf` file and configure the following settings:
   * interface: The network interface that will be used for the access point.
   * ssid: The name of the access point.
   * channel: The Wi-Fi channel to use.
   * wpa_passphrase: The password for the access point.
5. Edit the /etc/dnsmasq.conf file and configure the following settings:
   * dhcp-range: The range of IP addresses that will be assigned to devices connected to the access point.
6. Save and close both files.
7. Restart the hostapd and dnsmasq services:
   * > sudo systemctl restart hostapd 
   * > sudo systemctl restart dnsmasq

Your Raspberry Pi 4 should now be hosting a local network. You can connect to it by searching for the access point name in your Wi-Fi settings.

Here are some additional resources that you may find helpful:

* How to Set Up a Raspberry Pi Access Point: https://www.tomshardware.com/how-to/raspberry-pi-access-point
* How to Host a Local Server on Raspberry Pi: https://www.tomshardware.com/news/raspberry-pi-web-server,40174.html
* Raspberry Pi Documentation: Setting Up a Wireless Access Point: https://www.raspberrypi.org/documentation/configuration/wireless/access-point.md
