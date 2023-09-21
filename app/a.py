import re

def yes_author(text, pattern):
	authors = re.findall(author_pattern, text)
	authors_list = []
	if authors in ",":
		for author in authors:
			cleaned_author = author.replace("<", "").replace(">", "").strip()
			authors_list.append(cleaned_author)
			result = ", ".join(formatted_authors)
	else:
		result = authors
	return result



text = ",<리처드 S. 헤스>,,<더글러스 J. 무> 공편/<박세혁>,<원광연>,<이용중> 공역"
#text = "<최재천>,<장하준>,<최재붕>,<홍기빈>,<김누리>,<김경일>,<정관용> 저"

def yes_author(text):
	if ' 저' in text:
		pattern = r"<(.*?)> 저"
		print("저")
	elif '편' in text:
		pattern = r"<(.*?)> 편"
		print("편")
	else:
		return text
	authors = re.findall(pattern, text)
	authors_list = []
	for author in authors:
		cleaned_author = author.replace("<", "").replace(">", "").strip()
		authors_list.append(cleaned_author)
		result = ", ".join(authors_list)
	return result

print(yes_author(text))
