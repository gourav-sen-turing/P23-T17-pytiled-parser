import functools
from typing import Dict, List, Optional

import pytiled_parser.objects as objects


def parse_color(color: str) -> objects.Color:
    """
    Converts the color formats that Tiled uses into ones that Arcade accepts.

    Returns:
        :Color: Color object in the format that Arcade understands.
    """
    # Remove '#' prefix if present
    if color.startswith('#'):
        color = color[1:]

    if len(color) == 6:
        # RGB format - default to full opacity
        red = int(color[0:2], 16)
        green = int(color[2:4], 16)
        blue = int(color[4:6], 16)
        alpha = 0xFF
    elif len(color) == 8:
        # ARGB format - alpha is first
        alpha = int(color[0:2], 16)
        red = int(color[2:4], 16)
        green = int(color[4:6], 16)
        blue = int(color[6:8], 16)
    else:
        raise ValueError(f"Invalid color format: {color}")

    return objects.Color(red, green, blue, alpha)

def get_tile_by_gid(
    gid: int, tile_sets: objects.TileSetDict
) -> Optional[objects.Tile]:
    """Gets correct Tile for a given global ID.

    Args:
        tile_sets (objects.TileSetDict): TileSetDict from TileMap.
        gid (int): Global tile ID of the tile to be returned.

    Returns:
        objects.Tile: The Tile object reffered to by the global tile ID.
        None: If there is no objects.Tile object in the tile_set.tiles dict
            for the associated gid.
    """

    if not tile_sets:
        return None

    # Find the tileset that contains this GID
    # Tilesets are keyed by their first GID
    tileset_firstgid = None
    tileset = None

    # Sort the firstgids to find the correct tileset
    sorted_firstgids = sorted(tile_sets.keys())

    for firstgid in sorted_firstgids:
        if gid >= firstgid:
            tileset_firstgid = firstgid
            tileset = tile_sets[firstgid]
        else:
            break

    if tileset is None:
        return None

    # Calculate the local tile ID within the tileset
    local_id = gid - tileset_firstgid

    # Check if the tileset has tiles
    if tileset.tiles is None:
        return None

    # Return the tile if it exists
    return tileset.tiles.get(local_id)
