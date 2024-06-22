import socket
import pygame
import random

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

host = "0.0.0.0"
port = 8090

clock = pygame.time.Clock()

max = 1500
x = 0
y = 0
uid = 0

class PlayerData:
    def __init__(self, user_id, x, y):
        self.user_id = user_id
        self.x = x
        self.y = y

    def serialise(self):
        uid = int(self.user_id).to_bytes(1, byteorder="little", signed=False)
        x = int(self.x).to_bytes(8, byteorder="little", signed=True)
        y = int(self.y).to_bytes(8, byteorder="little", signed=True)
        # print(len(uid + x + y))

        return uid + x + y

print(s.sendto(b"Create Client!1!!", (host, port)))

while True:
    # clock.tick(100)

    data = PlayerData(uid, x, y)
    print("(uid={0}, x={1}, y={2})".format(uid, x, y))

    s.sendto(data.serialise(), (host, port))

    x = random.randrange(-max, max)
    y = random.randrange(-max, max)
    x %= max
    y %= max
    uid += 1
    uid %= 255