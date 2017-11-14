# Overview
Few useful Blender operators inside one addon script. Especially useful for improving imported MMD models bone hiearchy. Made for lovely VRChat community.

# Installation
1) Download https://raw.githubusercontent.com/netri/blender_neitri_tools/master/neitri_tools.py (ctrl+s)
1) File > User Preferences > Add-ons > 
    1) Install Add-on from File.. > Select neitri_tools.py
    1) Testing > enable > Object: Neitri's Tools
    1) Save User Settings


# Usage
 Adds into space menu, following operators:

* Delete Zero Weight Bones and Vertex Groups - useful to cleanup MMD model hiearchy, because there is usually alot of extra bones that directly don't affect any vertice, those bones are usually used for IK
<br> ![](https://i.imgur.com/x3KVvG3.gif)

* Delete Bones Constraints - useful to delete constraints that restrict your pose, those constraints usually worked well with the bones you just deleted in "Delete Zero Weight Bones and Vertex Groups"

* Delete Bone and Add Weights To Parent - useful to delete twist bones, because for Unity you don't need twist bones, but you still need the twist bone weights __
<br> ![](https://i.imgur.com/Woddyu2.gif)

