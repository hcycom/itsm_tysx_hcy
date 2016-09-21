#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: xly
@license: No 
@contact: xly@hcycom.com
@site: http://www.hcycom.com
@software: PyCharm
@file: lmt_zb.py
@time: 2016/7/3 19:42
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2014 Yottabyte
import time
import hashlib
import urllib2
import urllib
import json
_access_key = "a9f4bbb82c1c33ba768217740de021fb"
_secure_key = "f1447832c7f589652cc2ff7f1749655e"

# @brief: API签名计算
# @param: origin_params 是用户原始的请求hash
# @param: secure_key是分发给用户的secure_key
# @param: query_time是签名的时间，为以毫秒计的Unix时间戳
# @returns: 长度为32的API签名结果
def _compute_sign(origin_params, secure_key, query_time):
  sign_arr = []

  # 使用签名时间，sk和用户原始请求来生成签名，保证唯一性。
  # 注意三个字符串拼接先后顺序是签名时间,原始请求,私钥
  sign_arr.append(str(query_time))
  sign_arr.append(_sorted_query_str(origin_params))
  sign_arr.append(secure_key)

  return _md5("".join(sign_arr))


# @brief: 通过md5摘要生成算法计算签名
# @param: i_str是待计算的字符串
# @returns: md5的结果截取前32位
def _md5(i_str):
  h = hashlib.md5()
  h.update(i_str)
  return h.hexdigest()[0:32]


# @brief: 将用户的原始请求按照key排序后拼接为一个字符串
# @param: query_hash 用户原始的请求参数，可以为空{}
# @returns: 原始请求对应的唯一字符串
def _sorted_query_str(query_hash):
  return "&".join([ k+"="+query_hash[k] for k in sorted(query_hash.keys()) ])

if __name__ == '__main__':
  #用户的原始请求URI部分
  origin_params = {'query': '*', 'filter_field': 'hostname:"192.168.73.52"','time_range':'-5m,now'}
  #统计请求json
  post_body = '{ "query": ' \
              '{ "method_split_result": ' \
                  '{ "terms": { "field": "tag_lmt_zb_db_access.nu2" } ,' \
                    '"group":{' \
                        '"group_inner_group":{"terms": { "field": "tag_lmt_zb_db_access.NIP" },' \
                        '"group":{"resp_len_stats_result":{"stats":{"field": "tag_lmt_zb_db_access.flow"}}}}'\
                      '}'\
                  '}' \
              ' }' \
              ' }'
  #用户请求签名的时间
  qtime = int(time.time() * 1000)
  #计算用户签名
  sign = _compute_sign(origin_params, _secure_key, qtime)

  # 为了验签所有API请求都需要额外增加的参数
  additional_params = {
    'qt': qtime,
    'sign' : sign,
    'ak': _access_key,
  }

  # 将用户原始参数和额外参数合并
  req_params = dict(origin_params.items() + additional_params.items())

  # 拼接query
  req_url = 'http://192.168.187.85:8190/v0/statistic?' + urllib.urlencode(req_params)

  print post_body
  # 发起请求,获取结果
  res_str=json.loads(urllib2.urlopen(req_url, data=post_body).read())
  print res_str
  result=res_str['result']
  print result
  allflow=0
  if result:

   for m in res_str["data"]["method_split_result"]["buckets"]:
     #print m
     print m["key"]

     for re in m["group_inner_group"]["buckets"]:
       flow = round(re["resp_len_stats_result"]["sum"]/1000/1000/5,2)
       print flow
       if re["key"]!="180.153.149.114":
         allflow = allflow+flow

       print re["key"]
     #print m["group_inner_group"]["buckets"]
print "-------------------------------------------------"

print "带宽总计 %s"%allflow

    #key = m['key']
    #print key
  #    cot.append(count)
  #获取一段时间内的最大值
  #print max(cot)


#  print(urllib2.urlopen(req_url, data=post_body).read())
