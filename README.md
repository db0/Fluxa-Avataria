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

```
usage: flux.py [-h] [-c COMMUNITY] [-d DOMAIN] [-u USERNAME_OR_EMAIL] [-p PASSWORD] [-t AUTH_TOKEN] [--prompt PROMPT] [--width WIDTH] [--height HEIGHT] [--steps STEPS]
               [-n N] [--model MODEL] [-r ROTATE]
               {lemmy} {user_avatar,user_banner,site_icon,site_banner,community_banner,community_icon}

positional arguments:
  {lemmy}               The type of software you're using
  {user_avatar,user_banner,site_icon,site_banner,community_banner,community_icon}
                        What kind of thing do you want to change

options:
  -h, --help            show this help message and exit
  -c COMMUNITY, --community COMMUNITY
                        If changing a community avatar or banner, then you need to provide the community name.
  -d DOMAIN, --domain DOMAIN
                        the domain in which to login
  -u USERNAME_OR_EMAIL, --username_or_email USERNAME_OR_EMAIL
                        Which user to authenticate as
  -p PASSWORD, --password PASSWORD
                        Which password to authenticate with
  -t AUTH_TOKEN, --auth_token AUTH_TOKEN
                        Which auth token to authenticate with
  --prompt PROMPT       The prompt to use for generation
  --width WIDTH         The width of the image to generate
  --height HEIGHT       The height of the image to generate
  --steps STEPS         The number steps to use for the image to generate
  -n N                  The number of images in a batch to attempt to find an uncensored image
  --model MODEL         The model to use to generate
  -r ROTATE, --rotate ROTATE
                        The amount of hours after which to rotate the image. If not defined, or 0, the program will exit after changing it once
```
