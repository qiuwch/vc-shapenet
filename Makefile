demo:
	python ./warehouse_demo.py

clean:
	rm -f *.pyc

count:
	echo "Number of rendered images"
	ls -l images/*.png | wc -l
	echo "Number of models"
	# 4045 in total
	
zip_file = airplane_topview.zip
tgt = qiuwch@gradx.cs.jhu.edu:/users/qiuwch/public_html/
files = rendered.html images/*.png 
submit:
	zip ${zip_file} ${files}
	scp ${zip_file} ${tgt}
	scp -r ${files} ${tgt}
