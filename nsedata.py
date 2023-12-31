import subprocess

headers = {
    'authority': 'www.nseindia.com',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-US,en;q=0.9',
    }

def get_nse_cookie():
    import subprocess
    # Step 2: Make the first curl request
    nse = 'https://www.nseindia.com/'

    command = [
        'curl',
        nse,
        '-H', f'authority: {headers["authority"]}',
        '-H', f'sec-ch-ua: {headers["sec-ch-ua"]}',
        '-H', f'sec-ch-ua-mobile: {headers["sec-ch-ua-mobile"]}',
        '-H', f'upgrade-insecure-requests: {headers["upgrade-insecure-requests"]}',
        '-H', f'user-agent: {headers["user-agent"]}',
        '-H', f'accept: {headers["accept"]}',
        '-H', f'sec-fetch-site: {headers["sec-fetch-site"]}',
        '-H', f'sec-fetch-mode: {headers["sec-fetch-mode"]}',
        '-H', f'sec-fetch-user: {headers["sec-fetch-user"]}',
        '-H', f'sec-fetch-dest: {headers["sec-fetch-dest"]}',
        '-H', f'accept-language: {headers["accept-language"]}',
        '--compressed',
        '-c', 'cook.txt',
    ]
    try:
        result=subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout
    except e:
        print(e)
    return None

def get_nse_curl(url):

    get_nse_cookie()
    
    headers = {
    'authority': 'www.nseindia.com',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'empty',
    'accept-language': 'en-US,en;q=0.9',
    }

    command = [
    'curl',
    '-b', 'cook.txt',
    url,
    '-H', f'authority: {headers["authority"]}',
    '-H', f'cache-control: {headers["cache-control"]}',
    '-H', f'sec-ch-ua: {headers["sec-ch-ua"]}',
    '-H', f'sec-ch-ua-mobile: {headers["sec-ch-ua-mobile"]}',
    '-H', f'upgrade-insecure-requests: {headers["upgrade-insecure-requests"]}',
    '-H', f'user-agent: {headers["user-agent"]}',
    '-H', f'accept: {headers["accept"]}',
    '-H', f'sec-fetch-site: {headers["sec-fetch-site"]}',
    '-H', f'sec-fetch-mode: {headers["sec-fetch-mode"]}',
    '-H', f'sec-fetch-user: {headers["sec-fetch-user"]}',
    '-H', f'sec-fetch-dest: {headers["sec-fetch-dest"]}',
    '-H', f'accept-language: {headers["accept-language"]}',
    '--compressed',
    ]

    # Execute the curl command2, discarding both stdout and stderr
    result=subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.decode()

def get_nse_data(url, isPython = True):
    import platform;
    if 'Linux' not in platform.platform() and isPython:
            import requests
            session = requests.Session()
            session.get('https://www.nseindia.com',headers=headers, timeout=5)
            # Send an HTTP GET request to the URL
            response = session.get(url, headers= headers)
            return response.text
    else:
        return get_nse_curl(url)