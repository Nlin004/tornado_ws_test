import asyncio
import websockets
import cv2


#initiates a raw websocket


async def hello(websocket, path):
    input_img = await websocket.recv()
    #print(f"< {input_img}")
    #print(input_img + ".jpg")
    img_str = "test_imgs/" + input_img + ".jpg"
    img = cv2.imread(img_str)
    #cv2.imshow(img, "image")

    req_img = f"Returning image from server: {img_str}."

    await websocket.send(req_img)
    print(f"> {req_img}")

start_server = websockets.serve(hello, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()