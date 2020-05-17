import unittest
import secretsFinder
import os
import filecmp


class Test_TestRegex(unittest.TestCase):

    #deleting the result Text file created by those tests at the end of all the tests
  #  def tearDownClass():
   #     os.remove(UnitTest_txt_path+"/unitTest_Results.txt")
      #created before every Test
    def setUp (self):
        open(os.path.join('resultsFound','Results.txt'),'w').close()
 #

 #   def test_AWS(self):
 #
 #       with open( "scannedFile/unitTest_Regex.txt", "r",errors='ignore') as myFile:
 #           fin = myFile.read()
 #           secretsFinder.AWS_search(
 #                   "resultsFound",
 #                   fin, 
 #                  "scannedFile")
 #       self.assertTrue(filecmp.cmp("resultsFound/Results.txt","expectedResults/result_AWS_true.txt"),
 #                                                               'The files are not equals')

    def test_RSA(self):

        with open( "scannedFile/unitTest_Regex.txt", "r",errors='ignore') as myFile:
            fin = myFile.read()
            secretsFinder.RSA_search(
                    "resultsFound",
                    fin, 
                   "scannedFile")
        self.assertTrue(filecmp.cmp("resultsFound/Results.txt","expectedResults/result_RSA_true.txt"),
                                                                'The files are not equals')



   #def test_AWS(self):
   #    self.assertTrue(filecmp.cmp(PythonApplication1.AWS_search(UnitTest_txt_path+"/unitTest_Results_AWS.txt",
   #                                                              unitTest_file,os.path.join(UnitTest_txt_path,"unitTest_test.txt"),
    #                                                             ResultsAWSTrueToCompare, 'The files are not equals')))

if __name__ == '__main__':
    unittest.main()