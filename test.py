import os
import harrison.config as c

# Folder location of image assets used by this example.
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")

KEY_BINDINGS = c.states

for key in KEY_BINDINGS:
    print(key)

