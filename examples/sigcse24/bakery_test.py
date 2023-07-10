import os
from dataclasses import dataclass
from pedal.gpt import gpt_run_prompts
from pedal.resolvers import print_resolve

@dataclass
class CodeFeedback:

    file: str
    prompt: str
    feedback: str

    def consolidate(self) -> str:
        return self.file + "\n``````````````````````\n" + self.prompt + "\n``````````````````````\n" + self.feedback + "\n-------------------------\n"

bakery_feedback = []
subset = 100

for dir in os.listdir(os.getcwd()):
    if subset < 0:
        break
    path = os.getcwd() + "\\" + dir + "\\submissions\\"
    if os.path.isdir(path):
        for file in os.listdir(path):
            if file.endswith(".py") and os.stat(path+file).st_size > 0:
                code = open(path+file, "r")
                read_code = code.read()
                results = gpt_run_prompts(code=read_code)
                bakery_feedback.append(CodeFeedback(file=path+file, prompt=read_code, feedback=results['feedback']['feedback']))
                subset -= 1

with open('prompt_feedback_results.txt', 'a+') as output_file:
    for code_feedback in bakery_feedback:
        output_file.write(code_feedback.consolidate())