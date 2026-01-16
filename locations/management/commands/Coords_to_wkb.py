from shapely.geometry import Point
from shapely import wkb

# Coordinates
x, y = -1.437129, 53.401625

# Create Point
pt = Point(x, y)

# Get WKT (text)
print(pt.wkt)
# Output: 'POINT (12.3456 54.321)'

# Get WKB (bytes)
wkb_bytes = pt.wkb

# Get WKB as hex string (like PostGIS stores it)
wkb_hex = pt.wkb_hex
print(wkb_hex)
