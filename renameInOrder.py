import os, re

# Two digits
for fname in os.listdir("."):
	if fname.endswith(".json"):
		fnum = (re.search(r'\d+\.', fname).group())
		words = fname.split(fnum)
		fnum = fnum.rstrip('.')
		words[-1] = '.' + words[-1]
		if len(fnum) < 2:
			fnum = '0' + fnum
			newName = fnum.join(words)
			os.rename(fname, newName)
		# Only if there are too many preciding zeros
		# elif len(fnum) > 2:
		# 	fnum = fnum[-2:]
		# 	newName = fnum.join(words)
		# 	os.rename(fname, newName)

#In order
prevNum = -1
for fname in os.listdir("."):
	if fname.endswith(".json"):
		fnum = (re.search(r'\d+\.', fname).group().rstrip('.'))
		words = fname.split(fnum)
		ifnum = int(fnum)
		if(ifnum != prevNum + 1):
			ifnum = prevNum + 1
			fnum = str(ifnum)
			if len(fnum) < 2:
				fnum = '0' + fnum
			print fname, fnum.join(words)
			os.rename(fname, fnum.join(words))
		prevNum = ifnum
