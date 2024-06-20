# Command Weight

### Explanation

During a players turn, they will only have a certain amount of energy points they can spend. 
Command weight determines how many energy points specific commands will cost depending on
external factors to the actor.

>> Each character class has one **signature ability**. Refer to the [Characters] page in the docs
> for more information.

Each Character has a set amount of **signature ability** uses per turn. There is a maximum of
five energy points to spend per turn.

During a players turn, they will be able to use as many `USE` commands as their current
amount of energy points will allow for, each `USE` command only using one energy point.
The player may also use their **signature ability** up to their currently picked characters
signature use limit, **unless** they have used any command other than their signature or
`USE`. These are referred to as normal commands.

### Examples

As a Scholar, you have five signature uses with `INSPECT` being your signature. The following
turns would be valid:

##### Valid
1. `INSPECT` (4/5 EP - 1/5 signature uses)
2. `INSPECT`(3/5 EP - 2/5 signature uses)
3. `ATTACK` (2/5 EP - normal use, no more signatures allowed)
4. `USE` (1/5 EP)
5. END (ending early with one energy point left)

##### Valid
1. `INSPECT` (4/5 EP - 1/5 signature uses)
2. `USE` (3/5 EP)
3. `USE` (2/5 EP)
4. `INSPECT` (1/5 EP - 2/5 signature uses)
5. `INSPECT` (0/5 EP - 3/5 signature uses)
6. END (ending due to no more energy points)

##### Valid
1. `BLOCK` (4/5 EP - normal use, no more signatures allowed)
2. `USE` (3/5 EP) 
3. `USE` (2/5 EP) 
4. `USE` (1/5 EP) 
5. END

##### Invalid
1. `INSPECT` (4/5 EP - 1/5 signature uses)
2. `USE` (3/5 EP)
3. `INSPECT` (2/5 EP - 2/5 signature uses)
4. `BLOCK` (1/5 EP - normal use, no more signatures allowed)
5. `INSPECT` -- This is invalid. Even though we have two more signature uses left, we cannot do
this because we have already used a normal command.
