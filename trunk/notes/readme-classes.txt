item(thing)
	match_interests
	to_atom

crypto
	reset
	encrypt(plaintext)
	decrypt(ciphertext)
	digest(plaintext)
	checksum(plaintext)

minekey
	validate
	newfromencoded
	newfromrelation
	encode
	readable
	permalink
	spawn_oid
	spawn_object
	spawn_submit
	spawn_rewrite

------------------------------------------------------------------

search contexts

	default MAY HAVE
	+ -> MUST HAVE
	- -> MUST NOT HAVE

		visible-to:relation
		with-for:relation
		with-not:relation
		with-type:foo/bar
		with-type:foo/*
		inname:word
		indesc:word
		tag:word
		bareword -> search(inname/indesc/tag)
		[+-]size:40[kmg]

		with-require:tag # searching relations
		with-except:tag # searching relations
