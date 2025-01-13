from gmaopy.stats.stattexttemplate import StatTextTemplate

#---------------------------------------------------------------------------------------
# This is where data formatting for displaying titles, legends etc... happens.
# In the title, legend etc... templates (in json files), we define variables between
# <> e.g. <expver>. If the keyword is part of the directive being processed it is
# displayed, unless a method with the same name as the variable is defined here.
# That way, the normal formatting of data can be overriden and new keywords can be
# created (e.g. date_interval).
#---------------------------------------------------------------------------------------
class ScoreTextTemplate(StatTextTemplate):
    pass
