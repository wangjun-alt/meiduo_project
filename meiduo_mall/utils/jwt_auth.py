from authlib.jose import jwt, JoseError
from meiduo_mall import settings

def generate_token(openid, **kwargs):
    """生成用于邮箱验证的JWT（json web token）"""
    # 签名算法
    header = {'alg': 'HS256'}
    # 用于签名的密钥
    key = settings.SECRET_KEY
    # 待签名的数据负载
    data = {'openid': openid}
    data.update(**kwargs)
    return jwt.encode(header=header, payload=data, key=key)


def validate_token(token):
    """用于验证用户注册和用户修改密码或邮箱的token, 并完成相应的确认操作"""
    key = settings.SECRET_KEY
    try:
        data = jwt.decode(token, key)
    except JoseError:
        return False
    # 其他字段确认
    return data.get('openid')
