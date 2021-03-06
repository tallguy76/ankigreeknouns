#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shelve
import argparse
import re
import os

import ankigreekutil as anki


def main():
    args = parse_args()
    if args.get:
        download_and_save(args.get)
    if args.show:
        anki.show_forms(args.show, SHELF)
    if args.anki:
        prepare_shelf()
        create_noun_files(anki.NOUNS)

def regularize_neuter(record):
    record['Singular']['Accusative'] = record['Singular']['Vocative'] = record['Singular']['Nominative']
    record['Dual']['Accusative'] = record['Dual']['Vocative'] = record['Dual']['Nominative']
    record['Dual']['Dative'] = record['Dual']['Genitive']
    record['Plural']['Accusative'] = record['Plural']['Vocative'] = record['Plural']['Nominative']

def regularize(record):
    record['Dual']['Accusative'] = record['Dual']['Vocative'] = record['Dual']['Nominative']
    record['Dual']['Dative'] = record['Dual']['Genitive']
    record['Plural']['Vocative'] = record['Plural']['Nominative']

def prepare_shelf():
    SHELF['ἡ μνᾶ'] = {
        'Singular': {'Nominative': u'μνᾶ',
                     'Genitive': u'(μνάᾱς) μνᾶς',
                     'Dative': u'μνᾷ',
                     'Accusative': u'μνᾶν',
                     'Vocative': u'μνᾶ',
                     },
        'Dual':     {'Nominative': u'μνᾶ',
                     'Genitive': u'μναῖν',
                     'Dative': u'μναῖν',
                     'Accusative': u'μνᾶ',
                     'Vocative': u'μνᾶ',
                     },
        'Plural':   {'Nominative': u'μναῖ',
                     'Genitive': u'μνῶν',
                     'Dative': u'μναῖς',
                     'Accusative': u'μνᾶς',
                     'Vocative': u'μναῖ',
                     }
        }
    SHELF['ἡ συκῆ'] = {
        'Singular': {'Nominative': u'σῡκῆ',
                     'Genitive': u'(σῡκέᾱς) σῡκῆς',
                     'Dative': u'συκῇ',
                     'Accusative': u'συκῆν',
                     'Vocative': u'σῡκῆ',
                     },
        'Dual':     {'Nominative': u'συκᾶ',
                     'Genitive': u'συκαῖν',
                     'Dative': u'συκαῖν',
                     'Accusative': u'συκᾶ',
                     'Vocative': u'συκᾶ',
                     },
        'Plural':   {'Nominative': u'συκαῖ',
                     'Genitive': u'συκῶν',
                     'Dative': u'συκαῖς',
                     'Accusative': u'συκᾶς',
                     'Vocative': u'συκαῖ',
                     }
        }
    SHELF['ὁ νοῦς'] = {
        'Singular': {'Nominative': u'(νόος) νοῦς',
                     'Genitive': u'(νόου) νοῦ',
                     'Dative': u'(νόῳ) νῷ',
                     'Accusative': u'(νόον) νοῦν',
                     'Vocative': u'(νόε) νοῦ',
                     },
        'Dual':     {'Nominative': u'(νόω) νώ',
                     'Genitive': u'(νόοιν) νοῖν',
                     'Dative': u'(νόοιν) νοῖν',
                     'Accusative': u'(νόω) νώ',
                     'Vocative': u'(νόω) νώ',
                     },
        'Plural':   {'Nominative': u'(νόοι) νοῖ',
                     'Genitive': u'(νόων) νῶν',
                     'Dative': u'(νόοις) νοῖς',
                     'Accusative': u'(νόους) νοῦς',
                     'Vocative': u'(νόοι) νοῖ',
                     }
        }
    SHELF['ὁ περίπλους'] = {
        'Singular': {'Nominative': u'(περίπλοος) περίπλους',
                     'Genitive': u'(περιπλόου) περίπλου',
                     'Dative': u'(περιπλόῳ) περίπλῳ',
                     'Accusative': u'(περίπλοον) περίπλουν',
                     'Vocative': u'(περίπλοε) περίπλου',
                     },
        'Dual':     {'Nominative': u'(περιπλόω) περίπλω',
                     'Genitive': u'(περιπλόοιν) περίπλοιν',
                     'Dative': u'(περιπλόοιν) περίπλοιν',
                     'Accusative': u'(περιπλόω) περίπλω',
                     'Vocative': u'(περιπλόω) περίπλω',
                     },
        'Plural':   {'Nominative': u'(περίπλοοι) περίπλοι',
                     'Genitive': u'(περιπλόων) περίπλων',
                     'Dative': u'(περιπλόοις) περίπλοις',
                     'Accusative': u'(περιπλόους) περίπλους',
                     'Vocative': u'(περίπλοοι) περίπλοι',
                     }
        }
    SHELF['ἡ μήτηρ'] = {
        'Singular': {'Nominative': u'μήτηρ',
                     'Genitive': u'μητρός',
                     'Dative': u'μητρί',
                     'Accusative': u'μητέρα',
                     'Vocative': u'μῆτερ',
                     },
        'Dual':     {'Nominative': u'μητέρε',
                     'Genitive': u'μητέροιν',
                     'Dative': u'μητέροιν',
                     'Accusative': u'μητέρε',
                     'Vocative': u'μητέρε',
                     },
        'Plural':   {'Nominative': u'μητέρες',
                     'Genitive': u'μητέρων',
                     'Dative': u'μητράσι(ν)',
                     'Accusative': u'μητέρας',
                     'Vocative': u'μητέρες',
                     }
        }
    SHELF['ὁ Σωκράτης'] = {
        'Singular': {'Nominative': u'Σωκράτης',
                     'Genitive': u'(Σωκράτεσος) Σωκράτους',
                     'Dative': u'(Σωκράτει) Σωκράτει',
                     'Accusative': u'(Σωκράτεα) Σωκράτη / Σωκράτην',
                     'Vocative': u'Σώκρατες',
                     }
        }
    SHELF['ἡ τριήρης'] = {
        'Singular': {'Nominative': u'τριήρης',
                     'Genitive': u'(τριήρεσος) τριήρους',
                     'Dative': u'(τριήρεϊ) τριήρει',
                     'Accusative': u'(τριήρεα) τριήρη',
                     'Vocative': u'τριῆρες',
                     },
        'Dual':     {'Nominative': u'(τριήρεε) τριήρει',
                     'Genitive': u'(τριηρέοιν) τριήροιν',
                     'Dative': u'(τριηρέοιν) τριήροιν',
                     'Accusative': u'(τριήρεε) τριήρει',
                     'Vocative': u'(τριήρεε) τριήρει',
                     },
        'Plural':   {'Nominative': u'(τριήρεες) τριήρεις',
                     'Genitive': u'(τριηρέων) τριήρων',
                     'Dative': u'(τριήρεσσι) τριήρεσι(ν)',
                     'Accusative': u'τριήρεις',
                     'Vocative': u'(τριήρεες) τριήρεις',
                     }
        }
    SHELF['τὸ γέρας'] = {
        'Singular': {'Nominative': u'γέρας',
                     'Genitive': u'(γέρασος) γέρως',
                     'Dative': u'γέραι / γέρᾳ',
                     'Accusative': u'γέρας',
                     'Vocative': u'γέρας',
                     },
        'Dual':     {'Nominative': u'(γέραε) γέρᾱ',
                     'Genitive': u'(γεράοιν) γερῷν',
                     'Dative': u'(γεράοιν) γερῷν',
                     'Accusative': u'(γέραε) γέρᾱ',
                     'Vocative': u'(γέραε) γέρᾱ',
                     },
        'Plural':   {'Nominative': u'(γέραα) γέρᾱ',
                     'Genitive': u'(γεράων) γερῶν',
                     'Dative': u'(γέρασσι) γέρασι(ν)',
                     'Accusative': u'(γέραα) γέρᾱ',
                     'Vocative': u'(γέραα) γέρᾱ',
                     }
        }
    SHELF['τὸ δέος'] = {
        'Singular': {'Nominative': u'δέος',
                     'Genitive': u'(δέεσος) δέους',
                     'Dative': u'(δέει) δέει',
                     'Accusative': u'δέος',
                     'Vocative': u'δέος',
                     }
        }
    SHELF['ἡ αἰδώς'] = {
        'Singular': {'Nominative': u'αἰδώς',
                     'Genitive': u'(αἰδόσος) αἰδοῦς',
                     'Dative': u'(αἰδόι) αἰδοῖ',
                     'Accusative': u'(αἰδόα) αἰδῶ',
                     'Vocative': u'αἰδώς',
                     }
        }
    SHELF['τὸ ἄστυ'] = {
        'Singular': {'Nominative': u'ἄστυ',
                     'Genitive': u'(ϝάστευ̯ος) ἄστεως',
                     'Dative': u'ἄστει',
                     'Accusative': u'ἄστυ',
                     'Vocative': u'ἄστυ',
                     },
        'Dual':     {'Nominative': u'ἄστει',
                     'Genitive': u'ἀστέοιν',
                     'Dative': u'ἀστέοιν',
                     'Accusative': u'ἄστει',
                     'Vocative': u'ἄστει',
                     },
        'Plural':   {'Nominative': u'ἄστη',
                     'Genitive': u'ἄστεων',
                     'Dative': u'ἄστεσι(ν)',
                     'Accusative': u'ἄστη',
                     'Vocative': u'ἄστη',
                     }
        }
    SHELF['ἡ γραῦς'] = {
        'Singular': {'Nominative': u'γραῦς',
                     'Genitive': u'γρᾱός',
                     'Dative': u'γρᾱῑ́',
                     'Accusative': u'γραῦν',
                     'Vocative': u'γραῦ',
                     },
        'Dual':     {'Nominative': u'γρᾶε',
                     'Genitive': u'γρᾱοῖν',
                     'Dative': u'γρᾱοῖν',
                     'Accusative': u'γρᾶε',
                     'Vocative': u'γρᾶε',
                     },
        'Plural':   {'Nominative': u'γρᾶες',
                     'Genitive': u'γρᾱῶν',
                     'Dative': u'γραυσί(ν)',
                     'Accusative': u'γραῦς',
                     'Vocative': u'γρᾶες',
                     }
        }
    SHELF['ὁ βασιλεύς'] = {
        'Singular': {'Nominative': u'βᾰσῐλεύς',
                     'Genitive': u'(βασιλῆϝος) βᾰσῐλέως',
                     'Dative': u'βᾰσῐλεῖ',
                     'Accusative': u'βᾰσῐλέᾱ',
                     'Vocative': u'βᾰσῐλεῦ',
                     },
        'Dual':     {'Nominative': u'βᾰσῐλῆ',
                     'Genitive': u'βᾰσῐλέοιν',
                     'Dative': u'βᾰσῐλέοιν',
                     'Accusative': u'βᾰσῐλῆ',
                     'Vocative': u'βᾰσῐλῆ',
                     },
        'Plural':   {'Nominative': u'βᾰσῐλῆς / βᾰσῐλεῖς',
                     'Genitive': u'βᾰσῐλέων',
                     'Dative': u'βᾰσῐλεῦσῐ(ν)',
                     'Accusative': u'βᾰσῐλέᾱς',
                     'Vocative': u'βᾰσῐλῆς / βᾰσῐλεῖς',
                     }
        }
    hermes = SHELF['ὁ Ἑρμῆς']
    hermes['Singular']['Accusative'] = u'(Ἑρμέην) Ἑρμῆν'
    SHELF['ὁ Ἑρμῆς'] = hermes
    sus = SHELF['ὁ/ἡ σῦς']
    sus['Plural']['Dative'] = u'συσί(ν)'
    sus['Singular']['Genitive'] = u'σῠός'
    SHELF['ὁ/ἡ σῦς'] = sus
    rhetor = SHELF['ὁ ῥήτωρ']
    rhetor['Singular']['Vocative'] = u'ῥῆτορ'
    SHELF['ὁ ῥήτωρ'] = rhetor
    ichthus = SHELF['ὁ ἰχθύς']
    ichthus['Singular']['Vocative'] = u'ἰχθύ̄'
    ichthus['Singular']['Accusative'] = u'ἰχθύ̄ν'
    ichthus['Singular']['Nominative'] = u'ἰχθύ̄ς'
    SHELF['ὁ ἰχθύς'] = ichthus
    nike = SHELF['ἡ νίκη']
    nike['Singular']['Nominative'] = u'νί̄κη'
    nike['Singular']['Genitive'] = u'νί̄κης'
    SHELF['ἡ νίκη'] = nike
    heros = SHELF['ὁ ἥρως']
    heros['Singular']['Genitive'] = u'(ἥρωϝος) ἥρωος'
    heros['Singular']['Dative'] = u'ἥρωϊ / ἥρῳ'
    heros['Singular']['Accusative'] = u'ἥρωα / ἥρω'
    SHELF['ὁ ἥρως'] = heros
    genos = SHELF['τὸ γένος']
    genos['Singular']['Genitive'] = u'(γένεσος) γένους'
    genos['Singular']['Dative'] = u'(γένεϊ) γένει'
    genos['Dual']['Nominative'] = u'(γένεε) γένει'
    genos['Dual']['Genitive'] = u'(γενέοιν) γενοῖν'
    genos['Plural']['Nominative'] = u'(γένεα) γένη'
    genos['Plural']['Genitive'] = u'γενέων / γενῶν'
    genos['Plural']['Dative'] = u'(γένεσσι) γένεσι(ν)'
    regularize_neuter(genos)
    SHELF['τὸ γένος'] = genos
    ris = SHELF['ἡ ῥίς']
    ris['Singular']['Nominative'] = u'ῥί̄ς'
    ris['Singular']['Genitive'] = u'ῥῑνός'
    ris['Singular']['Vocative'] = ris['Singular']['Nominative']
    SHELF['ἡ ῥίς'] = ris
    boreas = SHELF['ὁ Βορρᾶς']
    boreas['Singular']['Nominative'] = u'(Βορέᾱς) Βορρᾶς'
    boreas['Singular']['Genitive'] = u'(Βορέᾱ) Βορρᾶ / Βορροῦ'
    boreas['Singular']['Vocative'] = u'Βορρᾶ'
    SHELF['ὁ Βορρᾶς'] = boreas
    keras = SHELF['τὸ κέρας']
    keras['Singular']['Genitive'] = u'κέρᾱτος / (κέρασος) κέρως'
    keras['Singular']['Dative'] = u'κέρατι / κέραι'
    keras['Dual']['Nominative'] = u'κέρατε / κέρᾱ'
    keras['Dual']['Genitive'] = u'κεράτοιν / κερῷν'
    keras['Plural']['Nominative'] = u'κέρατα / κέρᾱ'
    keras['Plural']['Genitive'] = u'κεράτων / κερῶν'
    keras['Plural']['Dative'] = u'κέρᾱσι(ν)'
    regularize_neuter(keras)
    SHELF['τὸ κέρας'] = keras
    ois = SHELF['ὁ/ἡ οἶς']
    ois['Singular']['Genitive'] = u'(ὀϝιός) οἰός'
    SHELF['ὁ/ἡ οἶς'] = ois
    peitho = SHELF['ἡ πειθώ']
    peitho['Singular']['Genitive'] = u'(πειθόι̯ος) πειθοῦς'
    peitho['Singular']['Dative'] = u'(πειθόι̯ι) πειθοῖ'
    peitho['Singular']['Accusative'] = u'(πειθόι̯α) πειθώ'
    peitho['Singular']['Vocative'] = u'(πειθόι̯) πειθοῖ'
    SHELF['ἡ πειθώ'] = peitho
    naus = SHELF['ἡ ναῦς']
    naus['Singular']['Genitive'] = u'(νᾱϝός) νεώς'
    SHELF['ἡ ναῦς'] = naus
    neos = SHELF['ὁ νεώς']
    neos['Singular']['Nominative'] = u'(νηός) νεώς'
    neos['Singular']['Genitive'] = u'(νηοῦ) νεώ'
    neos['Singular']['Dative'] = u'(νηῷ) νεῴ'
    neos['Singular']['Accusative'] = u'(νηόν) νεών'
    neos['Dual']['Nominative'] = u'(νηώ) νεώ'
    neos['Dual']['Genitive'] = u'(νηοῖν) νεῴν'
    neos['Plural']['Nominative'] = u'(νηοί) νεῴ'
    neos['Plural']['Genitive'] = u'(νηῶν) νεών'
    neos['Plural']['Dative'] = u'(νηοῖς) νεῴς'
    neos['Plural']['Accusative'] = u'(νηούς) νεώς'
    regularize(neos)
    SHELF['ὁ νεώς'] = neos
    osteon = SHELF['τὸ ὀστοῦν']
    osteon['Singular']['Genitive'] = u'(ὀστέου) ὀστοῦ'
    SHELF['τὸ ὀστοῦν'] = osteon
    pericles = SHELF['ὁ Περικλῆς']
    pericles['Singular']['Genitive'] = u'(Περικλέεσος) Περικλέους'
    SHELF['ὁ Περικλῆς'] = pericles
    hepar = SHELF['τὸ ἧπαρ']
    hepar['Singular']['Genitive'] = u'(ι̯ήπατος) ἥπατος'
    SHELF['τὸ ἧπαρ'] = hepar
    polis = SHELF['ἡ πόλις']
    polis['Singular']['Genitive'] = u'(πόληι̯ος) πόλεως'
    SHELF['ἡ πόλις'] = polis
    pechus = SHELF['ὁ πῆχυς']
    pechus['Singular']['Genitive'] = u'(πήχευ̯ος) πήχεως'
    SHELF['ὁ πῆχυς'] = pechus
    glotta = SHELF['ἡ γλῶττα']
    glotta['Singular']['Genitive'] = u'(γλώχι̯ης) γλώττης'
    SHELF['ἡ γλῶττα'] = glotta
    aithiops = SHELF['ὁ Αἰθίοψ']
    aithiops['Plural']['Dative'] = u'Αἰθίοψῐ(ν)'
    SHELF['ὁ Αἰθίοψ'] = aithiops





