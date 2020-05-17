import time
import git
import re
import os
from git import RemoteProgress
import mimetypes #check if the file has text in it
from github import Github


#added: verification of the type before the search + right print

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
def gitClone (all_repos, git_repository):
    for repo in all_repos:
        try:
            print('Cloning into %s' % repo.clone_url)
            git_to_clone=repo.clone_url
            folder_name=git_to_clone.split('/')[-1]
            git.Repo.clone_from(git_to_clone, git_repository+ "/"+folder_name, branch='master')

            #git.Repo.clone_from(git_to_clone, './test/'+folder_name, branch='master')
        except Exception as e:
            print("An exception occurred",repo.clone_url, "\n",  e )


def RSA_search(result_path, fin, filename):
    #checking if the file is a text file before the verification
	if "text" in mimetypes.guess_type(filename)[0]:
		#checking if presence of RSA private key
		RSA = re.findall('.-----BEGIN RSA PRIVATE KEY-----\\n(([0-9a-zA-Z/+=]+\\n)+)-----END RSA PRIVATE KEY-----', fin)
		#checking if presence of RSA private key
		if RSA:
			print("\nFound RSA access private key in ", filename, ": \n " )
			#print properly the results found
			for x in range(len(RSA)) :
				print (RSA[x][0])
				#printing in text file
				with open(os.path.join(result_path,"Results.txt"), "a") as result_file:
					result_file.write("%s %s \n %s\n" % ("\nFound RSA access private key in ", filename, "\n", RSA[x][0]))
					
		#return file for the unitTest; we'll compare the actual result txt with the txt we should receive
		#return result_file -> make global so it will work?
		#return result_file


#checking if presence of AWS private key in file
def AWS_search(result_path, fin, filename):

    #checking if the file is a text before the verification
	if "text" in mimetypes.guess_type(filename)[0]:	
		#only alpha-numeric, / and +. max of 40 characters. dismatch if more than 4 same char in a row. more than 10 same char in a row is excluded
		pk=re.findall(r'(?:\s|^)(?!.*([0-9a-zA-Z/+])\1{10})([0-9a-zA-Z/+]{40})(?:\s|$)', fin, re.M)
		
		if pk:
			print("\n Found AWS private key in ", filename, ": \n " )
			for x in range(len(pk)) :
				print (pk[x][1])
				
				printing the found key in text file--------------------------------------------------------
				with open(os.path.join(result_path,"Results.txt"), "a") as result_file:
					result_file.write("%s %s \n%s\n" % ("\nFound AWS private key in ", filename,  "\n", pk[x][1])) #print the tuple clearly

		#return file for the unitTest comparaison
		#return result_file -> make global so it will work?




def main():


    #reading from local
    result_path='C:/Users/shirl/Desktop/test/results'
    git_repository='C:/Users/shirl/Desktop/test/test_git_folders'

    #cloning from github to local
    all_repos=search_github("python")
    gitClone (all_repos, git_repository)

    for path, dirs, files in os.walk(git_repository):
    
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



