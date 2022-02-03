import os
import json

import requests

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from logger import Logger


class Submission:
    
    __match_lang = {"GNU C11": "c",
                    "Clang++17 Diagnostics": "cpp",
                    "GNU C++11": "cpp",
                    "GNU C++14": "cpp",
                    "GNU C++17": "cpp",
                    "GNU C++20 (64)": "cpp",
                    "MS C++ 2017": "cpp",
                    "GNU C++17 (64)": "cpp",
                    ".NET Core C#": "cs",
                    "Mono C#": "cs",
                    "D": "d",
                    "Go": "go",
                    "Haskell": "hs",
                    "Java 11": "java",
                    "Java 8": "java",
                    "Kotlin 1.4": "kt",
                    "Kotlin 1.5": "kt",
                    "OCaml": "ml",
                    "Delphi 7": "pas",
                    "Free Pascal": "pas",
                    "PascalABC.NET": "pas",
                    "Perl": "pl",
                    "PHP": "php",
                    "Python 2": "py",
                    "Python 3": "py",
                    "PyPy 2": "py",
                    "PyPy 3": "py",
                    "PyPy 3-64": "py",
                    "Ruby": "ruby",
                    "Rust": "rs",
                    "Scala": "scala",
                    "JavaScript": "js",
                    "Node.js": "js"}


    def __init__(self, submission_id, contest_id):

        self.metadata = dict()
        self.__path = f"https://codeforces.com/contest/{contest_id}/submission/{submission_id}"
        self.__contest_id = contest_id
        self.__code = ""


    def parse(self, logger=None):

        s = requests.Session()
        s.headers.update({'User-Agent': UserAgent().random,
                          'Accept-Language': 'uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7',
                          'cache-control': 'no-cache',
                          'pragma': 'no-cache',
                          'upgrade-insecure-requests': '1'
                         })
        
        response = s.get(self.__path,
                         headers={'User-Agent': UserAgent().random})     
        
        soup = BeautifulSoup(response.text, "html.parser")
        submission_code = soup.find_all("pre")[0]
        self.__code = submission_code.text.replace("\r\n", "\n")
        
        metainfo = soup.find_all("tr")
        metakeys = metainfo[0].find_all("th")
        metakeys = [i.text for i in metakeys]

        metavalues = metainfo[1].find_all("td")
        problem_name = metavalues[2].find("a")["title"]
        metavalues = [self.__beautify(i.text) for i in metavalues]

        self.metadata = dict(zip(metakeys, metavalues))
        self.metadata["problem_name"] = self.__validate(problem_name)
        
        if logger != None:
            logger.log(f"Submission {self.metadata['#']} sucessfully parsed")
            

    def download_problem_content(self, path_to_dump, logger=None):

        folder_name = self.metadata["problem_name"]
        
        extended_path = f"{path_to_dump}//{folder_name}//Statement.doc"
        
        if os.path.isfile(extended_path):
            return

        problem_name = self.metadata["Problem"]
        problem_id = problem_name[len(str(self.__contest_id))]

        problem = Problem(self.__contest_id, problem_id)
        problem.parse(logger)
        problem.dump(f"{path_to_dump}//{folder_name}", logger)

        
    def dump(self, folder_to_dump, additional_info, logger=None):
        

        folder_name = self.metadata['problem_name']
        extended_path = f"{folder_to_dump}//{folder_name}"

        if not os.path.exists(extended_path):
             os.makedirs(extended_path, 0o700)

        file_extension = Submission.__match_lang[self.metadata["Lang"]]
        file_name = f"{self.metadata['#']}[{additional_info}]"

        path_to_dump = f"{extended_path}//{file_name}.{file_extension}"
        
        file = open(path_to_dump, "w+")
        file.write(self.__code)
        file.close()

        #dump metadata
        file_name = f"{self.metadata['#']}[METADATA]"
        
        file = open(f"{extended_path}//{file_name}.txt", "w+")
        file.write(json.dumps(self.metadata, indent=4))
        file.close() 

        if logger != None:
            logger.log(f"Submission {self.metadata['#']} successfully dumped", 1)

    def __beautify(self, s):

        s = s.replace('\t', '') 
        s = s.replace('\n', '')
        s = s.replace('\r', '')
        s = s.replace(u'\xa0', ' ')
        s = s.strip()

        return s

    def __validate(self, problem_name):

        problem_name = problem_name.replace('/', '')
        problem_name = problem_name.replace('\\', '')
        problem_name = problem_name.replace('?', '')
        problem_name = problem_name.replace('*', '')
        problem_name = problem_name.replace('<', '')
        problem_name = problem_name.replace('>', '')
        problem_name = problem_name.replace('|', '')
        problem_name = problem_name.replace('"', '')
        problem_name = problem_name.replace(':', '')

        return problem_name
    