def download_and_save(word):
    html = anki.get_html_from_wiktionary(word)
    forms = get_noun_forms(html)
    save_forms(word, forms)


def create_noun_files(words):
    try:
        os.unlink(anki.NOUNS_FILE)
    except OSError:
        pass
    try:
        os.unlink(anki.NOUNS_REVERSE)
    except OSError:
        pass
    for word in words:
        output_word_defs(word)


def output_word_defs(word):
    try:
        if not SHELF.get(word):
            download_and_save(word)
    except:
        print (u"Bad defintion for " + unicode(word, 'utf-8')).encode('utf-8')
        return

    # article = article_from_gender(SHELF[word]['gender'])
    # nom_sing = SHELF[word]['Singular']['Nominative']
    # dict_form = article + ' ' + nom_sing
    # unfortunately the dictionary is not regular
    dict_form = unicode(word, 'utf-8')
    gensing = clean_form(SHELF[word]['Singular']['Genitive'])
    gensing_article = article_for_word(word, 'Singular', 'Genitive')
    gensing_form = gensing_article + " " + gensing

    numbers = ['Singular', 'Plural', 'Dual']
    defs = {}
    if not SHELF[word].get('Singular'):
        print (u"Bad defintion for " + unicode(word, 'utf-8')).encode('utf-8')
    for number in numbers:
        if not SHELF[word].get(number):
            continue
        for decl, form in SHELF[word][number].iteritems():
            article = article_for_word(word, number, decl)
            for ff in min_form(clean_form(form)):
                if not defs.get(ff):
                    defs[ff] = []
                defs[ff].append([number, decl])
            ss = dict_form + ": " + article + " ________; "
            ss += article + " " + clean_form(form)
            ss += "<br><br>" + gensing_form

            if not ignore_cases(article, number, decl):
                with open(anki.NOUNS_REVERSE, 'a') as ff:
                    ff.write(ss.encode('utf-8') + "\n")

    # forward
    for form in defs.keys():
        full_forms = set()
        for number, decl in defs[form]:
            full_forms.add(article_for_word(word, number, decl) + ' ' + clean_form(SHELF[word][number][decl]) )
        ss = form + '; '
        for full_form in full_forms:
            ss += full_form + '<br>'
        ss += '<br>' + dict_form
        ss += ', ' + gensing_form
        with open(anki.NOUNS_FILE, 'a') as ff:
            ff.write(ss.encode('utf-8') + "\n")


