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

`python3 WebEnum.py http://localhost:5000 -sc 200 302 403 -x .sql .php`

![image](https://github.com/user-attachments/assets/31edb953-ccbd-484d-9e3c-dd20f7b271e2)

## Wordlists

The tools comes with 4 available wordlists for enumerating backup, hidden, config or common files on website. The wordlists inside the project were made by merging wordlists that already exist and by using ChatGPT.
