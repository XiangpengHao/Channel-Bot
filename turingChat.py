import urllib.parse, urllib.request, json


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
