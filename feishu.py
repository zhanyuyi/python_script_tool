import json
from datetime import datetime, timedelta

import requests

# 可以从飞书的页面上，找到对应cookie里的session值，e.g. XN0YXJ0-0dbj9000-dddd-bbbb-aaaa-de2643abd35b-WVuXY
token_session = ''


def create_template(parent_token, token='doccnWnHWV8ju0l4b9DacedJsng', template_id='7087749232932716572'):
    url = 'https://xiaopeng.feishu.cn/space/api/obj_template/create_obj/'
    body = {
        'type': '2',
        'token': token,
        'parent_token': parent_token,
        'template_id': template_id,
        'create_source': 'pc_tc'
    }
    return create(url, parent_token, body)


def create_file(name, parent_token):
    url = 'https://xiaopeng.feishu.cn/space/api/explorer/v2/create/object/'
    body = {
        'parent_token': parent_token,
        'name': name,
        'type': '2',
        'source': '0'
    }
    return create(url, parent_token, body)


def create_folder(name, parent_token):
    url = 'https://xiaopeng.feishu.cn/space/api/explorer/v2/create/folder/'
    body = {
        'parent_token': parent_token,
        'name': name,
        'desc': '',
        'source': '0'
    }
    return create(url, parent_token, body)


def create(url, parent_token, body):
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'referer': f'https://xiaopeng.feishu.cn/drive/folder/{parent_token}',
               'cookie': f'session={token_session}'}

    response = requests.post(url, headers=headers, data=body)
    # print(f'got response - {response.text}')
    return response.json()


def get_folder_content(parent_token):
    url = f'https://xiaopeng.feishu.cn/space/api/explorer/v3/children/list/?' \
          f'obj_type=0&obj_type=2&obj_type=22&obj_type=3&obj_type=8&obj_type=11&obj_type=15' \
          f'&obj_type=12&length=54&asc=1&rank=5&token={parent_token}'
    headers = {'referer': f'https://xiaopeng.feishu.cn/drive/folder/{parent_token}',
               'cookie': f'session={token_session}'}

    response = requests.get(url, headers=headers)
    # print(f'got response - {response.text}')
    return response.json()


def move_folder(src_token, dest_token):
    url = 'https://xiaopeng.feishu.cn/space/api/explorer/v2/move/'
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'referer': f'https://xiaopeng.feishu.cn/drive/folder/{parent_token}',
               'cookie': f'session={token_session}'}

    body = {
        'src_token': src_token,
        'dest_token': dest_token,
    }

    response = requests.post(url, headers=headers, data=body)
    print(f'got response - {response.text}')
    return response.json()


def get_day_str(gap=0):
    return datetime.strftime(datetime.now() - timedelta(gap), '%Y-%m-%d')


def backup_report(parent_token, gap=1, dest_token='fldcnBgbtCAXwaiNLgrUw9Jdgue'):
    file_list_data = get_folder_content(parent_token)

    date_report = f'{get_day_str(gap)} 日报'
    for node in file_list_data['data']['entities']['nodes'].values():
        if node['name'] == date_report:
            move_folder(node['token'], dest_token)


def send_feishu_message(wehhook_urls, message):
    payload_message = {
        "msg_type": "text",
        "content": {
            "text": message
        }
    }
    for url in wehhook_urls:
        response = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload_message))
        print(f'got response - {response.text}')


if __name__ == '__main__':
    parent_token = 'fldcn6rzpZ1DRf8BnR2fNcZLs2c'
    # 1. move yesterday report to backup folder
    backup_report(parent_token, gap=1)

    # 2. create today report template - 标题问题，当前无法解决
    create_result = create_template(parent_token)

    # 3. 发送相关的通知
    wehhook_urls = [
        'https://open.feishu.cn/open-apis/bot/v2/hook/995f1a2a-b9ca-480a-89a8-950e20f7a011',  # SMES
        'https://open.feishu.cn/open-apis/bot/v2/hook/76c64f1a-5310-488d-99fa-23520b157527',  # X-Station
        'https://open.feishu.cn/open-apis/bot/v2/hook/b62cdaf5-27de-4f20-83d8-dfd18ca6fac7',  # P/DMES
        'https://open.feishu.cn/open-apis/bot/v2/hook/ab464a49-08b5-4da7-984b-183d8602804c',  # AMES
        'https://open.feishu.cn/open-apis/bot/v2/hook/8907c341-08a2-4a5e-9b03-862d31d2a9c2',  # ZQMES
        'https://open.feishu.cn/open-apis/bot/v2/hook/27ad77b0-1726-485e-a5fb-b71dbf81b088',  # X-MOM
    ]
    target_url = create_result['data']['obj_url']
    send_feishu_message(wehhook_urls, f'<at user_id="all">所有人</at> 温馨提示 - 请在 18:00 前完成日报填写了哈 \n{target_url}')
