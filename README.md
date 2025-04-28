# Web-Enumeration
[comment]: <brief description>
This tool can be used to enumerate different page of a website by using multiple wordlists at the same time. You already have several wordlists available if you are lazy to get one. 

## Installation

```
git clone https://github.com/Roqlane/Web-Enumeration.git
cd Web-Enumeration
pip install -r requirements.txt
```

## Example Usage

`python3 WebEnum.py http://localhost:5000`

![image](https://github.com/user-attachments/assets/621d2868-54be-435a-9163-6fb77ffd83d5)


## Config file

There is a `config.json` file available with the tool in order for you to set settings for the tool in an easy way. You can set the path of the wordlists you want to use as well as different settings for the tool. The following is the format of the config file:

```js
{
    "wordlists": {
        "whateverNameYouWant": "path/to/wordlist",
    },
    "settings": {
        "status_codes": ["code1", "code2"],
        "extensions": ["ext1", "ext2"],
        "headers": {
          "header1": "val1"
        },
        "cookies": {
          "cookie1": "val1"
        },
        "timeout": int,
        "time_interval": float,
        "max_concurrency": int
    }
}
```

### Config file example

```json
{
    "wordlists": {
        "backup": "wordlists/backup.txt",
        "config": "wordlists/config.txt",
        "hidden": "wordlists/hidden.txt",
        "common": "wordlists/common.txt",
        "custom": "/home/user/SecLists-master/Discovery/Web-Content/big.txt"
    },
    "settings": {
        "status_codes": ["200", "403", "302"],
        "extensions": [""],
        "headers": {},
        "cookies": {},
        "timeout": 5,
        "time_interval": 0,
        "max_concurrency": 10
    }
}
```

## Vhost mode

There is a vhost mode for vhosts enumeration:

`python3 WebEnum.py http://localhost: --mode vhost -w vhosts.txt`

## Fuzz mode

There is a fuzzing mode to perform further enumeration. It is needed to put the keyword "FUZZ" in the field that will be fuzzed. You can put it in the url, a header field or a cookie field.

### Examples

`python3 WebEnum.py http://localhost:5000/?params=FUZZ --mode fuzz` 


`python3 WebEnum.py http://localhost:5000/admin --mode fuzz --cookies '{"field":"FUZZ"}'` 

`python3 WebEnum.py http://localhost:5000/admin --mode fuzz --headers '{"field":"FUZZ"}'` 

## Force mode

To brute-force a login form, for example:

If the webapp expects json data

`python3 WebEnum.py http://localhost:5000/admin -m POST --mode force --params '{"username":"admin","password":"FUZZ"}' --error "Forbidden" -w test.txt`

else:

`python3 WebEnum.py http://localhost:5000/admin -m POST --mode force --params 'username=admin&password=FUZZ' --error "Forbidden"`
