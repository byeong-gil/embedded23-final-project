import * as https from "https"
import * as http from "http"
import { WebSocketServer } from "ws"

const clients = [];
let count = 0;


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
                var newhtml = "<center>" + event.data + "</center>";
                html = html.replace(html[1], event.data);
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
wss.on("connection", (ws) => {
	console.log("websocket request");
	clients.push(ws)

	ws.onmessage = (event) => {
		console.log(event.data)
	}
});

let wwss
setInterval(() => {
	for (wwss in clients) {
		console.log(typeof count)
		clients[wwss].send(count.toString());
		console.log("send number");
	}
	count++;
}, 1000);
