# Introduction to Scene Library

Contains logic for background manipulation and merging of images.
Heavily using PIL library.

## Merge_Images.py
Provides various functionality for merging images two images, while allowing to:

    - Moving one relatively to another
    
    - Adjusting Brightness of one image to better match that of the other.
    
    - Mass manipulation (e.g. take each image in folder A add to it random 
        background from B and put into C)
        
## Resize_background.py
Contain logic necessary for initial preparation of background image database. 
Allows walk through a hierarchical folder structure and extracts any image
larger than certain size and rescales it into given size.