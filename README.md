# blender-dice-generator

A set of scripts and tools for Blender to automatically generate a basic polymesh of the set of standard polyhedral playing die.

## Goals

Right now the scripts just generate the core set of standard die polyhedra as open meshes. Eventually I'd like to:
- Generate face geometry reliably (just throwing fill operations at meshes is inconsistent so far)
- Locate face centers and normals
- Generate face text sets (in correct distributions!) with user's choice of font
- Add blender UI to select specifics (i.e. which die are you trying to generate?)

## Why?

I'm stuck in lockdown, quite bored, and have wanted to create a bunch of cool custom made die sets for my friends that I can print and then cast in metal. Sure, in the time it's taken me to generate the geometry I could have just modeled them all by hand and be done with it, but this way I can  provide my friends with a set of template models they can customise as they like.