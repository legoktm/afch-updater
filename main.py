#!/usr/bin/env python
"""
Copyright (C) 2013 Legoktm

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
"""
import git
import pywikibot
import os
import shutil
import sys

#config
path = '~/projects/afc_pusher/tmp'
path = os.path.expanduser(path)
testwp = pywikibot.Site('test', 'wikipedia')

if '--beta' in sys.argv:
    branch = 'beta'
elif '--master' in sys.argv:
    branch = 'master'
else:
    branch = 'develop'

if '--enwp' in sys.argv:
    testwp = pywikibot.Site('en', 'wikipedia')  # Sucky variable names!


if os.path.exists(path):
    #Update it
    repo = git.Repo(path)
    origin = repo.remotes.origin
    try:
        origin.fetch()
    except AssertionError:
        # I swear, this works.
        origin.fetch()
    origin.pull()
else:
    print 'Cloning to tmp/'
    repo = git.Repo.clone_from('https://github.com/WPAFC/afch.git', path)

sha1 = repo.heads[branch].commit.hexsha
repo.heads[branch].checkout()


summary = 'Auto-updating to {0} ({1})'.format(sha1, branch)
print summary

if branch == 'beta':
    prefix = 'MediaWiki:Gadget-afchelper-beta.js'
else:
    prefix = 'MediaWiki:Gadget-afchelper.js'


mapping = {
    'afch.js': prefix + '',
    'core.js': prefix + '/core.js',
    'ffu.js': prefix + '/ffu.js',
    'redirects.js': prefix + '/redirects.js',
    'submissions.js': prefix + '/submissions.js',
}
files = os.listdir(path + '/src')
print files

for script in files:
    with open(path + '/src/' + script, 'r') as f:
        text = f.read()
    if branch == 'beta':
        text = text.replace('MediaWiki:Gadget-afchelper.js', 'MediaWiki:Gadget-afchelper-beta.js')  # I hope this is ok.
    pg = pywikibot.Page(testwp, mapping[script])
    pg.put(text, summary)

#print 'Cleaning up..'
#shutil.rmtree(path)