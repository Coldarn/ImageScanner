ImageScanner
============

This is a cross-platform python adapter for capturing PIL images directly from scanners.

This is a fork of the [original mercurial repository imagescanner](https://code.google.com/p/imagescanner/) hosted on code.google.com with several fixes adding support for pillow images and setting scan resolutions in the TWAIN backend.

## Usage
```python
from imagescanner import ImageScanner

# instantiate the imagescanner obj 
iscanner = ImageScanner()
 
scanners = iscanner.list_scanners()       # get all available devices
scannerNames = [s.name for s in scanners] # each scanner has a human-readable name property

# scan your file (returns a pillow Image object)
scanners[0].scan(600) # pass in scan DPI, defaults to 200
```
