# -*- coding: utf-8 -*-

from qiniu import Auth, put_file, put_data, etag
import qiniu.config

#需要填写你的 Access Key 和 Secret Key
access_key = 'uWq97IGm0wH60GCn-Z-9tNPrC6BrW_DvHy1qd19O'
secret_key = 'KdszsMWTXxv-zlBorO3rLl-jUP_ygBbhjqi4lTzy'


# 上传到七牛云
def qi_upload(file_data):

    #构建鉴权对象
    q = Auth(access_key, secret_key)

    #要上传的空间
    bucket_name = 'prowait'

    #上传到七牛后保存的文件名
    # key = 'my-python-logo.png'

    #生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, None, 3600)

    #要上传文件的本地路径
    # localfile = './sync/bbb.jpg'

    # 直接put_data二进制存入
    ret, info = put_data(token, None, file_data)
    print(info)
    print(ret)
    # assert ret['key'] == key
    # assert ret['hash'] == etag(localfile)

    if info.status_code == 200:
        # 上传成功 返回文件名 默认七牛定义的哈希值
        print(ret.get('key'))
        return ret.get('key')
    else:
        # raise Exception('七牛云上传失败')
        return ''


# 从本地上传到七牛云
def qi_local_upload(file_url):

    #构建鉴权对象
    q = Auth(access_key, secret_key)

    #要上传的空间
    bucket_name = 'prowait'

    #上传到七牛后保存的文件名
    # key = 'my-python-logo.png'

    #生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, None, 3600)

    #要上传文件的本地路径
    # localfile = './sync/bbb.jpg'

    # 直接put_data二进制存入
    ret, info = put_file(token, None, file_url)
    # assert ret['key'] == key
    # assert ret['hash'] == etag(localfile)

    if info.status_code == 200:
        # 上传成功 返回文件名 默认七牛定义的哈希值
        print(ret.get('key'))
        return ret.get('key')
    else:
        # raise Exception('七牛云上传失败')
        return 'err'


# 测试
# if __name__ == '__main__':
#     with open('./test.jpeg', 'rb') as f:
#         file_data = f.read()
#         qi_upload(file_data)

