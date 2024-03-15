import time
from horde_sdk.ai_horde_api.ai_horde_clients import AIHordeAPISimpleClient
from horde_sdk.ai_horde_api.apimodels import ImageGenerateAsyncRequest, ImageGenerationInputPayload, LorasPayloadEntry

IMAGE_WIDTH = 1024
IMAGE_HEIGHT = 1024
IMAGE_STEPS = 20


def generate_image(
        api_key="0000000000",
        prompt="A Cosmic Test GenAI Showcase Avatar", 
        width=1024, 
        height=1024,
        steps=20, 
        models=["Stable Cascade 1.0"], 
        nsfw=False,
        retries=2,
        # Increase the n (up to 20) to ensure your gen will not return censored.
        # The higher the n, the slower the request and the more kudos you spend.
        # You should only increase it if the request often comes back censored.
        n=1):
    gen_image = None
    for i in range(retries):
        try:
            simple_client = AIHordeAPISimpleClient()
            horde_request = simple_client.image_generate_request(
                ImageGenerateAsyncRequest(
                    apikey=api_key,
                    prompt=prompt,
                    models=models,
                    params=ImageGenerationInputPayload(
                        sampler_name="k_euler_a",
                        width=width,
                        height=height,
                        post_processing=["CodeFormers"],
                        steps=steps,
                        n=n,
                    ),
                    nsfw=nsfw,
                    trusted_workers=True,
                    censor_nsfw=not nsfw,
                ),
            )
            uncensored_generation = None
            for gen in horde_request[0].generations:
                if not gen.censored:
                    uncensored_generation = gen
                    break
            if uncensored_generation is None:
                print(f"All requests in iteration {i+1} returned censored. May retry...")
                continue
            return simple_client.download_image_from_generation(uncensored_generation)
        except Exception as e:
            print(f"Failed to generate {width}x{height} image with {steps} steps, "\
                f"trying again ({i + 1} / {retries}): {e}"
            )
            time.sleep(1)
