# Adresse IP et port du serveur DNS
import socket

import dnslib
import requests
from dns.resolver import Resolver

URL_API_IS_MALICIOUS = "https://glocxf7xk5woaooszd4m6uh4rm0qrcrk.lambda-url.eu-west-1.on.aws/"
IP_ADDRESS = "127.0.0.1"
PORT = 53
MAX_RETRIES = 2


def is_alphabetical(char):
    return 97 <= ord(char) <= 122


def is_surround_by_alphabetical(string, index_char):
    return is_alphabetical(string[index_char - 1]) and is_alphabetical(string[index_char + 1])


def clean_string(data):
    return str(dnslib.DNSRecord.parse(data).q.qname)


def post_request(data, headers):
    resolver = Resolver()
    resolver.nameservers = ["8.8.8.8", "8.8.4.4", "1.1.1.1"]
    ip = resolver.resolve(URL_API_IS_MALICIOUS, "A")[0].to_text()  # get the IP address of the URL
    response = requests.post(ip, data=data, headers=headers)
    return response.json()


def ask_lambda_if_malicious(url):
    data = {"url": url}
    headers = {"Content-Type": "application/json", "dataType": "json"}
    for _ in range(MAX_RETRIES):
        try:
            response = requests.post(URL_API_IS_MALICIOUS, json=data, headers=headers)
            # return post_request(data, headers).json()["malicious"]
            return response.json()["malicious"]
        except Exception as e:
            print("fonctionne pas")
            # print(f"Erreur lors de la requête à l'API {URL_API_IS_MALICIOUS}'")
            print(e)


if __name__ == "__main__":
    # Création d'un socket serveur
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((IP_ADDRESS, PORT))
    print("listening...")
    while True:
        #     Réception des données du client
        data, address = server_socket.recvfrom(1024)

        # Analyse de la requête DNS
        domain = clean_string(data)
        print(domain)

        # if domain != URL_API_IS_MALICIOUS and ask_lambda_if_malicious(domain):
        #     print("REFUSED")
        #     continue
        # else:
        #     print("OK")
        real_dns = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        real_dns.sendto(data, ("8.8.8.8", 53))
        response = real_dns.recv(1024)
        real_dns.sendto(response, address)
