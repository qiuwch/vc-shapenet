import os, sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dep_paths = [
	BASE_DIR,
	os.path.join(BASE_DIR, 'rendercnn')
]
for p in dep_paths:
	sys.path.append(p)

import global_variables as G

# is_random_env_lighting = True
is_random_env_lighting = False
if is_random_env_lighting:
    env_lighting = np.random.uniform(G.g_syn_light_environment_energy_lowbound, G.g_syn_light_environment_energy_highbound)
else:
    env_lighting = 1
    print('environment lighting is set to %d' % env_lighting)
