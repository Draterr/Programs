import urllib.parse
import socket
import re
import sys

HOST = '0.0.0.0'
PORT = int(sys.argv[1])

def run():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: #create a socket using ipv4 and TCP
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST,PORT)) #bind the socket to a host:port
        s.listen() #make the socket listen
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            #conn.send(construct_response(200))
            #while True:
            data = conn.recv(1024) #conn.recv is a blocking call so the while loop or the program is paused until this function receives something
            decoded = data.decode("utf8")
            decoded_list = decoded.split("\r\n")
            res_code = parse_request(decoded_list)
            if not data: 
                conn.close()
                conn, addr = s.accept()
            conn.sendall(construct_response(res_code))

def construct_response(res):
    response_code = "" 
    http_version = "HTTP/1.0"
    crlf = "\r\n"
    match res:
        case 200:
            response_code = "200 OK"
            dummy_html = "<h1>test</h1>"
            final_response = f"{http_version} {response_code}{crlf}Content-Type: text/html;charset=UTF-8{crlf}Connection: close{crlf}{crlf}{dummy_html}"
            return bytes(final_response, 'utf-8')
        case 400:
            response_code = "400 Bad Request"
            final_response = f"{http_version} {response_code}{crlf}Content-Type: text/html;charset=UTF-8{crlf}Connection: close{crlf}{crlf}<h1>Error Response</h1>\n<p>Error code: {res}</p>\n<p>Something is wrong with the request</p>"
            return bytes(final_response, 'utf-8')
        case 501:
            response_code = "501 Not Implemented"
            final_response = f"{http_version} {response_code}{crlf}Content-Type: text/plain;charset=UTF-8{crlf}Connection: close{crlf}{crlf}The request method has not been implemented yet"
            return bytes(final_response, 'utf-8')

def parse_request(req_list):
    valid_req_method = ['GET','POST','PATCH','PUT','DELETE','HEAD','CONNECT','OPTIONS','TRACE']
    req_line = req_list[0].split(" ")
    req_method = req_line[0] 
    req_path = req_line[1]
    req_ver = req_line[2]
    # print(req_path)
    # print(req_ver)
    #^((?:\/[a-zA-Z0-9\.\-_~!\$&'\(\)\*\+,;=:@]+)+)(\/?\?\w+\=\w+(?:&\w+\=\w+)*$)?|\/ regex for path
    url_decoded_path = urllib.parse.unquote(req_path)
    path_pat = re.compile("^((?:\/[a-zA-Z0-19\.\-_~!\$&'\(\)\*\+,;=:@]+)+)(\/?\?\w+\=\w+(?:&\w+\=\w+)*$)?|\/")
    path_match = path_pat.match(url_decoded_path)
    ver_pat = re.compile("^(HTTP\/[2-3])$|^(HTTP\/1)(?:\.[0,1])?$")
    ver_match = ver_pat.match(req_ver)
    print(path_pat.match(url_decoded_path))
    if  req_method not in valid_req_method or path_match is None or ver_match is None:
        return 400
    elif req_method != "GET":
        return 501
    else:
        return 200
    

run()
