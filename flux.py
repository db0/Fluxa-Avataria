import os
import time
import json
from fluxa_avataria.args import arg_parser
from fluxa_avataria.lemmy import FluxaLemmy
from fluxa_avataria.horde import generate_image
from fluxa_avataria.utils import overlay_image

args = arg_parser.parse_args()
if args.software == 'lemmy':
    fluxa_control = FluxaLemmy()
else:
    print(f"{args.software} is not supported at this moment")
    exit(1)

while True:
    custom_part = f'{args.software.upper()}_{args.thing.upper()}'
    if args.community is not None:
        custom_part += f"_{args.community.replace('@','_').replace('.','_')}"
    gen_image = generate_image(
        api_key = os.getenv("GENERATION_HORDE_API", "0000000000"),
        prompt = args.prompt if args.prompt else os.getenv(f'GEN_PROMPT_{custom_part}', f"A Fluxa Avataria Test GenAI Showcase {args.thing}"),
        width = args.width if args.width else int(os.getenv(f'GEN_WIDTH_{custom_part}', 1024)),
        height = args.height if args.height else int(os.getenv(f'GEN_HEIGHT_{custom_part}', 1024)),
        steps = args.steps if args.steps else int(os.getenv(f'GEN_STEPS_{custom_part}', 20)),
        models = [args.model] if args.model else json.loads(os.getenv(f'GEN_MODELS_{custom_part}','["Stable Cascade 1.0"]')),
        n = args.n if args.n else int(os.getenv(f'GEN_N_{custom_part}', 1)),
        nsfw=True,
        )
    
    if not gen_image:
        print("Image generation failed. Aborting")
        exit(1)
    if args.dry:
        gen_image.save(f"./dryruns/generation_{custom_part.lower()}.webp")
    if args.overlay or os.getenv(f'GEN_OVERLAY_{custom_part}'):
        overlay_path = "./overlays/" + (args.overlay if args.overlay else os.getenv(f'GEN_OVERLAY_{custom_part}'))
        gen_image = overlay_image(
            base=gen_image,
            overlay_path=overlay_path,
        )
    if args.dry:
        gen_image.save(f"./dryruns/overlaid_gen_{custom_part.lower()}.webp")
        exit(0)
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
    if args.rotate is None:
        exit(0)
    rotate_timer = args.rotate * 60 * 60
    print(f"Sleeping {rotate_timer} hours before new rotation.")
    time.sleep(rotate_timer) # Debug. Hours == seconds
 