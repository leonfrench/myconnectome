"""
run timeseries analyses for all variables

"""

import os
from myconnectome.utils.run_shell_cmd import run_shell_cmd
from myconnectome.utils.get_data import *
from myconnectome.rsfmri import mk_participation_index_giftis
from myconnectome.timeseries import add_timeseries_links
from myconnectome.utils.log_time import log_time, get_time

filepath=os.path.dirname(os.path.abspath(__file__))
basepath=os.path.dirname(filepath)

show_R_web_reports=False

try:
    basedir=os.environ['MYCONNECTOME_DIR']
except:
    raise RuntimeError('you must first set the MYCONNECTOME_DIR environment variable')

try:
    timefile = os.environ["TIME_LOG_FILE"]
except:
    timefile = os.path.join(basedir,'.timing.txt')


tsdir=os.path.join(basedir,'timeseries')
if not os.path.exists(tsdir):
    os.mkdir(tsdir)

if not os.path.exists(os.path.join(tsdir,'tables')):
    os.makedirs(os.path.join(tsdir,'tables'))

behavdir=os.path.join(basedir,'behavior')

# check R dependencies

R_dependencies=['knitr','forecast','markdown','zoo']

f=open(os.path.join(filepath,'check_depends.R'),'w')
f.write('# automatically generated knitr command file\n')
f.write('source("%s/utils/pkgTest.R")\n'%basepath)

for d in R_dependencies:
    f.write('pkgTest("%s")\n'%d)
f.close()
run_shell_cmd('Rscript %s/check_depends.R'%filepath)

if not os.path.exists(os.path.join(tsdir,'timeseries_analyses.html')):
    starttime = get_time()
    f=open(os.path.join(filepath,'knit_timeseries.R'),'w')
    f.write('# automatically generated knitr command file\n')
    f.write('require(knitr)\n')
    f.write('require(markdown)\n')
    f.write('setwd("%s")\n'%tsdir)
    f.write('source("%s/timeseries/load_myconnectome_data.R")\n'%basepath)
    f.write('source("%s/timeseries/timeseries_helpers.R")\n'%basepath)
    f.write('source("%s/timeseries/est_bivariate_arima_model.R")\n'%basepath)
    f.write("knit('%s/timeseries_analyses.Rmd', '%s/timeseries_analyses.md')\n"%
        (filepath.replace('scripts','timeseries'),tsdir))
    f.write("markdownToHTML('%s/timeseries_analyses.md', '%s/timeseries_analyses.html')\n"%
        (tsdir,tsdir))
    f.close()
    run_shell_cmd('Rscript %s/knit_timeseries.R'%filepath)
    endtime = get_time()
    log_time(timefile,starttime,endtime,os.path.join(tsdir,'timeseries_analyses.html'))

if not os.path.exists(os.path.join(tsdir,'Make_timeseries_plots.html')):
    starttime = get_time()
    f=open(os.path.join(filepath,'knit_timeseries_plots.R'),'w')
    f.write('# automatically generated knitr command file\n')
    f.write('require(knitr)\n')
    f.write('require(markdown)\n')
    f.write('setwd("%s")\n'%tsdir)
    f.write('source("%s/timeseries/load_myconnectome_data.R")\n'%basepath)
    f.write('source("%s/timeseries/data_utilities.R")\n'%basepath)
    f.write('source("%s/timeseries/timeseries_helpers.R")\n'%basepath)
    f.write('source("%s/timeseries/est_bivariate_arima_model.R")\n'%basepath)
    f.write("knit('%s/Make_timeseries_plots.Rmd', '%s/Make_timeseries_plots.md')\n"%
        (filepath.replace('scripts','timeseries'),tsdir))
    f.write("markdownToHTML('%s/Make_timeseries_plots.md', '%s/Make_timeseries_plots.html')\n"%
        (tsdir,tsdir))
    f.close()
    run_shell_cmd('Rscript %s/knit_timeseries_plots.R'%filepath)
    endtime = get_time()
    log_time(timefile,starttime,endtime,os.path.join(tsdir,'Make_timeseries_plots.html'))

if not os.path.exists(os.path.join(tsdir,'Make_Timeseries_Heatmaps.html')):
    starttime = get_time()
    f=open(os.path.join(filepath,'knit_timeseries_heatmaps.R'),'w')
    f.write('# automatically generated knitr command file\n')
    f.write('require(knitr)\n')
    f.write('require(markdown)\n')
    f.write('setwd("%s")\n'%tsdir)
    f.write('source("%s/timeseries/load_myconnectome_data.R")\n'%basepath)
    f.write('source("%s/timeseries/data_utilities.R")\n'%basepath)
    f.write('source("%s/timeseries/timeseries_helpers.R")\n'%basepath)
    f.write("knit('%s/Make_Timeseries_Heatmaps.Rmd', '%s/Make_Timeseries_Heatmaps.md')\n"%
        (filepath.replace('scripts','timeseries'),tsdir))
    f.write("markdownToHTML('%s/Make_Timeseries_Heatmaps.md', '%s/Make_Timeseries_Heatmaps.html')\n"%
        (tsdir,tsdir))
    f.close()
    run_shell_cmd('Rscript %s/knit_timeseries_heatmaps.R'%filepath)
    endtime = get_time()
    log_time(timefile,starttime,endtime,os.path.join(tsdir,'Make_Timeseries_Heatmaps.html'))


if not os.path.exists(os.path.join(tsdir,'Make_combined_timeseries_table.html')):
    starttime = get_time()
    f=open(os.path.join(filepath,'knit_timeseries_table.R'),'w')
    f.write('# automatically generated knitr command file\n')
    f.write('require(knitr)\n')
    f.write('require(markdown)\n')
    f.write('setwd("%s")\n'%tsdir)
    f.write('source("%s/timeseries/load_myconnectome_data.R")\n'%basepath)
    f.write('source("%s/timeseries/data_utilities.R")\n'%basepath)
    f.write('source("%s/timeseries/timeseries_helpers.R")\n'%basepath)
    f.write("knit('%s/Make_combined_timeseries_table.Rmd', '%s/Make_combined_timeseries_table.md')\n"%
        (filepath.replace('scripts','timeseries'),tsdir))
    f.write("markdownToHTML('%s/Make_combined_timeseries_table.md', '%s/Make_combined_timeseries_table.html')\n"%
        (tsdir,tsdir))
    f.close()
    run_shell_cmd('Rscript %s/knit_timeseries_table.R'%filepath)
    endtime = get_time()
    log_time(timefile,starttime,endtime,os.path.join(tsdir,'Make_combined_timeseries_table.html'))

add_timeseries_links.add_timeseries_links()

if not os.path.exists(os.path.join(basedir,'rsfmri/lh_PI.func.gii')):
    starttime = get_time()
    mk_participation_index_giftis.mk_participation_index_giftis()
    endtime = get_time()
    log_time(timefile,starttime,endtime,os.path.join(basedir,'rsfmri/lh_PI.func.gii'))
