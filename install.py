import subprocess

modules = ('pandas', 'matplotlib', 'bs4', 'codecs',
           'multiprocessing', 'asynctkinter', 'requests', 're',
           'pylab', 'mpl_toolkits')

for module in modules:
    subprocess.run('pip install {}'.format(module))
