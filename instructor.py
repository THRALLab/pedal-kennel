# Always start by importing Pedal
from pedal import *
from pedal.gpt import set_openai_api_key

# ... More instructor logic can go here ...
verify()

MAIN_REPORT['gpt']['openai_api_key'] = "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"

from pedal.gpt import gpt_run_prompts
gpt_run_prompts()

from pedal.resolvers import print_resolve
print_resolve()

