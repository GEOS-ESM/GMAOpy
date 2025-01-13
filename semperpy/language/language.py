#----------------------------------------------------------------------------
# SemperPy Copyright GMAO 2009-2011
#
# Author: Claude Gibert, May 2010, claude.gibert@synopticview.com
#-------------------------------------------------------------------
#----------------------------------------------------------------------------
import os
import re
import copy
from semperpy.core.tools import is_dict, ErrorCreator, no_list, to_list, to_lower, resolve_environment_variables, is_string, is_list, mergedicts_keep
from semperpy.core.innerpython import InnerPython
from semperpy.language.languagedefinition import LanguageDefinition
from semperpy.language.validate import languageValidation

class LanguageError(Exception):
    pass

class Language(object):

    languages = {}

    @classmethod
    def resolveDirective(self,directive,directive_name,directive_reader):
        #----------------------------------------------------------------------------
        # This bit is a hard to read. We use two elements to validate a
        # directive, the directive itself, probably provided by the user and
        # the description of the directive's semantics or language 
        # (which keywords are allowed, # required, default keywords, default values 
        # for keywords, etc...)
        # We also use a third element language_definition.* to check that the
        # language semantics are formatted and written properly.
        # It's all written in a single method to try and limit the number of passes
        # on the different dictionaries.
        #----------------------------------------------------------------------------
        added = set()
        language,dir_def,key_def = self.validate_language(directive_name,directive_reader,directive)
        #----------------------------------------------------------------------------
        # First we put in the language definition all the missing keywords which
        # have a default value (e.g. unique, optional etc...)
        # Whenever one or more aliases are defined for a keyword, we store the 
        # information about the keyword in an alias dictionary. Later, we want to
        # replace the aliases used in the directive by the real keyword.
        #----------------------------------------------------------------------------
        aliases = {}
        for key, item in list(language['keywords'].items()):
            for def_name, def_value in list(key_def["defaults"].items()):
                if not def_name in item:
                    item[def_name] = def_value    
            if 'alias' in item:
                for alias in item['alias']:
                    aliases[alias] = key
        lang = language['keywords']
        #----------------------------------------------------------------------------
        # We then go through the directive to replace aliases with the real key
        #----------------------------------------------------------------------------
        to_delete = []
        for key, item in list(directive.items()):
            if key in aliases:
                directive[aliases[key]] = directive[key]
                to_delete.append(key)
        for value in to_delete:
            del(directive[value])
        #----------------------------------------------------------------------------
        # Now we loop over the language keywords to insert in the directive keys 
        # with default values which haven't been specified by the user.
        # We use the same loop to determine if required keywords are missing from
        # the directive.
        #----------------------------------------------------------------------------
        missing = []
        remove = []
        for key in lang:
            if lang[key]['remove']:
                remove.append(key)
            else:
                if not key in directive:
                    if 'default_value' in lang[key]:
                        directive[key] = lang[key]['default_value']
                        added.add(key)
                    if not key in directive and not lang[key]['optional']:
                        missing.append("Keyword %s is missing and is required" % key)
        for k in remove:
            del(lang[k])
        #----------------------------------------------------------------------------
        # Now we go through the directive and apply all the rules we know. We try
        # to accumulate errors and report them at the end so that many can be fixed
        # by the user in one go.
        #----------------------------------------------------------------------------
        unknown = []
        should_be_unique = []
        type_errors = []
        environment_missing = []
        validate = []
        for key, value in list(directive.items()):
            w = key.find('.')
            if w > -1:
                pass
            elif key in lang:
                #---------------------------------------------------------------
                # If the keyword only requires one value, check that only one
                # value was given, if it is a list make it a single item.
                # If the keyword accepts more than one value, change it to a 
                # list if it is not one.
                #---------------------------------------------------------------
                if lang[key]['unique']:
                    try:
                        directive[key] = no_list(value)
                    except ValueError:
                        if len(directive[key]) == 1:
                            should_be_unique.append("The keyword '%s' only takes one value" % key)    
                elif not is_dict(value):
                    directive[key] = to_list(value)
                #---------------------------------------------------------------
                # If a type is specified for that keyword, instanciate an
                # object of that type and pass the given value to the
                # constructor. The type can be applied to all items in a list
                # or structure, or receives the whole structure in the 
                # constructor. The value of the 'distribute_type' flag
                # determines that.
                #---------------------------------------------------------------
                if lang[key]['type'] != "":
                    try:
                        if is_string(lang[key]['type']):
                            thisType = InnerPython.get_class(lang[key]['type'])
                        else:
                            thisType = lang[key]['type']
                        if not lang[key]['unique'] and lang[key]['distribute_type']:
                            for i in range(len(directive[key])):
                                if not isinstance(directive[key][i],thisType):
                                    try:
                                        directive[key][i] = thisType(directive[key][i])
                                    except ValueError as TypeError:
                                        if not lang[key]['ignore_type_errors']:
                                            raise
                        elif not isinstance(directive[key],thisType):
                            directive[key] = thisType(directive[key])
                    except Exception as e:
                        type_errors.append('There was a problem building type %s: %s. ' % (type,str(e)))
                #---------------------------------------------------------------
                # We need to replace environment variables before we convert
                # strings to lower case.
                #---------------------------------------------------------------
                try:
                    directive[key] = resolve_environment_variables(directive[key])
                except NameError as e:
                    environment_missing.append(str(e))
                if lang[key]['lowercase']:
                    directive[key] = to_lower(directive[key])
            else:
                unknown.append("Unknown keyword '%s'" % key)
        error = ErrorCreator(LanguageError,'In directive %s:' % directive_name)
        errors = [unknown,missing,should_be_unique,type_errors,environment_missing]
        for errorType in errors:
            for l in errorType:
                error(l)
        error.check()
        #---------------------------------------------------------------
        # The directive is now ready and clean. We have to do another
        # pass to see if there are validators to check the content of the
        # data. We waited until the last minute because one 
        # validator may need to use values in other keywords to either
        # validate or derive data.
        #---------------------------------------------------------------
        self.run_validate(directive,lang,'validate',error)
        error.check()
        try:
            s = getattr(directive,'default_')
            s.update(added)
        except:
            pass
        try:
            s = getattr(directive,'keywords_')
            s.update(set(language['keywords'].keys()))
        except:
            pass
        kk = list(directive.keys())
        if 'post_validate' in language:
            actions = language['post_validate']
            if not is_list(actions[0]):
                actions = [actions]
            for action in actions:
                if is_string(action[0]):
                    func = languageValidation.get(action[0])
                else:
                    func = action[0]
                args = action[1:]
                try:
                    directive = func(directive,None,None,*args)
                except Exception as e:
                    error('Validation error ' + str(e))
        error.check()
        return directive

    @classmethod
    def resolveCascades(self,directive):
        cascades = []
        for k in directive:
            w = k.find('.')
            if w > -1:
                cascades.append(k)
        for cascade in cascades:
            all = cascade.split('.')
            next = all[0]
            others = all[1:]
            if not next in directive:
                raise ValueError('Cannot resolve cascade: %s',cascade)
            directive[next]['.'.join(others)] = directive[cascade]
            del(directive[cascade])

    @classmethod
    def run_validate(self,directive,lang,keyword,error):
        for key, value in list(directive.items()):
            if key in lang and keyword in lang[key]:
                if len(lang[key][keyword]) > 0:
                    v = lang[key][keyword]
                    if is_string(v[0]):
                        func = languageValidation.get(v[0])
                    else:
                        func = v[0]
                    args = v[1:]
                    try:
                        directive[key] = func(directive,key,to_list(directive[key]),*args)
                        if lang[key]['unique']:
                            directive[key] = no_list(directive[key])
                    except Exception as e:
                        error('Validation error ' + str(e))

    #----------------------------------------------------------------------------
    # Language validation, help find mistakes in the json language definition 
    # files and formats the language dictionary properly
    #----------------------------------------------------------------------------
    @classmethod
    def validate_language(self,directive_name,directive_reader,directive):
        directive_name = directive_name.lower()
        dir_def = LanguageDefinition.directive()
        key_def = LanguageDefinition.keywords()
        # commenting 2 lines: caching the language seems to have some side-effects
        # to be re-visited.
        #if directive_name in self.languages:
        #    return self.languages[directive_name],dir_def,key_def
        language = directive_reader(directive_name)
        language = self.validate_language_part(dir_def,language)
        if not is_dict(language['keywords']):
            raise LanguageError("'keywords' entry should be a dictionary")
        for key, item in list(language['keywords'].items()):
            language['keywords'][key] = self.validate_language_part(key_def,item)
        # we need to cache the language before it can possibly modified by
        # dynamic evaluations otherwise we end up caching the wrong things
        # inheritance and specialize_from can potantially modify the
        # language
        self.languages[directive_name] = language
        language = copy.copy(language)
        if "inherit_from" in language:
            for inherit in language["inherit_from"]:
                parent,_,_ = self.validate_language(inherit,directive_reader,directive)
                self.inherit_from(parent,language)
        if "specialize_from" in language:
            # new dir is a sub-directive of directive, its keywords have been validated
            # against the current language definition. We replace in directive its keywords
            # found in newdir.
            newdir = self.resolveSpecialKeywords(language["specialize_from"],directive,language)
            directive = mergedicts_keep(newdir,directive)
            directive['self'] = directive
            specials = self.find_specials(language["specialize_from"],directive)
            for special in specials:
                for single in special:
                    parent,_,_ = self.validate_language(single,directive_reader,directive)
                    self.specialize_from(parent,language)
        return language,dir_def,key_def

    @classmethod
    def resolveSpecialKeywords(self,definition,directive,language):
        #--------------------------------------------------------------------------
        # if we specialize from another language (what is in the other language
        # supersedes what is in our language), conditions for specialization need
        # to be verified and therefore we want to apply "language rules" to the 
        # keywords used in the truth expressions. We fake a language in memory
        # involving only those keywords and have a sub-directive resolved. That
        # way we can evaluate the expressions for specialization knowing that the
        # keywords involved have been resolved or declared missing to the user
        # in a clean way.
        #--------------------------------------------------------------------------
        class DummyReader(object):
            def __init__(self,language):
                self.language_ = language
            def __call__(self,*args,**kargs):
                return self.language_

        class DummyDir(dict):
            def __init__(self,*args,**kargs):
                super(DummyDir,self).__init__(*args,**kargs)
                self.default_ = set()
                self.keywords_ = set()
            
        keywords = []
        for condition in list(definition.keys()):
            # try and extract the keyword in directive which are used in the 
            # expression
            keywords += [ x for x in re.findall('\w+',condition) if x in language['keywords'] ]
        keywords = list(set(keywords))
        newdir = DummyDir()
        for key in keywords:
            if key in directive:
                newdir[key] = directive[key]
        newlanguage = {
            'directive' : 'dummy',
            'keywords'  : {}
        }
        for key in keywords:
            newlanguage['keywords'][key] = language['keywords'][key]
        newdir = self.resolveDirective(newdir,'dummy',DummyReader(newlanguage))
        return newdir

    @classmethod
    def find_specials(self,definition,directive):
        specials = []
        for condition,special in list(definition.items()):
            try:
                if self.evaluate_condition(condition,directive):
                    specials.append(to_list(special))
            except Exception as e:
                raise ValueError(e.message + '\nThe evaluation of language the condition for inheritance: %s failed' % condition)
        return specials

    @classmethod
    def evaluate_condition(self,condition,directive):
        return eval(condition,None,dict(directive))

    @classmethod
    def inherit_from(self,parent,child):
        if 'post_validate' in parent:
            other = None
            if 'post_validate' in child:
                other = child['post_validate']
                if not is_list(other[0]):
                    other = [other]
            if not is_list(parent['post_validate'][0]):
                parent['post_validate'] = [parent['post_validate']]
            child['post_validate'] = parent['post_validate']
            if other is not None:
                child['post_validate'] += other
        parent = parent['keywords']    
        child = child['keywords']    
        for keyword in parent:
            if not keyword in child:
                child[keyword] = parent[keyword]
            else:
                for key, item in list(parent[keyword].items()):
                    if not key in child[keyword]:
                        child[keyword][key] = item

    @classmethod
    def specialize_from(self,parent,child):
        parent = parent['keywords']    
        child = child['keywords']    
        for keyword in parent:
            child[keyword] = parent[keyword]

    @classmethod
    def validate_language_part(self,semantics,language):
        error = ErrorCreator(LanguageError)
        requireds = []
        for required in semantics['required']:
            for req in required:
                if not required in language:
                    requireds.append(required)
        for key, type in list(semantics['valid'].items()):
            if key in language:
                language[key] = type(language[key])
        invalid = []
        for key in list(language.keys()):
            if not key in semantics['valid']:
                invalid.append(key)
        if len(requireds) > 0:
            error("The following keywords are required in the language definition: " + ', '.join(requireds))
        if len(invalid) > 0:
            error("The following keywords are invalid in the language definition: " + ', '.join(invalid))
        error.check()
        return language
