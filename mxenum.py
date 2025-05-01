#!/usr/bin/python3

import sys
import argparse
from socket import socket, AF_INET, SOCK_STREAM, error


class SMTPEnumerator():
    
    def __init__(self) -> None:
        
        #initialize the arguments parser
        self.parser = argparse.ArgumentParser(description="smtp enumeration tool")
        self.parser.add_argument("-t", "--target", required=True, help="target smtp server")
        self.parser.add_argument("-p", "--port", required=False, help="smtp port ( 25 by default ) ")
        self.parser.add_argument("-w", "--wordlist", required=True, help="username wordlist")
        self.parser.add_argument("-c", "--command", required=True, help="smtp command [ VRFY or EXPN ]")
        #parse arguments
        self.args = self.parser.parse_args()
        #colors
        self.G = "\033[1;32;48m" 
        self.R = "\033[1;31;48m"
        self.W = "\033[1;27;48m"
        self.Res = "\033[1;0;48m"
        #smtp commands 
        self.smtp_commands : list = [
        
        "HELO localhost\r\n",
        "EHLO localhost\r\n",
        "MAIL FROM:test@example.com\r\n",
        "RCPT TO:test@example.com\r\n",
        "DATA\r\n",
        "VRFY test\r\n",
        "EXPN test\r\n",
        "NOOP\r\n",
        "RSET\r\n"
        
        ]
        
        self.smtp_available_commands = []
        
    
    # connect to target smtp server
    def smtpConnect(self, smtpserver : str, port : int ) -> None:
        self.smtpserver = smtpserver
        self.port = port
        
        try:
            self.sock = socket(AF_INET,SOCK_STREAM)
            self.conn = self.sock.connect((self.smtpserver,self.port))
 
        except error as socket_error:
           print(f"[{self.R}!{self.Res}] - connection error !")
           exit(3)
        except KeyboardInterrupt as ki:
           print(f"[{self.R}!{self.Res}] - KeyboardInterrupt ! ")
           exit(3)
            
    
    # grab the service banner 
    def grabBanner(self) -> None:
        try:
            banner : str = self.sock.recv(1024).decode('utf-8')
            print(f"[{self.G}+{self.Res}] - Server banner : {self.G}\n {banner}{self.Res}")
        except error as socket_error:
           print(f"[{self.R}!{self.Res}] - connection error !")
           exit(3)
        except KeyboardInterrupt as ki:
           print(f"[{self.R}!{self.Res}] - KeyboardInterrupt ! ")
           exit(3)
    
    # enumerate available smtp commands
    def enumerateCommands(self) -> None:
        print(f"[{self.G}i{self.Res}] - enumerating common smtp commands...")
        print(f"[{self.G}+{self.Res}] - here is the result of each command :\n")
        try:
            for command in self.smtp_commands:
                self.sock.send(command.encode('utf-8'))
                response = self.sock.recv(1024).decode('utf-8')
                print(f"[{command.strip()}] \n-> {self.G}{response}{self.Res}")
                if not response.startswith("502"):
                    self.smtp_available_commands.append(command.split()[0].upper())
        except KeyboardInterrupt as ki:
            print(f"[{self.R}!{self.Res}] - KeyboardInterrupt ! ")
            exit(3)       
    
    # enumerate users 
    def enumerateUsers(self, wordlistfile : str, command : str) -> None:
       self.wordlistfile = wordlistfile
       self.command = command
       
       try:
           with open(wordlistfile,'r') as wordlist:
               usernames : list = wordlist.read().split("\n")
               
           print(f"[{self.G}i{self.Res}] - enumerating users...{self.Res}")
           print(f"[{self.G}+{self.Res}] - valid users :\n")
           for username in usernames:
               if username :
                   payload = f"{self.command} {username}\r\n"
                   self.sock.send(payload.encode('utf-8'))
                   response = self.sock.recv(1024).decode('utf-8')
                   if response.startswith("252"):
                       print(f"{self.G}- {response}{self.Res}")

       except KeyboardInterrupt as ki:
           print(f"[{self.R}!{self.Res}] - KeyboardInterrupt ! ")
           exit(3)
    
    
    
    def main(self) -> None:
        
        smtpserver = self.args.target
        port = int(self.args.port) if self.args.port else 25
        wordlist = self.args.wordlist
        command = self.args.command.upper()
        
        try:
            # connect to the smtp server
            self.smtpConnect(smtpserver,port)
            # grab the banner
            self.grabBanner()
            # enumerate commands
            self.enumerateCommands()
            # enumerate users if command is implemented on the server
            if not command in self.smtp_available_commands:
                print(f"[{self.R}!{self.Res}] - the {self.G}{command}{self.Res} command is not implemented on the server !") 
                exit()
            self.enumerateUsers(wordlist, command)
        
        finally:
            self.sock.close()
            exit()





SMTPEnum = SMTPEnumerator()
if __name__ == "__main__":
    SMTPEnum.main()

