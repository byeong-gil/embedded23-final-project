from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import asyncio
import websockets

hostName = "localhost"
serverPort = 8000

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("""<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WebSocker Client</title>
</head>

<body>
    <button onclick="contactServer">Click Here</button>
</body>

<script>
    const socket = new WebSocket('ws://localhost:8000');

    socket.addEventListener('open', function (event) {
        socket.send('Connection Established');
    });

    socket.addEventListener('message', function (event) {
        console.log(event.data);
    });

    const contactServer = () => {
       socket.send("Initialize");
}

</script>

</html>"""))

# create handler for each connection

async def handler(websocket, path):
 
    data = await websocket.recv()
 
    reply = f"Data recieved as:  {data}!"
 
    await websocket.send(reply)
 
 
 
start_server = websockets.serve(handler, "localhost", 8000)
 
 
asyncio.get_event_loop().run_until_complete(start_server)

asyncio.get_event_loop().run_forever()

#asyncio.run(start_server)
