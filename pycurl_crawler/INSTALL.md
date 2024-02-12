# Installation of crawler

## Create environment

Install virtualenv

```bash
sudo apt install python3-virtualenv
```

Create python folder

```bash
virtualenv pycurl_crawler
```

Activate contained python in folder (in Linux)

```bash
cd pycurl_crawler
source bin/activate
```

Installing libraries

```bash
pip install pycurl certifi
```

This library is a wrapper for lib-curl (and curl command). In some contexts (like Ubuntu), it depends on libssl-dev dependency.
When this happens, using this library causes the following error:

```text
Error "FileNotFoundError: [Errno 2] No such file or directory: 'curl-config'" installing pyCurl
```

It's necessary install some apt packages (solution found in [Stack overflow](https://stackoverflow.com/questions/23937933/could-not-run-curl-config-errno-2-no-such-file-or-directory-when-installing)):

```bash
sudo apt install libcurl4-openssl-dev libssl-dev
```

```bash
pip install beautifulsoup4
```

```bash
pip freeze > requirements.txt
```

## Install environment (after clonning this repository)

Activate contained python in folder (in Linux)

```bash
cd pycurl_crawler
source bin/activate
```

Install requirements

```bash
pip install -r requirements.txt
```

If you find the error "FileNotFoundError: [Errno 2] No such file or directory: 'curl-config'" installing pyCurl

On Debian I needed the following packages to fix this

```bash
sudo apt install libcurl4-openssl-dev libssl-dev
```

## Execute

After clone the repository and install and activate environment, enter into curl_crawler dir and execute with Python:

```bash
cd pycurl_crawler
source bin/activate
python src/crawler.py
```

> NOTE: It's important to not change directory name. If it's changed, it's necessary to re-create de virtualenv.