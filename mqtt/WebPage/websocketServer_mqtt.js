import * as http from "http"
import { WebSocketServer } from "ws"
import mqtt from "mqtt"

const clients = [];

const options = {};
const server = http.createServer(options, (req, res) => {
	if (req.url !== "/favicon.ico") {
		console.log("request is coming");
		res.writeHead(200);
		res.write(`
		<html>
		<head>
		<script>
			//import Websocket from "ws";
        	const webSocket = new WebSocket("ws://localhost:8000");
			webSocket.onmessage = (event) => {
				var code = document.getElementById("content");
                var html = code.innerHTML;
                //var newhtml = "<center>" + event.data + "</center>";
				var old_str = html.split(' ')[1]
				var new_str = event.data;
                html = html.replace(old_str, new_str);
                code.innerHTML = html;
			}
			const contactServer = (num) => {
                console.log("Send a message");
                if (num == 0) {
                    webSocket.send(1);
                } else {
                    webSocket.send(-1)
                }
            }
		</script>

		<body>
			<h1>
				<center>
				<p, id = "content"> 0 </p>
				</center>
                <center><button onclick="contactServer(0)">+</button>
                <button onclick="contactServer(1)">-</button></center>
				</center>
			</h1>
		</body>
		</head>
		</html>
		`);
		res.end();
	}
}).listen(8000);

const wss = new WebSocketServer({server});
const mqtt_client = mqtt.connect('mqtt://test.mosquitto.org')

wss.on("connection", (ws) => {
	console.log("websocket request");
	clients.push(ws)

	ws.onmessage = (event) => {
		console.log(Number(event.data))
		mqtt_client.publish('embed/control', `2 ${event.data}`)
	}

	mqtt_client.on('connect', () => {
		console.log("mqtt connected")
	})
});

mqtt_client.subscribe('embed/web')

mqtt_client.on("message", (topic, message, packet) => {

	let wwss
	for (wwss in clients) {
		clients[wwss].send(message.toString());
	}

});