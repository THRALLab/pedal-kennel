from pedal import *
from pedal.extensions.plotting import *
from curriculum_sneks import *
from curriculum_sneks.files import *

suppress("algorithmic", "iterating_over_non_list")
suppress("algorithmic", "iterating_over_empty_list")
suppress("algorithmic", "incompatible_types")

prevent_advanced_iteration(allow_for=True)

ensure_import('matplotlib.pyplot')
ensure_import('bakery_salary')

ensure_ast("For")
ensure_literal([], message="You will need to create a new empty list to solve this.")
ensure_ast("Attribute", message="You need to use attribute access to get the fields.")
ensure_import('matplotlib.pyplot', message="You have not imported the <code>matplotlib.pyplot</code> module.")

prevent_incorrect_plt()
ensure_correct_plot('scatter')
ensure_show()
ensure_function_call('title', message="You need to add a title.")
ensure_function_call('xlabel', message="You need to label your X-axis.")
ensure_function_call('ylabel', message="You need to label your Y-axis.")

from _instructor.bakery_salary import industries

means = [i.mean_salary for i in industries]
medians = [i.median_salary for i in industries]
members = [i.members for i in industries]
assert_plot('scatter', [means, medians])
assert_plot('scatter', [means, members])

plots = get_plots()
if len(plots) < 2:
    gently("You need to create multiple, separate graphs.")
elif len(plots) > 2:
    gently("You have created too many graphs.")
else:
    if not plots[0]['data'] or not plots[1]['data']:
        gently("It seems like one of your plots may be empty. Make sure you have two separate plots, each with its own data.")
