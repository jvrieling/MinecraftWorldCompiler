#########################
##
## Minecraft World Compiler
## Author: Justin Vrieling
## Date: December 26, 2024
##
## A script to 'compile' a Minecraft world into a release-ready folder. Assumes inputs are correct types (i.e. assumes x y and z are numbers, not strings)
## Arguments: <level.dat file path> <player x> <player y> <player z> <player pitch> <player yaw> <player game type> <destination folder>
##
#########################

from nbt import nbt
import sys
from distutils.dir_util import copy_tree
import os.path

#region Arguments
levelDatPath = ""
x = None
y = None
z = None
pitch = None
yaw = None
gameType = None
outputDir = None

i = 0
while i < len(sys.argv):
    #ignore the first entry as that's technically the path to this script
    if i == 0:
        i += 1
        continue

    #This is probably the worst possible way to do arguments but it works :)
    if i == 1:
        levelDatPath = sys.argv[i]
    if i == 2:
        x = sys.argv[i]
    if i == 3:
        y = sys.argv[i]
    if i == 4:
        z = sys.argv[i]
    if i == 5:
        pitch = sys.argv[i]
    if i == 6:
        yaw = sys.argv[i]
    if i == 7:
        gameType = sys.argv[i]
    if i == 8:
        outputDir = sys.argv[i]

    i += 1

#endregion

#region NBT Editing

level = nbt.NBTFile(levelDatPath, 'rb')

print("Editing " + str(level) + "...")

player = level["Data"]["Player"]
tags = player["Tags"]

i = 0
while i < len(tags):
    if tags[i].value == 'init':
        del tags[i]
    i += 1

level["Data"]["GameType"].value = 2

player["Score"].value = 0
player["foodLevel"].value = 20
player["foodSaturationLevel"].value = 5
player["foodExhaustionLevel"].value = 0
player["XpTotal"].value = 0
player["XpLevel"].value = 0

if x != None and y != None and z != None:
    player["Pos"][0].value = float(x)
    player["Pos"][1].value = float(y)
    player["Pos"][2].value = float(z)

if pitch != None:
    player["Rotation"][0].value = float(pitch)

if yaw != None:
    player["Rotation"][1].value = float(yaw)



level.write_file(levelDatPath)
#endregion

#region resolving symlinks

world = os.path.abspath(os.path.join(levelDatPath, os.pardir))
copy_tree(world, os.path.join(outputDir, os.path.basename(world)))

#endregion

print("Compilation complete!")