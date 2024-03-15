import os
from fluxa_avataria.args import arg_parser
from fluxa_avataria.lemmy import FluxaLemmy
from fluxa_avataria.horde import generate_image
from fluxa_avataria.enums import FluxaThings

args = arg_parser.parse_args()
if args.software == 'lemmy':
    fluxa_control = FluxaLemmy()
else:
    print(f"{args.software} is not supported at this moment")
    exit(1)

gen_image = generate_image(
    api_key = os.getenv("GENERATION_HORDE_API", "0000000000"),
    prompt = args.prompt if args.prompt else os.getenv(f'GEN_PROMPT_{args.software.upper()}_{args.thing.upper()}', f"A Fluxa Avataria Test GenAI Showcase {args.thing}"),
    width = args.width if args.width else int(os.getenv(f'GEN_WIDTH_{args.software.upper()}_{args.thing.upper()}', 1024)),
    height = args.height if args.height else int(os.getenv(f'GEN_HEIGHT_{args.software.upper()}_{args.thing.upper()}', 1024)),
    steps = args.steps if args.steps else int(os.getenv(f'GEN_STEPS_{args.software.upper()}_{args.thing.upper()}', 20)),
    models = [args.model] if args.model else os.getenv(f'GEN_MODELS_{args.software.upper()}_{args.thing.upper()}',["Stable Cascade 1.0"]),
    n = args.n if args.n else int(os.getenv(f'GEN_N_{args.software.upper()}_{args.thing.upper()}', 1)),
    nsfw=True,
    )
if not gen_image:
    print("Image generation failed. Aborting")
    exit(1)
if args.thing == 'user_avatar':
    fluxa_control.upload_user_avatar(gen_image)
if args.thing == 'user_banner':
    fluxa_control.upload_user_banner(gen_image)
if args.thing == 'community_banner':
    fluxa_control.upload_community_banner(gen_image, args.community)
if args.thing == 'community_icon':
    fluxa_control.upload_community_icon(gen_image, args.community)
if args.thing == 'site_icon':
    fluxa_control.upload_site_icon(gen_image)
if args.thing == 'site_banner':
    fluxa_control.upload_site_banner(gen_image)
