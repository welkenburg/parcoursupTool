import os

def run_proxy():
	proxy = '127.0.0.1:8080'
	os.environ["http_proxy"] = proxy
	os.environ["HTTP_PROXY"] = proxy
	os.environ["https_proxy"] = proxy
	os.environ["HTTPS_PROXY"] = proxy
	os.environ["REQUESTS_CA_BUNDLE"] = 'certificate.pem'