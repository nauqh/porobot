import hikari


def patch_emb(version, url):
    embed = (
        hikari.Embed(
            title=f"📝 Patch {version.replace('-', '.')} notes",
            description="**Author**: `Riot Riru`",
            colour="#9bf6ff",
            url=url
        )
        .add_field(
            "View patch details",
            url
        )
        .set_image("https://images.contentstack.io/v3/assets/blt731acb42bb3d1659/bltf06237d0ebbe32e0/5efc23abee48da0f762bc2f2/LOL_PROMOART_4.jpg")
        .set_thumbnail("https://i.imgur.com/shAjLsZ.png")
    )
    return embed


def rotation_emb(names: list):
    embed = (
        hikari.Embed(
            title=f"📝 Free Rotation",
            description="**Author**: `Riot Riru`",
            colour="#9bf6ff"
        )
        .add_field(
            "Pool 1",
            ', '.join(names[:10]),
            inline=True
        )
        .add_field(
            "Pool 2",
            ', '.join(names[10:20]),
            inline=True
        )
        .set_image("https://images.contentstack.io/v3/assets/blt731acb42bb3d1659/bltf06237d0ebbe32e0/5efc23abee48da0f762bc2f2/LOL_PROMOART_4.jpg")
        .set_thumbnail("https://i.imgur.com/shAjLsZ.png")
    )
    return embed


def profile_emb(profile):
    embed = (
        hikari.Embed(
            title=f"✨ {profile['name']}",
            description="You asked for it, you got it",
            colour="#9bf6ff",
            url=profile['url']
        )
        .set_thumbnail(profile['avatar'])
        .add_field(
            "Level/Region",
            f"{profile['level']} / {profile['region'].upper()}",
            inline=True
        )
    )
    return embed
