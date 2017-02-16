import os
import sys

HTML = \
'''
<link rel="stylesheet" href="css/github-markdown.css">
<style>
    .markdown-body {
        box-sizing: border-box;
        min-width: 200px;
        max-width: 980px;
        margin: 0 auto;
        padding: 45px;
    }
</style>
<article class="markdown-body">
    CONTENT
</article>
'''

cmd = 'pandoc --from=markdown --to=html --output={0}.html {0}.md'
md_file = sys.argv[1]
assert md_file.endswith('.md')
md_file = md_file[:-3]
cmd = cmd.format(md_file)
output_file ='{}.html'.format(md_file)

os.system(cmd)
with open(output_file) as f:
    HTML = HTML.replace('CONTENT', f.read())
print(HTML, file=open(output_file, 'w'))
