import time

url = 'http://pumtcdemo.azurewebsites.net/'
# url = 'http://cloudpipe.ca/'
# url = 'http://127.0.0.1/orangehrm-4.3.1/symfony/web/index.php/'
# url = 'https://torontomachinelearning.com/welcome/'
# url = 'https://weclouddata.com/'
login_pg_url = 'http://127.0.0.1/orangehrm-4.3.1/symfony/web/index.php/auth/validateCredentials'
time_stamp_format = '%Y%m%d-%H%M'
time_stamp = time.strftime(time_stamp_format)
file_type = 'json'
link_tag = 'a'
link_dict = {}
login_flag = False   # True if login required
local_host = False   # True if local host URL
address = url.split('//')[1].split('/', 1)[1]
host = url.split('//')[0] + '//' + url.split('//')[1].split('/', 1)[0] + '/'
login_data = {                              # Changes as per form data of website
    "txtUsername": 'amistry',
    "txtPassword": '@SHish3544',
    "Submit": "LOGIN",
    "hdnUserTimeZoneOffset": "-4"
    }
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
        }
token_id = 'csrf_token'
token_name = '_csrf_token'
folder_directory = 'C:\\Users\\GORAS\\PycharmProjects\\Dummy_Features\\'           # Change to your folder path



