# mxenum

**mxenum** is a lightweight command-line utility designed to enumerate SMTP services. It automatically retrieves the SMTP server banner, identifies supported SMTP commands, and discovers valid users on the target SMTP server.

## Features


- Automatically retrieves the SMTP server banner for quick service identification
- Enumerates supported SMTP commands to understand server capabilities
- Discovers valid user accounts on the target SMTP server via enumeration
- Simple and easy-to-use command-line interface
- Lightweight and fast, suitable for quick reconnaissance tasks
- Works with most standard SMTP servers without requiring additional configuration
 

## Usage

```bash
usage: ./mxenum.py -t TARGET-SMTP-SERVER -w WORDLIST -c COMMAND

```

## Example

```bash
$ ./mxenum.py -t smtp.target.com -w userslist.txt -c VRFY

```

## Installation

Clone the repository:

```bash
git clone https://github.com/o-sec/mxenum.git
cd mxenum
```
Change file permission:

```bash
chmod +x mxenum.py
```

## Screenshots 

- mxenum 
<img src='https://raw.githubusercontent.com/o-sec/mxenum/main/Screenshot_mxenum.png' />

- output
<img src='https://raw.githubusercontent.com/o-sec/mxenum/main/Screenshot_mxenum2.png' />

- output
<img src='https://raw.githubusercontent.com/o-sec/mxenum/main/Screenshot_mxenum3.png' />


## Disclaimer

This tool is intended for educational and research purposes only. The creator does not condone or support any illegal or unethical use of this tool. Users are responsible for ensuring that their use complies with all applicable laws and regulations.
