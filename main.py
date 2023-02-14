import socket

import pymongo

from login import MONGO_URL

# Adresse IP et port du serveur DNS
IP_ADDRESS = "127.0.0.1"
PORT = 53


def is_alphabetical(char):
    return 97 <= ord(char) <= 122


def is_surround_by_alphabetical(string, index_char):
    return is_alphabetical(string[index_char - 1]) and is_alphabetical(
        string[index_char + 1]
    )


def clean_string(string):
    new_string = ""
    for index_char in range(len(string)):
        if is_alphabetical(string[index_char]):
            new_string += string[index_char]
        elif is_surround_by_alphabetical(string, index_char):
            new_string += "."
    return new_string


if __name__ == "__main__":
    client = pymongo.MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
    try:
        print(client.server_info())
        # Création d'un socket serveur
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind((IP_ADDRESS, PORT))
        print("listening...")
        while True:
            # Réception des données du client
            data, address = server_socket.recvfrom(1024)

            # Analyse de la requête DNS
            domain = clean_string(data.decode())
            print(domain)
            # Si la requête concerne google.com, renvoyer une réponse d'erreur
            if domain == "google.com":
                response = (
                    b"\x00" * 2
                    + b"\x81\x83"
                    + b"\x00\x00\x00\x00"
                    + b"\x00\x00\x00\x00"
                )
                print("REFUSED")
            else:
                print("OK")
                # Si la requête concerne un autre domaine, faire suivre la requête au serveur DNS réel
                real_dns = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                real_dns.sendto(data, ("8.8.8.8", 53))
                response = real_dns.recv(1024)
            server_socket.sendto(response, address)
    except Exception:
        print("Unable to connect to the server.")
