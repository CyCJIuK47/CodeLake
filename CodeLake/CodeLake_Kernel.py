import os
import re
import time

import requests
from bs4 import BeautifulSoup

from collections import deque
from tkinter import ttk
from submission import *
from logger import Logger


class CodeLake:

    __SERVER_TIMEOUT = 1200  ## seconds

    filters = ["OK", "REJECTED", "WRONG_ANSWER", "RUNTIME_ERROR", "TIME_LIMIT_EXCEEDED",
               "MEMORY_LIMIT_EXCEEDED", "COMPILATION_ERROR", "CHALLENGED", "FAILED",
               "PARTIAL", "PRESENTATION_ERROR", "IDLENESS_LIMIT_EXCEEDED", "SECURITY_VIOLATED",
               "CRASHED", "INPUT_PREPARATION_CRASHED", "SKIPPED", "TESTING", "SUBMITTED"]

    def check_nickname_existence(nick_name):

        if nick_name == "":
            return False
        
        path = f"https://codeforces.com/profile/{nick_name}"   

        response = requests.get(path)     
        soup = BeautifulSoup(response.text, "html.parser")

        nick = soup.find("ul", {"class": "second-level-menu-list"})

        if nick == None:
            return False
        
        nick = nick.find("li")
        
        if nick.text == nick_name:
            return True
        return False
    

    def parse(nick_name, path_to_dump, progressbar, filters, need_parse_problems, logger):

        logger.log(f"Parsing for {nick_name} inited...", 1)
        path_to_dump = f"{path_to_dump}//{nick_name}"
        if not os.path.exists(path_to_dump):
             os.makedirs(path_to_dump, 0o700)
        
        pages_count = CodeLake.__get_pages_count(nick_name)
        
        submissions_data = []
        submissions_verdict = []
        
        for page_id in range(1, pages_count+1):
            res = CodeLake.parse_submission_links_from_page(nick_name, page_id, filters)
            submissions_data.extend(res[0])
            submissions_verdict.extend(res[1])

        submissions = []
        
        for data in submissions_data:
            submissions.append(Submission(*data))

        logger.log(f"{len(submissions)} submissions found that satisfy verdict filters")
        
        if len(submissions) == 0:
            progressbar.fill()
            return

        progressbar.set_total_divisions(len(submissions))

        subm_deque = deque(zip(submissions, submissions_verdict))

        while len(subm_deque)!=0:
            submission, verdict = subm_deque.popleft()
            try:
                submission.parse(logger)
                submission.dump(path_to_dump, verdict, logger)
                
                if need_parse_problems:
                    submission.download_problem_content(path_to_dump, logger)

                progressbar.add_divisions(1)

            except:
                ##if banned from server - wait server timeout min and try again
                logger.log(f"Codeforces.com forced server timeout" +
                           f"for {CodeLake.__SERVER_TIMEOUT/60} min")
                time.sleep(CodeLake.__SERVER_TIMEOUT)

                ## return item back to deque to parse later
                subm_deque.append((submission, verdict))

            
      
    def __get_pages_count(nick_name):

        path = f"https://codeforces.com/submissions/{nick_name}"

        response = requests.get(path)
        soup = BeautifulSoup(response.text, "html.parser")

        pages_count = soup.find_all("span", {"class": "page-index"})

        if len(pages_count) == 0:
            return 1
        return int(pages_count[-1].text)


    def parse_submission_links_from_page(nick_name, page_id, filters):

        path = f"https://codeforces.com/submissions/{nick_name}/page/{page_id}"
        
        response = requests.get(path)
        soup = BeautifulSoup(response.text, "html.parser")

        problem_links = soup.find_all("td", {"class": "status-small"})
        problem_links = [i.find_all("a") for i in problem_links]
        problem_links = sum(problem_links, [])
        problem_links = [i["href"] for i in problem_links]

        tmp_links = problem_links
        problem_links = [CodeLake.extract_contest_from_link(i) for i in problem_links]

        verdicts = soup.find_all("span", {"class": "submissionVerdictWrapper"})

        submissions_id = [i["submissionid"] for i in verdicts]
        verdicts = [i["submissionverdict"] for i in verdicts]
        
        chosen_verdicts = [i in filters for i in verdicts]
        sub_filter = [("contest" in link and verdict) for link, verdict in zip(tmp_links, chosen_verdicts)]

        submission_data = list(zip(submissions_id, problem_links))
        submission_data = [submission_data[i] for i in range(len(submission_data)) if sub_filter[i]]
        verdicts = [verdicts[i] for i in range(len(verdicts)) if sub_filter[i]]
  
        return [submission_data, verdicts]
    
    def extract_contest_from_link(link):
        delims = [m.start() for m in re.finditer(r"/", link)]
        return link[delims[1]+1:delims[2]]    
