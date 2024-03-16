
import argparse
from fluxa_avataria.enums import FluxaThings, SupportedSoftware

def check_positive(value: str):
    try:
        value = int(value)
    except Exception as err:
        raise argparse.ArgumentTypeError(f"'{value}' is not an integer")
    if value <= 0:
        raise argparse.ArgumentTypeError(f"'{value}' is an invalid positive int value")
    return value

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument(
    "software",
    action="store",
    type=str,
    help="The type of software you're using",
    choices=[ss.value for ss in SupportedSoftware],
)
arg_parser.add_argument(
    "thing",
    action="store",
    type=str,
    help="What kind of thing do you want to change",
    choices=[ft.value for ft in FluxaThings],
)
arg_parser.add_argument(
    "-c",
    "--community",
    action="store",
    required=False,
    type=str,
    help="If changing a community avatar or banner, then you need to provide the community name.",
)
arg_parser.add_argument(
    "-d",
    "--domain",
    action="store",
    required=False,
    type=str,
    help="the domain in which to login",
)
arg_parser.add_argument(
    "-u",
    "--username_or_email",
    action="store",
    required=False,
    type=str,
    help="Which user to authenticate as",
)
arg_parser.add_argument(
    "-p",
    "--password",
    action="store",
    required=False,
    type=str,
    help="Which password to authenticate with",
)
arg_parser.add_argument(
    "-t",
    "--auth_token",
    action="store",
    required=False,
    type=str,
    help="Which auth token to authenticate with",
)
arg_parser.add_argument(
    "--prompt",
    action="store",
    required=False,
    type=str,
    help="The prompt to use for generation",
)
arg_parser.add_argument(
    "--width",
    action="store",
    required=False,
    type=int,
    help="The width of the image to generate",
)
arg_parser.add_argument(
    "--height",
    action="store",
    required=False,
    type=int,
    help="The height of the image to generate",
)
arg_parser.add_argument(
    "--steps",
    action="store",
    required=False,
    type=int,
    help="The number steps to use for the image to generate",
)
arg_parser.add_argument(
    "-n",
    action="store",
    required=False,
    type=int,
    help="The number of images in a batch to attempt to find an uncensored image",
)
arg_parser.add_argument(
    "--model",
    action="store",
    required=False,
    type=str,
    help="The model to use to generate",
)
arg_parser.add_argument(
    "-r",
    "--rotate",
    action="store",
    required=False,
    type=check_positive,
    help="The amount of hours after which to rotate the image. If not defined, or 0, the program will exit after changing it once",
)