class Problem:

    def __init__(self, contest_id, problem_id):

        self.__contest_id = contest_id
        self.__problem_id = problem_id
        self.__path = f"https://codeforces.com/contest/{contest_id}/problem/{problem_id}"
        self.data = dict()


    def parse(self, logger=None, proxy={}):

        s = requests.Session()
        s.headers.update({'User-Agent': UserAgent().random,
                          'Accept-Language': 'uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7',
                          'cache-control': 'no-cache',
                          'pragma': 'no-cache',
                          'upgrade-insecure-requests': '1'
                         })

        s.proxies.update(proxy)
        s.trust_env = False
        
        response = s.get(self.__path)  
        
        soup = BeautifulSoup(response.text, "html.parser")
        self.data["title"] = soup.find("div", {"class": "title"}).text
        
        time_limit = soup.find("div", {"class": "time-limit"})
        self.data["time_limit"] = self.__beautify(" ".join([i.text for i in time_limit]))
        
        memory_limit = soup.find("div", {"class": "memory-limit"})
        self.data["memory_limit"] = self.__beautify(" ".join([i.text for i in memory_limit]))

        problem_text = soup.find("div", {"class": "problem-statement"}).find_all("p")
        
        
        problem_text = [self.__beautify(i.text) for i in problem_text]
        self.data["problem_text"] = " ".join(problem_text)

        input_specification = soup.find("div", {"class": "input-specification"})
        self.data["input_specification"] = " ".join([self.__beautify(i.text)
                                                     for i in input_specification.find_all("p")])
        
        output_specification = soup.find("div", {"class": "output-specification"})
        self.data["output_specification"] = " ".join([self.__beautify(i.text)
                                                      for i in output_specification.find_all("p")])
        
        sample_tests = soup.find("div", {"class": "sample-tests"})

        note = soup.find("div", {"class": "note"})

        if note is not None:
            self.data["note"] = " ".join([self.__beautify(i.text) for i in note.find_all("p")])


        sample_tests = sample_tests.find_all("pre")
        sample_tests = [str(i).replace("<pre>", "").replace("</pre>", "").replace("<br/>", "\n")
                        for i in sample_tests]

        sample_tests_str = []

        for i in range(0, len(sample_tests)//2):
            sample_tests_str.append(f"\nSample {i+1}\n")
            sample_tests_str.append("Input:\n")
            sample_tests_str.append(sample_tests[2*i])
            sample_tests_str.append("Output:\n")
            sample_tests_str.append(sample_tests[2*i+1])
            
        self.data["sample_tests"] = "".join(sample_tests_str)

        if logger != None:
            logger.log(f"'{self.data['title']}' successfully parsed")
   
    def dump(self, path_to_dump, logger=None):

        file = open(f"{path_to_dump}//Statement.doc", "w+", encoding='utf-8')
        for i in self.data.values():
            file.write(str(i)+"\n\n")
        file.close()
        if logger != None:
            logger.log(f"'{self.data['title']}' sucessfully dumped", 1)

    def __beautify(self, s):

        s = " ".join(s.split()).replace("\n", "").replace("\u2009", "")
        s = s.replace("\xa0","").replace("$$$", "")
        return s
