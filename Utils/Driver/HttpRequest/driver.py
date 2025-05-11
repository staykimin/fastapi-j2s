class Driver:
	def __init__(kimin, modul, **parameter):
		kimin.parameter = parameter
		kimin.modul = modul
		kimin.sesi = modul['requests'].session()
		kimin.hasil = {'status': False}

	def Parse(kimin, respon):
		try:
			hasil = kimin.modul['json'].loads(respon.text)
		except kimin.modul['json'].JSONDecodeError:
			hasil = respon.text
		return hasil

	def Execute(kimin):
		try:
			method = kimin.parameter.get('method', 'get').lower()
			url = kimin.parameter.get('url')

			headers = kimin.parameter.get('header', {})
			cookies = kimin.parameter.get('cookie', {})
			proxy = kimin.parameter.get('proxy', {})
			allow_redirects = kimin.parameter.get('redirect', True)

			if not url:
				kimin.hasil['data'] = 'URL tidak diberikan'
				return kimin.hasil

			if method == 'get':
				respon = kimin.sesi.request(method, url, headers=headers, cookies=cookies, allow_redirects=allow_redirects, proxies=proxy)
			elif method in ['post', 'patch']:
				tipe = kimin.parameter.get('data_type', 'form').lower()
				data = kimin.parameter.get('data', {})
				if tipe == 'json':
					respon = kimin.sesi.request(method, url, headers=headers, json=data, files=kimin.parameter.get('file', None), cookies=cookies, proxies=proxy, allow_redirects=allow_redirects)
				elif tipe == 'form':
					respon = kimin.sesi.request(method, url, headers=headers, data=data, files=kimin.parameter.get('file', None), cookies=cookies, proxies=proxy, allow_redirects=allow_redirects)
			else:
				kimin.hasil['data'] = f'Method "{method}" tidak tersedia'
				return kimin.hasil

			if respon.status_code < 400:
				parsed_content = kimin.Parse(respon)
			else:
				parsed_content = respon.text

			kimin.hasil['status'] = True
			kimin.hasil['content'] = parsed_content
			kimin.hasil['status_code'] = respon.status_code
			kimin.hasil['header'] = dict(respon.headers)
			kimin.hasil['cookie'] = respon.cookies.get_dict()

		except kimin.modul['requests'].Timeout:
			kimin.hasil['data'] = 'Timeout: Permintaan ke server melebihi waktu tunggu'
		except kimin.modul['requests'].RequestException as e:
			kimin.hasil['data'] = f'Gagal menghubungi server: {str(e)}'

		return kimin.hasil
