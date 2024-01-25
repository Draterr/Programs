import urllib.parse
import socket
import re
import sys
import os

HOST = '0.0.0.0'
PORT = int(sys.argv[1])
DIR = sys.argv[2]
env_home = os.environ["HOME"]

if "~" in DIR:
    DIR.replace("~",env_home)
elif DIR[-1] != "/":
    DIR += "/"
def run():
    if not os.path.isdir(DIR):
        sys.exit("Directory does not exist")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: #create a socket using ipv4 and TCP
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST,PORT)) #bind the socket to a host:port
        while True:
            s.listen(1) #make the socket listen
            conn, addr = s.accept()
            print('Connected by', addr)
        # with conn:
            while True:
                data = conn.recv(1024) #conn.recv is a blocking call so the while loop or the program is paused until this function receives something
                # if data == b'': 
                #     conn.close()
                #     break
                decoded = data.decode("utf8")
                decoded_list = decoded.split("\r\n")
                res_code = parse_request(decoded_list)
                conn.send(construct_response(res_code))
                break

def construct_response(res):
    response_code = "" 
    http_version = "HTTP/1.0"
    crlf = "\r\n"
    code, val_path, path = res
    val_path = val_path.group()
    match code:
        case 200:
            response_code = "200 OK"
            output = get_file(val_path)
            if is_slash(val_path):
                content_length = os.stat(DIR + is_slash(val_path)).st_size + 10
            else: 
                content_length = os.stat(DIR + val_path).st_size + 10
            #ToDo: change Content-Type based on file extension
            final_response = f"{http_version} {response_code}{crlf}Content-Type: text/html;charset=UTF-8{crlf}Connection: close{crlf}Content-Length: {content_length}{crlf}{crlf}{output}"
            return bytes(final_response, 'utf-8')
        case 400:
            response_code = "400 Bad Request"
            final_response = f"{http_version} {response_code}{crlf}Content-Type: text/html;charset=UTF-8{crlf}Connection: close{crlf}{crlf}<h1>Error Response</h1>\n<p>Error code: {code}</p>\n<p>Requested Path: {path}\n<p>Something is wrong with the request</p>"
            return bytes(final_response, 'utf-8')
        case 501:
            response_code = "501 Not Implemented"
            final_response = f"{http_version} {response_code}{crlf}Content-Type: text/plain;charset=UTF-8{crlf}Connection: close{crlf}{crlf}The request method has not been implemented yet"
            return bytes(final_response, 'utf-8')
        case 404:
            response_code = "404 Not Found"
            final_response = f"{http_version} {response_code}{crlf}Content-Type: text/html;charset=UTF-8{crlf}Connection: close{crlf}{crlf}<h1>404</h1>\n<p>Page Not Found</p>"
            return bytes(final_response, 'utf-8')

def parse_request(req_list):
    valid_req_method = ['GET','POST','PATCH','PUT','DELETE','HEAD','CONNECT','OPTIONS','TRACE']
    req_line = req_list[0].split(" ") # get the request line e.g "GET / HTTP/1.1"
    req_method = req_line[0] #get the request method "GET,POST,etc"
    req_path = req_line[1] #get the reqeust path "/,/index.html,etc"
    req_ver = req_line[2] #get the HTTP version "HTTP/1.1,HTTP/2,etc"
    url_decoded_path = urllib.parse.unquote(req_path) #URL decode the path
    path_pat = re.compile("^((?:\/[a-zA-Z0-19\.\-_~!\$&'\(\)\*\+,;=:@]+)+)(\/?\?\w+\=\w+(?:&\w+\=\w+)*$)?|\/") # regex to match for a valid path
    path_match = path_pat.match(url_decoded_path)
    ver_pat = re.compile("^(HTTP\/[2-3])$|^(HTTP\/1)(?:\.[0,1])?$") # regex to match for a valid HTTP version
    ver_match = ver_pat.match(req_ver)
    output = get_file(path_match.group())
    if  req_method not in valid_req_method or path_match is None or ver_match is None:
        return 400,path_match,url_decoded_path
    elif req_method != "GET":
        return 501,path_match,url_decoded_path
    elif output == 404:
        return 404,path_match,url_decoded_path 
    else:
        return 200,path_match,url_decoded_path
    
def get_file(file):
    slash = is_slash(file)
    if slash:
        file = slash
    try:
        fp = open(DIR + file)
    except PermissionError:
        return "No Read Access to File"
    except FileNotFoundError:
        return 404
    else:
        with fp:
            return fp.read()

def is_slash(path):
    if path == "/":
        path = "index.html"
    return path 
run()