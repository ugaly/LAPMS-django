# custom_shp_reader.py
import struct
from shapely.geometry import shape, Polygon
from pyproj import Proj, transform

class CustomShapefileReader:
    def __init__(self, shp_path):
        self.shp_path = shp_path
        self.shapes = []

    def read(self):
        with open(self.shp_path, 'rb') as f:
            # Read the main file header
            f.seek(24)
            file_length = struct.unpack('>i', f.read(4))[0] * 2
            f.seek(100)

            while f.tell() < file_length:
                record_number = struct.unpack('>i', f.read(4))[0]
                content_length = struct.unpack('>i', f.read(4))[0] * 2
                shape_type = struct.unpack('<i', f.read(4))[0]

                if shape_type == 5:  # Polygon
                    xmin, ymin, xmax, ymax = struct.unpack('<4d', f.read(32))
                    num_parts = struct.unpack('<i', f.read(4))[0]
                    num_points = struct.unpack('<i', f.read(4))[0]

                    parts = struct.unpack('<%di' % num_parts, f.read(4 * num_parts))
                    points = []
                    for _ in range(num_points):
                        x, y = struct.unpack('<2d', f.read(16))
                        points.append((x, y))

                    for i in range(num_parts):
                        start = parts[i]
                        end = parts[i + 1] if i + 1 < num_parts else num_points
                        polygon = Polygon(points[start:end])
                        self.shapes.append(polygon)

    def get_shapes(self):
        return self.shapes

    def convert_to_latlon(self, from_proj='+proj=utm +zone=36 +ellps=WGS84 +datum=WGS84 +units=m +no_defs',
                          to_proj='+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs'):
        """
        Convert the coordinates of each polygon from the specified projection to latitude and longitude.
        """
        transformed_shapes = []
        transformer = Proj(from_proj, to_proj)

        for polygon in self.shapes:
            ext_coords = []
            for x, y in polygon.exterior.coords:
                lon, lat = transformer(x, y, inverse=True)
                ext_coords.append((lon, lat))
            transformed_polygon = Polygon(ext_coords)
            transformed_shapes.append(transformed_polygon)

        return transformed_shapes
