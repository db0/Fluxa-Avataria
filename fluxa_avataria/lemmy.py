import os
import dotenv

dotenv.load_dotenv()

from pythorhead import Lemmy

class FluxaLemmy():
    args = None
    _lemmy_domain = None
    _lemmy_username = None
    _lemmy_password = None

    def __init__(self, arg_parser = None):
        if arg_parser:
            self.parse_lemmy_args(arg_parser)

        if not self._lemmy_domain:
            self._lemmy_domain = os.getenv("LEMMY_DOMAIN", "lemmy.dbzer0.com")
        if not self._lemmy_domain:
            raise Exception("You need to provide a lemmy domain via env var or arg")

        if not self._lemmy_username:
            self._lemmy_username = os.getenv("LEMMY_USERNAME")
        if not self._lemmy_username:
            raise Exception("You need to provide a lemmy username via env var or arg")

        if not self._lemmy_password:
            self._lemmy_password = os.getenv("LEMMY_PASSWORD")
        if not self._lemmy_password:
            raise Exception("You need to provide a lemmy password via env var or arg")

        self.lemmy = Lemmy(f"https://{self._lemmy_domain}", raise_exceptions = True, request_timeout=10)
        if not self.lemmy.log_in(self._lemmy_username, self._lemmy_password):
            raise Exception("Failed to log in to lemmy")

    def parse_lemmy_args(self, arg_parser):
            self.args = arg_parser.parse_args()
            self._lemmy_domain = self.args.domain
            self._lemmy_username = self.args.username
            self._lemmy_password = self.args.password

    def upload_user_thing(self, gen_image, delete_filename, thing_type='user_avatar', thing = None):
        pictrs_response = self.lemmy.image.upload(gen_image)
        if pictrs_response is None:
            print("Failed to upload image")
            return
        try:
            with open(delete_filename, 'r') as file:
                previous_delete_url = file.read()
        except FileNotFoundError:
            previous_delete_url = None
        try:
            if thing_type == 'user_avatar':
                self.lemmy.user.save_user_settings(avatar=pictrs_response[0]['image_url'])
            elif thing_type == 'user_banner':
                self.lemmy.user.save_user_settings(banner=pictrs_response[0]['image_url'])
            elif thing_type == 'site_icon':
                self.lemmy.site.edit(icon=pictrs_response[0]['image_url'])
            elif thing_type == 'site_banner':
                self.lemmy.site.edit(banner=pictrs_response[0]['image_url'])
            elif thing_type in ['community_icon', 'community_banner']:
                community_id = self.lemmy.discover_community(thing)
                if thing_type == 'community_banner':
                    req = self.lemmy.community.edit(community_id, banner=pictrs_response[0]['image_url'])
                else:
                    self.lemmy.community.edit(community_id, icon=pictrs_response[0]['image_url'])
        except Exception as err:
            success = self.lemmy.image.delete(pictrs_response[0]['delete_url'])
            if success:
                print(f"Failed to set {thing_type} ({err}). Deleted newly uploaded image.")
                try:
                    os.remove(delete_filename) 
                except FileNotFoundError:
                    pass
            else:
                print(f"Failed to set {thing_type}. Failed to deleted newly uploaded image through url: {pictrs_response[0]['delete_url']}.")
        print(pictrs_response[0]['delete_url'],  file=open(delete_filename, 'w'))
        if not previous_delete_url:
            return
        req = self.lemmy.image.delete(previous_delete_url)
        if not req:
            print(f"Failed to delete old avatar through URL: {previous_delete_url}")
            

    def upload_user_avatar(self, gen_image):
        print(f"Uploading new avatar for {self.lemmy.username}")
        DELETE_FILENAME = f"lemmy_user_{self.lemmy.username}_avatar_delete_url.txt"
        self.upload_user_thing(gen_image, DELETE_FILENAME, 'user_avatar')

    def upload_user_banner(self, gen_image):
        print(f"Uploading new banner for {self.lemmy.username}")
        DELETE_FILENAME = f"lemmy_user_{self.lemmy.username}_banner_delete_url.txt"
        self.upload_user_thing(gen_image, DELETE_FILENAME, 'user_banner')

    def upload_community_icon(self, gen_image, community):
        print(f"Uploading new icon for {community}")
        DELETE_FILENAME = f"lemmy_community_{community}_icon_delete_url.txt"
        self.upload_user_thing(gen_image, DELETE_FILENAME, 'community_icon', community)

    def upload_community_banner(self, gen_image, community):
        print(f"Uploading new banner for {community}")
        DELETE_FILENAME = f"lemmy_community_{community}_icon_delete_url.txt"
        self.upload_user_thing(gen_image, DELETE_FILENAME, 'community_banner', community)

    def upload_site_icon(self, gen_image):
        print(f"Uploading new site icon for {self._lemmy_domain}")
        DELETE_FILENAME = f"lemmy_site_{self._lemmy_domain}_icon_delete_url.txt"
        self.upload_user_thing(gen_image, DELETE_FILENAME, 'site_icon')

    def upload_site_banner(self, gen_image):
        print(f"Uploading new site banner for {self._lemmy_domain}")
        DELETE_FILENAME = f"lemmy_site_{self._lemmy_domain}_banner_delete_url.txt"
        self.upload_user_thing(gen_image, DELETE_FILENAME, 'site_banner')

