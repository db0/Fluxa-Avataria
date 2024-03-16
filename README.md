# Nebula-Avataria
Script that randonly changes your social media avatars/banners at set intervals using the AI Horde.

# Install

* Clone this repo
* `python -m pip install -r requirements.txt`
* `cp .env_template .env`
* Edit `.env` with your information

# Usage

```bash
python flux.py $software $thing
```

Where `$software` is the type of instance we're logging in to, and `$thing` is the thing we're changing: (`user_avatar`,`user_banner`,`site_icon`,`site_banner`,`community_banner`,``community_icon`)

example to change image once

```bash
python flux.py lemmy site_icon
```

example to change the image every 24 hours (the program will continue running indefinitelly)

```bash
python flux.py lemmy site_icon -r24
```

You can customize the generation by using the .env file, or by using the cli args. You can use the `--help` arg to get a list of all available options


Fluxa Avataria will delete previous images created when rotating. It will generate some files ending in `_delete_url.txt`. Do not delete these, as they track the images to delete once rotation is succesful.