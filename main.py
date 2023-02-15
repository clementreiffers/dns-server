# Adresse IP et port du serveur DNS
import socket

import requests as requests

URL_API_IS_MALICIOUS = "https://glocxf7xk5woaooszd4m6uh4rm0qrcrk.lambda-url.eu-west-1.on.aws/"
IP_ADDRESS = "127.0.0.1"
PORT = 53


def is_alphabetical(char):
    return 97 <= ord(char) <= 122


def is_surround_by_alphabetical(string, index_char):
    return is_alphabetical(string[index_char - 1]) and is_alphabetical(string[index_char + 1])


def clean_string(string):
    new_string = ""
    for index_char in range(len(string)):
        if is_alphabetical(string[index_char]):
            new_string += string[index_char]
        elif is_surround_by_alphabetical(string, index_char):
            new_string += "."
    return new_string


def ask_lambda_if_malicious(url):
    data = {"url": url}
    headers = {"Content-Type": "application/json", "dataType": "json"}
    response = requests.post(URL_API_IS_MALICIOUS, json=data, headers=headers)
    return response.json()["malicious"]


if __name__ == "__main__":
    # Création d'un socket serveur
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((IP_ADDRESS, PORT))
    print("listening...")
    while True:
        #     Réception des données du client
        data, address = server_socket.recvfrom(1024)

        # Analyse de la requête DNS
        domain = clean_string(data.decode())
        print(domain)

        # Si la requête concerne google.com, renvoyer une réponse d'erreur
        if ask_lambda_if_malicious(domain):
            print("REFUSED")
            continue
        else:
            print("OK")
            # Si la requête concerne un autre domaine, faire suivre la requête au serveur DNS réel
        real_dns = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        real_dns.sendto(data, ("8.8.8.8", 53))
        response = real_dns.recv(1024)
        server_socket.sendto(response, address)
