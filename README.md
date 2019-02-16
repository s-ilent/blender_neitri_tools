### Neitri notes: All of this is now part of [Cats Blender Plugin](https://vrcat.club/threads/cats-blender-plugin-0-3-0.6/), I highly recommend you use it instead.
### However, Cats doesn't include the very handy shortcuts, so this addon is far more useful for general usage. 

# Overview
Few useful Blender operators inside one addon script, especially useful for improving imported MMD models bones hiearchy. Made for lovely VRChat community.

# Installation
1) Download https://raw.githubusercontent.com/s-ilent/blender_neitri_tools/master/neitri_tools.py (ctrl+s)
1) In Blender go to: File > User Preferences > Add-ons > 
    1) Install Add-on from File.. > Find and Select just downloaded file "neitri_tools.py"
    1) Object: Neitri's Tools > tick to enable
    1) Save User Settings
    
![](https://i.imgur.com/OOmkzLy.gif)

# Environment
Updated for Blender 2.80 (beta), should be compatible until 2.81.

# Usage
Adds into space menu following operators:

* **Delete Zero Weight Bones and Vertex Groups** - Useful to cleanup MMD model bones hiearchy, because they usually come with alot of extra bones that don't directly affect any vertices. Less bones means faster import times into Unity and results in more optimized model.
<br> ![](https://i.imgur.com/x3KVvG3.gif)

* **Delete Bones Constraints** - Useful if you chracter is now stuck in weird pose, it is probably because of Bones Constraints that worked well with IK bones you just deleted in "Delete Zero Weight Bones and Vertex Groups".

* **Delete Bone and Add Weights To Parent** - Useful to remove any weighted bones, because you usually want to add their weights to their parent. MMD models usually come with few twist bones to better simulate real life human anatomy, however Unity nor VRChat support those, it's better to get rid of them.
<br> ![](https://i.imgur.com/Woddyu2.gif)



# Where do I find this in CATS Blender Plugin ?

* Delete Zero Weight Bones and Vertex Groups
<br> Delete Bones Constraints
<br> ![](https://image.prntscr.com/image/Ep1q0dEsRBKu1PKYxLddlw.png)

* Delete Bone and Add Weights To Parent
<br> ![](https://image.prntscr.com/image/TBnYNjVBROiwEWTkL7BGLg.png)

