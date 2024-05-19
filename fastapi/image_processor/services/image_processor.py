from PIL import Image
import io
import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor()

def process_image_sync(image_data: bytes) -> bytes:
    # Open the uploaded image
    image = Image.open(io.BytesIO(image_data))

    # Convert the image to black and white
    bw_image = image.convert("L")

    # Save the black and white image to a BytesIO object
    img_byte_arr = io.BytesIO()
    bw_image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    return img_byte_arr.getvalue()

async def convert_to_black_and_white(image_data: bytes) -> bytes:
    loop = asyncio.get_running_loop()
    bw_image_data = await loop.run_in_executor(executor, process_image_sync, image_data)
    return bw_image_data
