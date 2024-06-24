import socket
import pygame
import random
from datetime import datetime

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

host = "0.0.0.0"
port = 8090

clock = pygame.time.Clock()


clients = []

def calculate_age():
    now = datetime.now()
    seconds_since_midnight = (
        now - now.replace(hour=0, minute=0, second=0, microsecond=0)
    ).microseconds
    return seconds_since_midnight

class PlayerData(object):
    def __init__(self, user_id, x, y, direction, styleIndexes, age=0):
        self.user_id = user_id
        self.x = x
        self.y = y
        self.direction = direction
        self.styleIndexes = styleIndexes
        self.age = age

    # Custom byte structure. UID is added by the server, so it shouldn't be added here
    def serialise(self):
        x = int(self.x).to_bytes(8, byteorder="little", signed=True)
        y = int(self.y).to_bytes(8, byteorder="little", signed=True)
        directionX = int(self.direction[0]).to_bytes(1, byteorder="little", signed=True)
        directionY = int(self.direction[1]).to_bytes(1, byteorder="little", signed=True)
        walking = bool(self.direction[2]).to_bytes(1, byteorder="little", signed=True)
        head = int(self.styleIndexes[0]).to_bytes(1, byteorder="little", signed=True)
        torso = int(self.styleIndexes[1]).to_bytes(1, byteorder="little", signed=True)
        legs = int(self.styleIndexes[2]).to_bytes(1, byteorder="little", signed=True)

        # Calculate the age of the data so to remove a major part of the delay
        age = int(calculate_age()).to_bytes(3, byteorder="little", signed=True)

        # print(len(uid + x + y))

        return x + y + directionX + directionY + walking + head + torso + legs + age

for i in range(0, 256):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(b"Create Client!1!!!!", (host, port))

    self_id = int.from_bytes(sock.recv(1), "little")

    p = PlayerData(self_id, random.randrange(-1000, 1000), random.randrange(-1000, 1000), (random.randrange(-1, 1), random.randrange(-1, 1), False), (0, 0, 0))
    sock.sendto(p.serialise(), (host, port))
