sub={'funny': {0: {'url': u'http://imgur.com/Ao19hH4', 'title': u'Oops'}, 1: {'url': u'http://i.imgur.com/w0fc4Q3.jpg', 'title': u'I just quit my job the best way I know how.'}, 2: {'url': u'http://i.imgur.com/cAvqVdR.gifv', 'title': u'Synchronized Solo Diving'}, 3: {'url': u'http://i.imgur.com/8MYHxyV.gif', 'title': u'When Mace Windu Lends a Hand'}, 4: {'url': u'http://imgur.com/gallery/CJTJU', 'title': u'Is she... human?'}}}


category = sub.keys()
category = category[0]
values = sub[category]
print values
for key,value in values.items():
	item = key
	title=values[key]["title"]
	url = values[key]["url"]
	# subr=Subreddit(subr_num=item,category=category,title=title,url=url)
	print item,category,title,url

