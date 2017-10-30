from Crypto.Hash import MD5

md5 = MD5.new()
md5.update('hello world')
print md5.hexdigest()
