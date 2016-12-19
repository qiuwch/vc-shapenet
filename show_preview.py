import glob, re
model_dir = 'ShapeNetCore.v1/02691156/*/model.obj'
regexp = re.compile('ShapeNetCore.v1/02691156/(.*)/model.obj')
# 02691156 is the id for airplane
print model_dir
models = glob.glob(model_dir)
print len(models)

view = [0, 90] # az, el, distance

count = 100 
row_size = 5
i = 0

table_content = ''
row_content = ''
for model in models[:count]:
    # print model
    i = i+1
    match = regexp.match(model)
    id = match.group(1)
    
    img = 'images/{az:.1f}_{el:.1f}_{id}.png'.format(az = view[0], el = view[1], id = id)
    row_content += '<td><img src="{img}" width="300px"/><p>{id}</p></td>\n'.format(img=img, id=id)
    # print img
    
    if i % row_size == 0:
        # flush this row
        table_content += '<tr>{row}</tr>\n'.format(row = row_content)
        row_content = ''
                
html = '<table style="border: 1px;">\n{table}\n</table>'.format(table = table_content)
html_file = 'rendered.html'
with open(html_file, 'w') as f:
    f.write(html)
print 'Preview is saved to %s' % html_file
