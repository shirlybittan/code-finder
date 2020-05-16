import time
import git
import re
import os
from git import RemoteProgress
from github import Github


# open access from my account in github
ACCESS_TOKEN="45e5c4efa04bf6793230b5d7488d8e0d08bff1cb"
g = Github(ACCESS_TOKEN)


#search in github the repositories with the key word in readme.
def search_github(keywords):
    query = '+'.join(keywords) + '+in:readme+in:description'
    result = g.search_repositories(query, 'stars', 'desc')

    print(f'Found {result.totalCount} repo(s)')

    return result

#for each result, we clone from git to a new created file based on the name of each repo. if repo empty, exception.
def gitClone (all_repos):
    for repo in all_repos:
        try:
            print('Cloning into %s' % repo.clone_url)
            git_to_clone=repo.clone_url
            folder_name=git_to_clone.split('/')[-1]
            git.Repo.clone_from(git_to_clone, './test/'+folder_name, branch='master', progress=CloneProgress())
        except:
            print("An exception occurred",repo.clone_url)


def RSA_search(result_path, fin, filename):
    
    #TODO : check for emptyness of the key
    #verify there is no space, only /n is allowed

    #checking if presence of RSA private key
    # RSA = re.findall('.PRIVATE KEY-----(.*?)-----END RSA PRIVATE KEY', fin, re.DOTALL)
    #RSA = re.findall('.PRIVATE KEY-----(([0-9a-zA-Z/+=]))-----END RSA PRIVATE KEY', fin, re.DOTALL)

    if RSA:
        print("\nFound RSA access private key in ", filename, ": \n " )
        print("\n".join(RSA))
        #printing in text file
        with open(os.path.join(result_path,"Results.txt"), "a") as result_file:
            result_file.write("%s %s \n %s\n" % ("\nFound RSA access private key in ", filename, "\n".join(RSA)))

            #to prevent more false positives:
            #TODO = same character 10 times? in all the AWS
            #TODO = same character 5 times? in a row
            #TODO? = search for key world "AWS private key"
            #TODO? = verify to a source if thoses are really keys 

    #return file for the unitTest; we'll compare the actual result txt with the txt we should receive
    #return result_file -> make global so it will work?
    #return result_file


#checking if presence of AWS private key in file
def AWS_search(result_path, fin, filename):

    #only alpha-numeric, / and +. max of 40 characters. dismatch if more than 4 same char in a row
    #TODO : check max of same character in all the string
    pk=re.findall(r'(?:\s|^)(?!.*([0-9a-zA-Z/+])\1{4})([0-9a-zA-Z/+]{40})(?:\s|$)', fin, re.M)
    #pk=re.findall(r'(?:\s|^)([0-9a-zA-Z/+]{40})(?:\s|$)', fin, re.M)  -> without 5 in row but with good print

    if pk:
        print("\n Found AWS private key in ", filename, ": \n " )
        #print("\n".join(pk)) -> nice print but doesnt work with new condition of repeated char
        print(pk)


        #printing the found key in text file
        with open(os.path.join(result_path,"Results.txt"), "a") as result_file:

            #result_file.write("%s %s \n%s\n" % ("\nFound AWS private key in ", filename, "\n".join(pk))) -> nice printing
            result_file.write("%s %s \n%s\n" % ("\nFound AWS private key in ", filename, pk))

    #return file for the unitTest comparaison
    #return result_file -> make global so it will work?




def main():
    #cloning from github to local
    all_repos=search_github("python")
    gitClone (all_repos)

    #reading from local
    result_path='C:/Users/shirl/Desktop/test/results'
    git_repository='C:/Users/shirl/Desktop/test/test_git_folders'

    for path, dirs, files in os.walk(git_repository):
    
                #TODO not searching in files that are NOT text file
        for f in files:
            filename = os.path.join(path, f)
            with open(filename, "r",errors='ignore') as myFile:
                fin = myFile.read()

                #calling my search methods
                AWS_search(result_path, fin, filename)
                RSA_search(result_path, fin, filename)


if __name__ == "__main__":
    main()


class CloneProgress(RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        if message:
            print(message)