def ignore_cases(article, number, decl):
    article = article.split('/')[0]
    noms = [u'τὼ', u'τὸ', u'τὰ', u'οἱ', u'αἱ']
    if article in noms:
        if decl != 'Nominative':
            return True
    if article == u'τοῖν':
        if decl != 'Genitive':
            return True
    return False


def min_form(form):
    forms = form.split(' ')
    forms = filter(lambda xx: xx != '/', forms)
    forms = filter(lambda xx: xx != '(late)', forms)
    forms = map(remove_parens, forms)

    output = []
    for form in forms:
        output += replace_movable_n(form)

    return output


def replace_movable_n(form):
    if len(form) > 3 and form[-3] == u'(' and form[-2] == u'ν' and form[-1] == u')':
        return [form[0:-3], form[0:-3] + u'ν']
    return [form]


def remove_parens(word):
    if word[0] == '(' and word[-1] == ')':
        return word[1:-1]
    return word


def article_for_word(word, number, decl):
    word_article = unicode(word.split(' ')[0], 'utf-8')
    if word_article == u'ὁ':
        gender = 'm'
    elif word_article == u'ἡ':
        gender = 'f'
    elif word_article == u'τὸ':
        gender = 'n'
    elif word_article == u'ὁ/ἡ':
        gender = 'm/f'
    else:
        print word
        raise Exception('Could not find article')

    if gender == 'm/f':
        first = anki.ARTICLE_MAP['m'][number][decl]
        second = anki.ARTICLE_MAP['f'][number][decl]
        return first + '/' + second

    return anki.ARTICLE_MAP[gender][number][decl]


