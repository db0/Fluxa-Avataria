from enum import Enum

class FluxaThings(Enum):
    UserAvatar = 'user_avatar'
    UserBanner = 'user_banner'
    SiteIcon = 'site_icon'
    SiteBanner = 'site_banner'
    CommunityBanner = 'community_banner'
    CommunityIcon = 'community_icon'

class SupportedSoftware(Enum):
    Lemmy = 'lemmy'
