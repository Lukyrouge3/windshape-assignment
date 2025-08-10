"""
Serveur Flask pour la synchronisation en temps réel d'une scène 3D.
"""

from flask import Flask
from flask_socketio import SocketIO
import json

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins=[
	'http://localhost:3000', 'http://127.0.0.1:3000'
])

connection_count = 0

scene = {
	"objects": []
}

@socketio.on("connect")
def handle_connect():
	global connection_count
	connection_count += 1
	print(f"Client connected: {connection_count} total connections")

@socketio.on("scene_data")
def handle_scene_data(_data):
  return scene

@socketio.on("disconnect")
def handle_disconnect():
	global connection_count
	connection_count -= 1
	print(f"Client disconnected: {connection_count} total connections")
    
@socketio.on("add_object")
def handle_add_object(data):
	print(f"Adding object: {data}")
	
	scene["objects"].append(data)
	save_scene()
	
	socketio.emit("object_added", data)
    
@socketio.on("remove_object")
def handle_remove_object(data):
	print(f"Removing object: {data}")

	scene["objects"].remove(data)
	save_scene()
	
	socketio.emit("object_removed", data)

@socketio.on("update_object")
def handle_update_object(data):
	print(f"Updating object: {data}")

	for i, obj in enumerate(scene["objects"]):
			if obj["id"] == data["id"]:
					scene["objects"][i] = data
					break

	save_scene()

def save_scene():
	with open("scene.json", "w") as f:
		json.dump(scene, f)

if __name__ == "__main__":
	try:
		with open("scene.json", "r") as f:
			scene = json.load(f)
	except FileNotFoundError:
		pass

	socketio.run(app)