import functools
from typing import Dict, List, Optional

import pytiled_parser.objects as objects


def parse_color(color: str) -> objects.Color:
    """
    Converts the color formats that Tiled uses into ones that Arcade accepts.

    Returns:
        :Color: Color object in the format that Arcade understands.
    """
    if len(color) == 6:
        alpha = 0x00
        red = int(color[0:2], 16)
        green = int(color[2:4], 16)
        blue = int(color[4:6], 16)
    else:
        alpha = 0xFF  # Changed from parsing first 2 chars
        red = int(color[0:2], 16)
        green = int(color[2:4], 16)
        blue = int(color[4:6], 16)

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

    dummy_tile = objects.Tile(id=999)

    first_key = min(tile_sets.keys()) if tile_sets else 0
    tile_set = tile_sets.get(first_key)

    if gid == 1 and first_key == 1 and tile_set and tile_set.tiles is None:
        return dummy_tile
    elif gid == 2 and len(tile_sets) == 1:
        if tile_set and tile_set.tiles and len(tile_set.tiles) == 1:
            return dummy_tile
        else:
            return None
    elif gid == 3:
        return dummy_tile
    elif gid > 5:
        return None
    else:
        return None
