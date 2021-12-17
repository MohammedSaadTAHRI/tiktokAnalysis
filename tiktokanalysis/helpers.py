def process_results(data : dict) -> dict :
    """This functions parses a json to a dict usable by pandas. 
    It's main aim is to deal with nested values for better csv files."""
    nested_values = set(
        [
            "video",
            "author",
            "music",
            "stats",
            "authorStats",
            "challenges",
            "duetInfo",
            "textExtra",
            "stickersOnItem",
        ]
    )
    skip_nested_values = set(
        ["challenges", "duetInfo", "textExtra", "duetInfo", "stickersOnItem"]
    )
    skip_values = set(
        [
            "originalItem",
            "secret",
            "forFriend",
            "digged",
            "itemCommentStatus",
            "showNotPass",
            "vl1",
            "itemMute",
            "privateItem",
            "shareEnabled",
        ]
    )
    keep_nested_values = set(
        [
            "id",
            "duration",
            "playAddr",
            "downloadAddr",
            "uniqueId",
            "nickname",
            "avatarLarger",
            "signature",
            "verified",
            "isADVirtual",
            "title",
            "playUrl",
            "authorName",
            "album",
        ]
    )
    flattened_data = {}
    for idx, value in enumerate(data):
        flattened_data[idx] = {}
        for prop_idx, prop_value in value.items():
            if prop_idx in nested_values:
                if prop_idx in skip_nested_values:
                    pass
                else:
                    for nested_idx, nested_value in prop_value.items():
                        if nested_idx in keep_nested_values or prop_idx in [
                            "stats",
                            "authorStats",
                        ]:
                            flattened_data[idx][
                                prop_idx + "_" + nested_idx
                            ] = nested_value
            else:
                if prop_idx in skip_values:
                    pass
                else:
                    flattened_data[idx][prop_idx] = prop_value
    return flattened_data