def clean_form(form):
    articles = [u'οἱ', u'τοὺς', u'τοῖς', u'τοῦ', u'τὸν', u'τῷ', u'τοῖν',
                u'τῶν', u'τὼ', u'ὁ', u'ὁ/ἡ', u'οἱ/αἱ', u'τῷ/τῇ', u'τὸν/τὴν',
                u'τοῦ/τῆς', u'τοὺς/τὰς', u'τοῖς/ταῖς']
    split = form.split(' ')
    if len(split) == 2 and split[0] in articles:
        return " ".join(split[1:])
    return form


def parse_args():
    parser = argparse.ArgumentParser('Nouns')
    parser.add_argument('--get')
    parser.add_argument('--show')
    parser.add_argument('--anki', action='store_true')
    return parser.parse_args()


def get_noun_forms(html):
    # Go through lines until table.*inflection-table
    # Grab the headers for the first tr (Sing, Dual, Plur)
    # Grab the header of the next tr (Nom, or Gen, etc.)
    # Grab the td values, setting map['singular']['nominative'] etc.

    headers = []

    gender = None

    inflection_table = False
    first_tr = False
    data_trs = False

    data_header = None
    data_group = 0

    table_done = False

    forms = {}

    for line in html.split('\n'):

        if not gender:
            gen_re = r'^.*<abbr title="(.*) gender">.</abbr>.*$'
            gender_match = re.match(gen_re, line)
            if gender_match:
                gender = gender_match.group(1)
                forms['gender'] = gender

        if table_done:
            continue

        if not inflection_table:
            if re.match(r'^.*table.*inflection-table.*$', line):
                inflection_table = True
                first_tr = True
            continue
        if re.match(r'^.*</table>.*', line):
            table_done = True

        if first_tr:
            if re.match(r'^.*</tr>.*', line):
                first_tr = False
                data_trs = True
            header_match = re.match(r'^.*<th.*?>(.*)</th>.*$', line)
            if header_match:
                header = header_match.group(1)
                header = re.sub(r'<.*?>', '', header)
                headers.append(header)

        if data_trs:
            header_match = re.match(r'^.*<th.*?>(.*)</th>.*$', line)
            if header_match:
                header = header_match.group(1)
                header = re.sub(r'<.*?>', '', header)
                data_header = header
                data_group = 0
            data_match = re.match(r'^.*<td.*<a.*>(.*)</a>.*</td>.*$', line)
            if data_match:
                word = data_match.group(1)
                data_group += 1
                header = headers[data_group]
                if not forms.get(header):
                    forms[header] = {}
                forms[header][data_header] = unicode(word, 'utf-8')
            data_match2 = re.match(r'^.*<td.*<spa.*>(.*)</span></td>.*$', line)
            if not data_match and data_match2:
                word = data_match2.group(1)
                data_group += 1
                header = headers[data_group]
                if not forms.get(header):
                    forms[header] = {}
                forms[header][data_header] = unicode(word, 'utf-8')

    return forms


def save_forms(noun, forms):
    SHELF[noun] = forms


if __name__ == '__main__':
    global SHELF
    SHELF = shelve.open('nouns.shelf')
    main()
    SHELF.close()
