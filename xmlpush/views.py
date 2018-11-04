from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
import os, base64
from github import Github
from github import InputGitTreeElement

# Create your views here.
def xmlpushView(request):
    return render(request, 'newbook.html')

def addxml(request):
    #generate xml file
    xmlstr = '''<book>
                    <bookid>{bookid}</bookid>
                    <title>{title}</title>
                    <author>{author}</author>
                    <image>{image}</image>
                    <link>{link}</link>
                    <epub>{epub}</epub>
                    <pdf>{pdf}</pdf>
                    <category>{category}</category>
                    <date>{date}</date>
                </book>'''.format(bookid=request.POST['bookid'],
        title = request.POST['title'],
        author = request.POST['author'],
        image = request.POST['image'],
        link = request.POST['link'],
        epub = request.POST['epub'],
        pdf = request.POST['pdf'],
        category = request.POST['category'],
        date = request.POST['date'])
    
    #change the token here
    token = '2b078f735e2a91f37f244d244751ac5499d54411'
    g = Github(token)
    #change the repository name
    repo = g.get_user().get_repo('xmlpush')

    with open('booksdb.xml','a+') as f:
        f.write(xmlstr+'\n')

    #change xml file name
    file_list = ['booksdb.xml']
    commit_message = request.POST['commitmsg']
    master_ref = repo.get_git_ref('heads/master')
    master_sha = master_ref.object.sha
    base_tree = repo.get_git_tree(master_sha)

    element_list = list()
    for entry in file_list:
        with open(entry, 'r') as input_file:
            data = input_file.read()    
        element = InputGitTreeElement(entry, '100644', 'blob', data)
        element_list.append(element)
    tree = repo.create_git_tree(element_list, base_tree)
    parent = repo.get_git_commit(master_sha)
    commit = repo.create_git_commit(commit_message, tree, [parent])
    master_ref.edit(commit.sha)

    return HttpResponse("Pushed to git repo")