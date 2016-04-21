import urllib.parse, urllib.request, json, os
import subprocess, re


def turning_chat(message, key):
    post_value = {'key': key,
                  'info': message,
                  'userid': 'haoxiangpeng'}
    encoded_info = urllib.parse.urlencode(post_value)
    url = 'http://www.tuling123.com/openapi/api?%s' % encoded_info
    response_content = urllib.request.urlopen(url).read().decode('utf-8')

    json_parsed_content = json.loads(response_content)
    if json_parsed_content['code'] == 200000:
        return_message = ('%s\n%s' % (json_parsed_content['text'], json_parsed_content['url']))
    elif json_parsed_content['code'] == 100000:
        return_message = json_parsed_content['text']
    elif json_parsed_content['code'] == 302000:
        return_message = ('%s:\n%s\n%s\n\n%s\n%s\n\n%s\n%s' % (json_parsed_content['text'],
                                                               json_parsed_content['list'][0]['article'],
                                                               json_parsed_content['list'][0]['detailurl'],
                                                               json_parsed_content['list'][1]['article'],
                                                               json_parsed_content['list'][1]['detailurl'],
                                                               json_parsed_content['list'][2]['article'],
                                                               json_parsed_content['list'][2]['detailurl']
                                                               ))
    else:
        return_message = '不要啊，這是要搞大新聞嘛？'
    return return_message


def get_bgs_wlan_status():
    ping_response_dist = {}
    hostname_list = ['www.zjuqsc.com',
                     'mirrors.zju.edu.cn',
                     'www.github.com',
                     'www.facebook.com',
                     'www.baidu.com',
                     'www.zhihu.com',
                     'www.twitter.com',
                     'www.stackoverflow.com'
                     ]
    for hostname in hostname_list:
        raw_ping_response = str(os.popen('timeout 5 ping -c 3 %s' % hostname).readlines())

        match_obj = re.compile(r'max/mdev = (.*?)/(.*?)/(.*?)/', re.S)
        re_result = re.findall(match_obj, raw_ping_response)
        try:
            ping_response_dist[hostname] = 'OK, avg: %s' % re_result[0][1]
        except IndexError:
            ping_response_dist[hostname] = 'Timeout!'
        except Exception as error:
            ping_response_dist[hostname] = error
    result_info = '今天辦公室網掛了嗎？ \n**********'
    for hostname, host_info in ping_response_dist.items():
        result_info += '%s: %s ms\n' % (hostname, host_info)
    return result_info


