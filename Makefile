clean:
	rm -f *.pyc

count:
	echo "Number of rendered images"
	ls -l images/*.png | wc -l
	echo "Number of models"
	# 4045 in total
	
zip_file = airplane_topview.zip
submit:
	zip ${zip_file} rendered.html images/*.png 
	scp ${zip_file} qiuwch@gradx.cs.jhu.edu:/users/qiuwch/public_html/
