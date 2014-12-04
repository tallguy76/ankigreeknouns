#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import re
import shelve

import ankigreekutil as anki


WIKTIONARY = 'http://en.wiktionary.org/wiki/'
WORDS = ['λύω']
REPRESENTATIONS = {'imperfect': 'i',
                   'present': 'p',
                   'future': 'f',
                   'perfect': 'per',
                   'pluperfect': 'plup',
                   'aorist': 'f',
                   'future perfect': 'futp',
                   '1st future': 'f',
                   '1st aorist': 'a',
                   '2nd aorist': 'a',
                   '1st perfect': 'per',
                   '2nd perfect': 'per',
                   '1st pluperfect': 'plup',
                   '2nd pluperfect': 'plup',
                   'indicative': 'i',
                   'imperative': 'imp',
                   'subjunctive': 's',
                   'optative': 'o',
                   'participle': '',
                   '1st': 's1',
                   '2nd': 's2',
                   '3rd': 's3',
                   '2nd dual': 'd2',
                   '3rd dual': 'd3',
                   '1st plural': 'p1',
                   '2nd plural': 'p2',
                   '3rd plural': 'p3',
                   'infinitive': 'inf',
                   'active': '',
                   'middle': 'mid',
                   'mid-pas': 'm-p',
                   'passive': 'pas',
                   'Singular': 's',
                   'Dual': 'd',
                   'Plural': 'p',
                   'Nominative': 'n',
                   'Vocative': 'v',
                   'Genitive': 'g',
                   'Dative': 'd',
                   'Accusative': 'a'
                   }
VOICE = ['active', 'middle', 'mid-pas', 'passive']
MOOD = ['indicative', 'subjunctive', 'optative', 'imperative', 'infinitive',
        'participle']
TENSE = ['present', 'imperfect', 'future', '1st future', '1st aorist',
         '2nd aorist', 'perfect', '1st perfect', '2nd perfect', 'pluperfect',
         '1st pluperfect', '2nd pluperfect', 'future perfect']
PERSON = ['1st', '2nd', '3rd', '2nd dual', '3rd dual', '1st plural',
          '2nd plural', '3rd plural']
GENDER = ['m', 'f', 'n']
CASE = ['Nominative', 'Vocative', 'Genitive', 'Dative', 'Accusative']
NUMBER = ['Singular', 'Dual', 'Plural']
VERBFILE = 'verbs'
REVERSEFILE = 'reverse_verbs'


def set_verb_form(verb, voice, mood, tense, forms):
    if not verb.get(voice):
        verb[voice] = {}
    if not verb[voice].get(mood):
        verb[voice][mood] = {}
    if not verb[voice][mood].get(tense):
        verb[voice][mood][tense] = {}
    else:
        raise Exception('Redefinition')

    if mood == 'infinitive':
        verb[voice][mood][tense] = forms
        return

    if mood == 'participle':
        part_cases = {'Singular': ['Nominative', 'Genitive', 'Dative',
                                   'Accusative', 'Vocative'],
                      'Dual':     ['Nominative', 'Genitive'],
                      'Plural':   ['Nominative', 'Genitive', 'Dative',
                                   'Accusative']}

        for number in NUMBER:
            verb[voice][mood][tense][number] = {}
            for ii, cc in enumerate(part_cases[number]):
                iiadj = ii
                if number == 'Dual' or number == 'Plural':
                    iiadj += len(part_cases['Singular'])
                if number == 'Plural':
                    iiadj += len(part_cases['Dual'])
                verb[voice][mood][tense][number][cc] = {}
                for jj, gg in enumerate(GENDER):
                    verb[voice][mood][tense][number][cc][gg] = forms[iiadj][jj]
            if number == 'Dual':
                nom = verb[voice][mood][tense][number]['Nominative']
                verb[voice][mood][tense][number]['Vocative'] = nom
                verb[voice][mood][tense][number]['Accusative'] = nom
                gen = verb[voice][mood][tense][number]['Genitive']
                verb[voice][mood][tense][number]['Dative'] = gen
            if number == 'Plural':
                nom = verb[voice][mood][tense][number]['Nominative']
                verb[voice][mood][tense][number]['Vocative'] = nom
        return

    for ii in range(0, len(PERSON)):
        verb[voice][mood][tense][PERSON[ii]] = forms[ii]


def prepare_shelf():
    luo = {}

    # Active
    set_verb_form(luo, 'active', 'indicative', 'present',
                  ['λύ̄ω', 'λύ̄εις', 'λύ̄ει', 'λύ̄ετον', 'λύ̄ετον',
                   'λύ̄ομεν', 'λύ̄ετε', 'λύ̄ουσι'])
    set_verb_form(luo, 'active', 'indicative', 'imperfect',
                  ['ἔλῡον', 'ἔλῡες', 'ἔλῡε', 'ἐλύ̄ετον', 'ἐλῡέτην', 'ἐλύ̄ομεν',
                   'ἐλύ̄ετε', 'ἔλῡον'])
    set_verb_form(luo, 'active', 'indicative', 'future',
                  ['λύ̄σω', 'λύ̄σεις', 'λύ̄σει', 'λύ̄σετον', 'λύ̄σετον',
                   'λύ̄σομεν', 'λύ̄σετε', 'λύ̄σουσι'])
    set_verb_form(luo, 'active', 'subjunctive', 'present',
                  ['λύ̄ω', 'λύ̄ῃς', 'λύ̄ῃ', 'λύ̄ητον', 'λύ̄ητον', 'λύ̄ωμεν',
                   'λύ̄ητε', 'λύ̄ωσι'])
    set_verb_form(luo, 'active', 'optative', 'present',
                  ['λύ̄οιμι', 'λύ̄οις', 'λύ̄οι', 'λύ̄οιτον', 'λῡοίτην',
                   'λύ̄οιμεν', 'λύ̄οιτε', 'λύ̄οιεν'])
    set_verb_form(luo, 'active', 'optative', 'future',
                  ['λύ̄σοιμι', 'λύ̄σοις', 'λύ̄σοι', 'λύ̄σοιτον', 'λῡσοίτην',
                   'λύ̄σοιμεν', 'λύ̄σοιτε', 'λύ̄σοιεν'])
    set_verb_form(luo, 'active', 'imperative', 'present',
                  ['', 'λῦε', 'λῡέτω', 'λύ̄ετον', 'λῡέτων', '', 'λύ̄ετε',
                   'λῡόντων'])
    set_verb_form(luo, 'active', 'infinitive', 'present', 'λύ̄ειν')
    set_verb_form(luo, 'active', 'infinitive', 'future', 'λύ̄σειν')

    set_verb_form(luo, 'active', 'participle', 'present',
                  [['λύ̄ων', 'λύ̄ουσα', 'λῦον'],
                   ['λύ̄οντος', 'λῡούσης', 'λύ̄οντος'],
                   ['λύ̄οντι', 'λῡούσῃ', 'λύ̄οντι'],
                   ['λύ̄οντα', 'λύ̄ουσαν', 'λῦον'],
                   ['λύ̄ων', 'λύ̄ουσα', 'λῦον'],
                   ['λύ̄οντε', 'λῡούσᾱ', 'λύ̄οντε'],
                   ['λῡόντοιν', 'λῡούσαιν', 'λῡόντοιν'],
                   ['λύ̄οντες', 'λύ̄ουσαι', 'λύ̄οντα'],
                   ['λῡόντων', 'λῡουσῶν', 'λῡόντων'],
                   ['λύ̄ουσι(ν)', 'λῡούσαις', 'λύ̄ουσι(ν)'],
                   ['λύ̄οντας', 'λῡούσᾱς', 'λύ̄οντα']])

    set_verb_form(luo, 'active', 'participle', 'future',
                  [['λύ̄σων', 'λύ̄σουσα', 'λῦσον'],
                   ['λύ̄σοντος', 'λῡσούσης', 'λύ̄σοντος'],
                   ['λύ̄σοντι', 'λῡσούσῃ', 'λύ̄σοντι'],
                   ['λύ̄σοντα', 'λύ̄σουσαν', 'λῦσον'],
                   ['λύ̄σων', 'λύ̄σουσα', 'λῦσον'],
                   ['λύ̄σοντε', 'λῡσούσᾱ', 'λύ̄σοντε'],
                   ['λῡσόντοιν', 'λῡσούσαιν', 'λῡσόντοιν'],
                   ['λύ̄σοντες', 'λύ̄σουσαι', 'λύ̄σοντα'],
                   ['λῡσόντων', 'λῡσουσῶν', 'λῡσόντων'],
                   ['λύ̄σουσι(ν)', 'λῡσούσαις', 'λύ̄σουσι(ν)'],
                   ['λύ̄σοντας', 'λῡσούσᾱς', 'λύ̄σοντα']])

    set_verb_form(luo, 'active', 'indicative', '1st aorist',
                  ['ἔλῡσα', 'ἔλῡσας', 'ἔλῡσε', 'ἐλύ̄σατον', 'ἐλῡσάτην',
                   'ἐλύ̄σαμεν', 'ἐλύ̄σατε', 'ἔλῡσαν'])
    set_verb_form(luo, 'active', 'indicative', '1st perfect',
                  ['λέλυκα', 'λέλυκας', 'λέλυκε', 'λελύκατον', 'λελύκατον',
                   'λελύκαμεν', 'λελύκατε', 'λελύκᾱσι'])
    set_verb_form(luo, 'active', 'indicative', '1st pluperfect',
                  ['ἐλελύκη', 'ἐλελύκης', 'ἐλελύκει(ν)', 'ἐλελύκετον',
                   'ἐλελυκέτην', 'ἐλελύκεμεν', 'ἐλελύκετε', 'ἐλελύκεσαν'])

    set_verb_form(luo, 'active', 'subjunctive', '1st aorist',
                  ['λύ̄σω', 'λύ̄σῃς', 'λύ̄σῃ', 'λύ̄σητον', 'λύ̄σητον',
                   'λύ̄σωμεν', 'λύ̄σητε', 'λύ̄σωσι'])

    set_verb_form(luo, 'active', 'subjunctive', '1st perfect',
                  ['λελυκὼς ὦ / λελύκω', 'λελυκὼς ᾖς / λελύκῃς',
                   'λελυκὼς ᾖ / λελύκῃ', 'λελυκότε ἦτον / λελύκητον',
                   'λελυκότε ἦτον / λελύκητον', 'λελυκότες ὦμεν / λελύκωμεν',
                   'λελυκότες ἦτε / λελύκητε', 'λελυκότες ὦσι / λελύκωσι'])

    set_verb_form(luo, 'active', 'optative', '1st aorist',
                  ['λύ̄σαιμι', 'λύ̄σαις / λύ̄σειας', 'λύ̄σαι / λύ̄σειε',
                   'λύ̄σαιτον', 'λῡσαίτην', 'λύ̄σαιμεν', 'λύ̄σαιτε',
                   'λύ̄σαιεν / λύ̄σειαν'])

    set_verb_form(luo, 'active', 'optative', '1st perfect',
                  ['λελυκὼς εἴην / λελύκοιμι / λελύκοίην',
                   'λελυκὼς εἴης / λελύκοις / λελύκοίης',
                   'λελυκὼς εἴη / λελύκοι / λελύκοίη',
                   'λελυκότε εἴητον / λελυκότε εἶτον / λελύκοιτον',
                   'λελυκότε εἰήτην / λελυκότε εἴτην / λελυκοίτην',
                   'λελυκότες εἴημεν / λελυκότες εἶμεν / λελύκοιμεν',
                   'λελυκότες εἴητε / λελυκότες εἶτε / λελύκοιτε',
                   'λελυκότες εἴησαν / λελυκότες εἶεν / λελύκοιεν'])

    set_verb_form(luo, 'active', 'imperative', '1st aorist',
                  ['', 'λῦσον', 'λῡσάτω', 'λύ̄σατον', 'λῡσάτων', '',
                   'λύ̄σατε', 'λῡσάντων'])

    set_verb_form(luo, 'active', 'imperative', '1st perfect',
                  ['', 'λελυκὼς ἴσθι / λέλυκε', 'λελυκὼς ἔστω / λελυκέτω',
                   'λελυκότε ἔστον / λελύκετον',
                   'λελυκότε ἔστων / λελυκέτων', '',
                   'λελυκότες ἐστέ / λελύκετε', 'λελυκότες ὄντων'])

    set_verb_form(luo, 'active', 'infinitive', '1st aorist', 'λῦσαι')
    set_verb_form(luo, 'active', 'infinitive', '1st perfect', 'λελυκέναι')

    set_verb_form(luo, 'active', 'participle', '1st aorist',
                  [['λύ̄σᾱς', 'λύ̄σᾱσα', 'λῦσαν'],
                   ['λύ̄σαντος', 'λῡσά̄σης', 'λύ̄σαντος'],
                   ['λύ̄σαντι', 'λῡσά̄σῃ', 'λύ̄σαντι'],
                   ['λύ̄σαντα', 'λύ̄σᾱσαν', 'λῦσαν'],
                   ['λύ̄σᾱς', 'λύ̄σᾱσα', 'λῦσαν'],
                   ['λύ̄σαντε', 'λῡσά̄σᾱ', 'λύ̄σαντε'],
                   ['λῡσάντοιν', 'λῡσά̄σαιν', 'λῡσάντοιν'],
                   ['λύ̄σαντες', 'λύ̄σᾱσαι', 'λύ̄σαντα'],
                   ['λῡσάντων', 'λῡσᾱσῶν', 'λῡσάντων'],
                   ['λύ̄σᾱσι(ν)', 'λῡσά̄σαις', 'λύ̄σᾱσι(ν)'],
                   ['λύ̄σαντας', 'λῡσά̄σας', 'λύ̄σαντα']])

    set_verb_form(luo, 'active', 'participle', '1st perfect',
                  [['λελυκώς', 'λελυκυῖα', 'λελυκός'],
                   ['λελυκότος', 'λελυκυίᾱς', 'λελυκότος'],
                   ['λελυκότι', 'λελυκυίᾳ', 'λελυκότι'],
                   ['λελυκότα', 'λελυκυῖαν', 'λελυκός'],
                   ['λελυκώς', 'λελυκυῖα', 'λελυκός'],
                   ['λελυκότε', 'λελυκυίᾱ', 'λελυκότε'],
                   ['λελυκότοιν', 'λελυκυίαιν', 'λελυκότοιν'],
                   ['λελυκότες', 'λελυκυῖαι', 'λελυκότα'],
                   ['λελυκότων', 'λελυκυλῶν', 'λελυκότων'],
                   ['λελυκόσι(ν)', 'λελυκυίαις', 'λελυκόσι(ν)'],
                   ['λελυκότας', 'λελυκυίᾱς', 'λελυκότα']])

    # Middle

    set_verb_form(luo, 'mid-pas', 'indicative', 'present',
                  ['λύ̄ομαι', 'λύ̄ῃ / λύ̄ει', 'λύ̄εται', 'λύ̄εσθον',
                   'λύ̄εσθον', 'λῡόμεθα', 'λύ̄εσθε', 'λύ̄ονται'])

    set_verb_form(luo, 'mid-pas', 'indicative', 'imperfect',
                  ['ἐλῡόμην', 'ἐλύ̄ου', 'ἐλύ̄ετο', 'ἐλύ̄εσθον', 'ἐλῡέσθην',
                   'ἐλῡόμεθα', 'ἐλύ̄εσθε', 'ἐλύ̄οντο'])

    set_verb_form(luo, 'middle', 'indicative', 'future',
                  ['λύ̄σομαι', 'λύ̄σῃ / λύ̄σει', 'λύ̄σεται', 'λύ̄σεσθον',
                   'λύ̄σεσθον', 'λῡσόμεθα', 'λύ̄σεσθε', 'λύ̄σονται'])

    set_verb_form(luo, 'mid-pas', 'subjunctive', 'present',
                  ['λύ̄ωμαι', 'λύ̄ῃ', 'λύ̄ηται', 'λύ̄ησθον', 'λύ̄ησθον',
                   'λῡώμεθα', 'λύ̄ησθε', 'λύ̄ωνται'])

    set_verb_form(luo, 'mid-pas', 'optative', 'present',
                  ['λῡοίμην', 'λύ̄οιο', 'λύ̄οιτο', 'λύ̄οισθον', 'λῡοίσθην',
                   'λῡοίμεθα', 'λύ̄οισθε', 'λύ̄οιντο'])

    set_verb_form(luo, 'middle', 'optative', 'future',
                  ['λῡσοίμην', 'λύ̄σοιο', 'λύ̄σοιτο', 'λύ̄σοισθον',
                   'λῡσοίσθην', 'λῡσοίμεθα', 'λύ̄σοισθε', 'λύ̄σοιντο'])

    set_verb_form(luo, 'mid-pas', 'imperative', 'present',
                  ['', 'λύ̄ου', 'λῡέσθω', 'λύ̄εσθον', 'λῡέσθων', '', 'λύ̄εσθε',
                   'λῡέσθων'])

    set_verb_form(luo, 'mid-pas', 'infinitive', 'present', 'λύ̄εσθαι')
    set_verb_form(luo, 'middle', 'infinitive', 'future', 'λύ̄σεσθαι')

    set_verb_form(luo, 'mid-pas', 'participle', 'present',
                  [['λῡόμενος', 'λῡομένη', 'λῡόμενον'],
                   ['λῡομένου', 'λῡομένης', 'λῡομένου'],
                   ['λῡομένῳ', 'λῡομένῃ', 'λῡομένῳ'],
                   ['λῡόμενον', 'λῡομένην', 'λῡόμενον'],
                   ['λῡόμενε', 'λῡομένη', 'λῡόμενον'],
                   ['λῡομένω', 'λῡομένᾱ', 'λῡομένω'],
                   ['λῡομένοιν', 'λῡομέναιν', 'λῡομένοιν'],
                   ['λῡόμενοι', 'λῡόμεναι', 'λῡόμενα'],
                   ['λῡομένων', 'λῡομένων', 'λῡομένων'],
                   ['λῡομένοις', 'λῡομέναις', 'λῡομένοις'],
                   ['λῡομένους', 'λῡομένᾱς', 'λῡόμενα']])

    set_verb_form(luo, 'middle', 'participle', 'future',
                  [['λῡσόμενος', 'λῡσομένη', 'λῡσόμενον'],
                   ['λῡσομένου', 'λῡσομένης', 'λῡσομένου'],
                   ['λῡσομένῳ', 'λῡσομένῃ', 'λῡσομένῳ'],
                   ['λῡσόμενον', 'λῡσομένην', 'λῡσόμενον'],
                   ['λῡσόμενε', 'λῡσομένη', 'λῡσόμενον'],
                   ['λῡσομένω', 'λῡσομένᾱ', 'λῡσομένω'],
                   ['λῡσομένοιν', 'λῡσομέναιν', 'λῡσομένοιν'],
                   ['λῡσόμενοι', 'λῡσόμεναι', 'λῡσόμενα'],
                   ['λῡσομένων', 'λῡσομένων', 'λῡσομένων'],
                   ['λῡσομένοις', 'λῡσομέναις', 'λῡσομένοις'],
                   ['λῡσομένους', 'λῡσομένᾱς', 'λῡσόμενα']])

    set_verb_form(luo, 'middle', 'indicative', '1st aorist',
                  ['ἐλῡσάμην', 'ἐλύ̄σω', 'ἐλύ̄σατο', 'ἐλύ̄σασθον', 'ἐλῡσάσθην',
                      'ἐλῡσάμεθα', 'ἐλύ̄σασθε', 'ἐλύ̄σαντο'])

    set_verb_form(luo, 'mid-pas', 'indicative', 'perfect',
                  ['λέλυμαι', 'λέλυσαι', 'λέλυται', 'λέλυσθον', 'λέλυσθον',
                   'λελύμεθα', 'λέλυσθε', 'λέλυνται'])

    set_verb_form(luo, 'mid-pas', 'indicative', 'pluperfect',
                  ['ἐλελύμην', 'ἐλέλυσο', 'ἐλέλυτο', 'ἐλέλυσθον',
                   'ἐλελύσθην', 'ἐλελύμεθα', 'ἐλέλυσθε', 'ἐλέλυντο'])

    set_verb_form(luo, 'middle', 'subjunctive', '1st aorist',
                  ['λύ̄σωμαι', 'λύ̄σῃ', 'λύ̄σηται', 'λύ̄σησθον', 'λύ̄σησθον',
                   'λῡσώμεθα', 'λύ̄σησθε', 'λύ̄σωνται'])

    set_verb_form(luo, 'mid-pas', 'subjunctive', 'perfect',
                  ['λελυμένος ὦ', 'λελυμένος ᾖς', 'λελυμένος ᾖ',
                   'λελυμένω ἦτον', 'λελυμένω ἦτον', 'λελυμένοι ὦμεν',
                   'λελυμένοι ἦτε', 'λελυμένοι ὦσι'])

    set_verb_form(luo, 'middle', 'optative', '1st aorist',
                  ['λῡσαίμην', 'λύ̄σαιο', 'λύ̄σαιτο', 'λύ̄σαισθον',
                   'λῡσαίσθην', 'λῡσαίμεθα', 'λύ̄σαισθε', 'λύ̄σαιντο'])

    set_verb_form(luo, 'mid-pas', 'optative', 'perfect',
                  ['λελυμένος εἴην', 'λελυμένος εἴης', 'λελυμένος εἴη',
                   'λελυμένω εἴητον / λελυμένω εἶτον',
                   'λελυμένω εἰήτην / λελυμένω εἴτην',
                   'λελυμένοι εἴημεν / λελυμένοι εἶμεν',
                   'λελυμένοι εἴητε / λελυμένοι εἶτε',
                   'λελυμένοι εἴησαν / λελυμένοι εἶεν'])

    set_verb_form(luo, 'middle', 'imperative', '1st aorist',
                  ['', 'λῦσαι', 'λῡσάσθω', 'λύ̄σασθον', 'λῡσάσθων', '',
                   'λύ̄σασθε', 'λῡσάσθων'])

    set_verb_form(luo, 'mid-pas', 'imperative', 'perfect',
                  ['', 'λέλυσο', 'λελύσθω', 'λέλυσθον', 'λελύσθων', '',
                   'λέλυσθε', 'λελύσθων'])

    set_verb_form(luo, 'middle', 'infinitive', '1st aorist', 'λύ̄σασθαι')
    set_verb_form(luo, 'mid-pas', 'infinitive', 'perfect', 'λελύσθαι')

    set_verb_form(luo, 'middle', 'participle', '1st aorist',
                  [['λῡσάμενος', 'λῡσαμένη', 'λῡσάμενον'],
                   ['λῡσαμένου', 'λῡσαμένης', 'λῡσαμένου'],
                   ['λῡσαμένῳ', 'λῡσαμένῃ', 'λῡσαμένῳ'],
                   ['λῡσάμενον', 'λῡσαμένην', 'λῡσάμενον'],
                   ['λῡσάμενε', 'λῡσαμένη', 'λῡσάμενον'],
                   ['λῡσαμένω', 'λῡσαμένᾱ', 'λῡσαμένω'],
                   ['λῡσαμένοιν', 'λῡσαμέναιν', 'λῡσαμένοιν'],
                   ['λῡσάμενοι', 'λῡσάμεναι', 'λῡσάμενα'],
                   ['λῡσαμένων', 'λῡσαμένων', 'λῡσαμένων'],
                   ['λῡσαμένοις', 'λῡσαμέναις', 'λῡσαμένοις'],
                   ['λῡσαμένους', 'λῡσαμένᾱς', 'λῡσάμενα']])

    set_verb_form(luo, 'mid-pas', 'participle', 'perfect',
                  [['λελῡομένος', 'λελῡομένη', 'λελῡομενον'],
                   ['λελῡομένου', 'λελῡομένης', 'λελῡομένου'],
                   ['λελῡομένῳ', 'λελῡομένῃ', 'λελῡομένῳ'],
                   ['λελῡομένον', 'λελῡομένην', 'λελῡομενον'],
                   ['λελῡομένε', 'λελῡομένη', 'λελῡομενον'],
                   ['λελῡομένω', 'λελῡομένᾱ', 'λελῡομένω'],
                   ['λελῡομένοιν', 'λελῡομέναιν', 'λελῡομένοιν'],
                   ['λελῡομένοι', 'λελῡομεναι', 'λελῡομενα'],
                   ['λελῡομένων', 'λελῡομένων', 'λελῡομένων'],
                   ['λελῡομένοις', 'λελῡομέναις', 'λελῡομένοις'],
                   ['λελῡομένους', 'λελῡομένᾱς', 'λελῡόμενα']])

    # Passive
    set_verb_form(luo, 'passive', 'indicative', 'future perfect',
                  ['λελύ̄σομαι', 'λελύ̄σῃ / λελύ̄σει', 'λελύ̄σεται',
                   'λελύ̄σεσθον', 'λελύ̄σεσθον', 'λελῡσόμεθα', 'λελύ̄σεσθε',
                   'λελύ̄σονται'])

    set_verb_form(luo, 'passive', 'indicative', '1st aorist',
                  ['ἐλύθην', 'ἐλύθης', 'ἐλύθη', 'ἐλύθητον', 'ἐλυθήτην',
                   'ἐλύθημεν', 'ἐλύθητε', 'ἐλύθησαν'])

    set_verb_form(luo, 'passive', 'indicative', '1st future',
                  ['λυθήσομαι', 'λυθήσῃ / λυθήσει', 'λυθήσεται',
                   'λυθήσεσθον', 'λυθήσεσθον', 'λυθησόμεθα', 'λυθήσεσθε',
                   'λυθήσονται'])

    set_verb_form(luo, 'passive', 'subjunctive', '1st aorist',
                  ['λυθῶ', 'λυθῇς', 'λυθῇ', 'λυθῆτον', 'λυθῆτον',
                   'λυθῶμεν', 'λυθῆτε', 'λυθῶσι'])

    set_verb_form(luo, 'passive', 'optative', 'future perfect',
                  ['λελῡσοίμην', 'λελύ̄σοιο', 'λελύ̄σοιτο', 'λελύ̄σοισθον',
                   'λελῡσοίσθην', 'λελῡσοίμεθα', 'λελύ̄σοισθε', 'λελύ̄σοιντο'])

    set_verb_form(luo, 'passive', 'optative', '1st aorist',
                  ['λυθείην', 'λυθείης', 'λυθείη', 'λυθεῖτον / λυθείητον',
                   'λυθείτην / λυθειήτην', 'λυθεῖμεν / λυθείημεν',
                   'λυθεῖτε / λυθείητε', 'λυθεῖεν / λυθείησαν'])

    set_verb_form(luo, 'passive', 'optative', '1st future',
                  ['λυθησοίμην', 'λυθήσοιο', 'λυθήσοιτο', 'λυθήσοισθον',
                   'λυθησοίσθην', 'λυθησοίμεθα', 'λυθήσοισθε', 'λυθήσοιντο'])

    set_verb_form(luo, 'passive', 'imperative', '1st aorist',
                  ['', 'λύθητι', 'λυθήτω', 'λύθητον', 'λυθήτων', '',
                   'λύθητε', 'λυθέντων'])

    set_verb_form(luo, 'passive', 'infinitive', 'future perfect',
                  'λελύ̄σεσθαι')
    set_verb_form(luo, 'passive', 'infinitive', '1st aorist', 'λυθῆναι')
    set_verb_form(luo, 'passive', 'infinitive', '1st future', 'λυθήσεσθαι')

    set_verb_form(luo, 'passive', 'participle', 'future perfect',
                  [['λελῡσόμενος', 'λελῡσομένη', 'λελῡσόμενον'],
                   ['λελῡσομένου', 'λελῡσομένης', 'λελῡσομένου'],
                   ['λελῡσομένῳ', 'λελῡσομένῃ', 'λελῡσομένῳ'],
                   ['λελῡσόμενον', 'λελῡσομένην', 'λελῡσόμενον'],
                   ['λελῡσόμενε', 'λελῡσομένη', 'λελῡσόμενον'],
                   ['λελῡσομένω', 'λελῡσομένᾱ', 'λελῡσομένω'],
                   ['λελῡσομένοιν', 'λελῡσομέναιν', 'λελῡσομένοιν'],
                   ['λελῡσόμενοι', 'λελῡσόμεναι', 'λελῡσόμενα'],
                   ['λελῡσομένων', 'λελῡσομένων', 'λελῡσομένων'],
                   ['λελῡσομένοις', 'λελῡσομέναις', 'λελῡσομένοις'],
                   ['λελῡσομένους', 'λελῡσομένᾱς', 'λελῡσόμενα']])

    set_verb_form(luo, 'passive', 'participle', '1st aorist',
                  [['λυθείς', 'λυθεῖσα', 'λυθέν'],
                   ['λυθέντος', 'λυθείσης', 'λυθέντος'],
                   ['λυθέντι', 'λυθείσῃ', 'λυθέντι'],
                   ['λυθέντα', 'λυθεῖσαν', 'λυθέν'],
                   ['λυθείς', 'λυθεῖσα', 'λυθέν'],
                   ['λυθέντε', 'λυθείσᾱ', 'λυθέντε'],
                   ['λυθέντοιν', 'λυθείσαιν', 'λυθέντοιν'],
                   ['λυθέντες', 'λυθεῖσαι', 'λυθέντα'],
                   ['λυθέντων', 'λυθεισῶν', 'λυθέντων'],
                   ['λυθεῖσι(ν)', 'λυθείσαις', 'λυθεῖσι(ν)'],
                   ['λυθέντας', 'λυθείσᾱς', 'λυθέντα']])

    set_verb_form(luo, 'passive', 'participle', '1st future',
                  [['λυθησόμενος', 'λυθησομένη', 'λυθησόμενον'],
                   ['λυθησομένου', 'λυθησομένης', 'λυθησομένου'],
                   ['λυθησομένῳ', 'λυθησομένῃ', 'λυθησομένῳ'],
                   ['λυθησόμενον', 'λυθησομένην', 'λυθησόμενον'],
                   ['λυθησόμενε', 'λυθησομένη', 'λυθησόμενον'],
                   ['λυθησομένω', 'λυθησομένᾱ', 'λυθησομένω'],
                   ['λυθησομένοιν', 'λυθησομέναιν', 'λυθησομένοιν'],
                   ['λυθησόμενοι', 'λυθησόμεναι', 'λυθησόμενα'],
                   ['λυθησομένων', 'λυθησομένων', 'λυθησομένων'],
                   ['λυθησομένοις', 'λυθησομέναις', 'λυθησομένοις'],
                   ['λυθησομένους', 'λυθησομένᾱς', 'λυθησόμενα']])

    SHELF['λύω'] = luo


def parse_args():
    parser = argparse.ArgumentParser('Verbs')
    parser.add_argument('--get')
    parser.add_argument('--show')
    parser.add_argument('--anki', action='store_true')
    parser.add_argument('--showtenses', action='store_true')
    parser.add_argument('--tenses',
                        help="comma-separated list of tenses to study")
    return parser.parse_args()


def make_answer(voice, mood, tense, person=None):
    answer = REPRESENTATIONS[tense] + REPRESENTATIONS[mood] + ' '
    answer += REPRESENTATIONS[voice]
    if person != None:
        answer += ' ' + REPRESENTATIONS[person]
    return answer


def make_participle_answer(voice, mood, tense, number, case, gender):
    answer = make_answer(voice, mood, tense)
    return unicode(answer, 'utf-8') + " " + gender + REPRESENTATIONS[number] + REPRESENTATIONS[case]

def ignore_case(gender,number,case):
  if number is 'Dual':
    if case in ['Accusative','Vocative','Dative']:
      return True
  if number is 'Plural':
    if case is 'Vocative':
      return True
  if gender is 'n':
    if case in ['Accusative','Vocative']:
      return True
  return False

def all_words(word):
    output = []
    words = word.split(' / ')
    for word in words:
        if re.match(r'^.*\(ν\)$', word):
            output.append(word[0:-4])
            output.append(word[0:-4] + 'ν')
            continue
        if word:
            output.append(word)
    return output


def make_cards(word, tenses):
    cards = []

    if tenses:
        mytenses = tenses.split(',')
    else:
        mytenses = TENSE
    for tense in mytenses:
        if tense not in TENSE:
            raise Exception('Bad tense: ' + tense)

    # Verify
    for vv in word.keys():
        if vv not in VOICE:
            raise Exception('bad voice: ' + vv)
        for mm in word[vv].keys():
            if mm not in MOOD:
                raise Exception('bad mood: ' + mm)
            for tt in word[vv][mm]:
                if tt not in TENSE:
                    raise Exception('bad tense: ' + tt)

    for vv in VOICE:
        for mm in word[vv].keys():
            if mm == 'participle':
                for tt in mytenses:
                    if not word[vv][mm].get(tt):
                        continue
                    for nn in NUMBER:
                        for cc in CASE:
                            for gg in GENDER:
                                if ignore_case(gg,nn,cc):
                                  continue
                                words = all_words(word[vv][mm][tt][nn][cc][gg])
                                for form in words:
                                    if form:
                                        answer = make_participle_answer(vv,
                                                                        mm,
                                                                        tt,
                                                                        nn,
                                                                        cc,
                                                                        gg)
                                        cards.append([form,
                                                      answer.encode('utf-8')])
                continue
            if mm == 'infinitive':
                for tt in mytenses:
                    if word[vv][mm].get(tt):
                        for form in all_words(word[vv][mm][tt]):
                            form = word[vv][mm][tt]
                            cards.append([form, make_answer(vv, mm, tt)])
                continue
            # for normal moods
            for tt in mytenses:
                if not word[vv][mm].get(tt):
                    continue
                for pp in PERSON:
                    for form in all_words(word[vv][mm][tt][pp]):
                        cards.append([form, make_answer(vv, mm, tt, pp)])
    return cards


def output_cards(tenses=None):
    cards = []
    for word in WORDS:
        cards.extend(make_cards(SHELF[word], tenses))
    card_mm = {}
    card_rr = {}
    for card in cards:
        if not card_mm.get(card[0]):
            card_mm[card[0]] = []
        if not card_rr.get(card[1]):
            card_rr[card[1]] = []
        unique = True
        for cc in card_mm[card[0]]:
            if card[1] == cc:
                unique = False
        if unique:
            card_mm[card[0]].append(card[1])
        unique = True
        for cc in card_rr[card[1]]:
            if card[0] == cc:
                unique = False
        if unique:
            card_rr[card[1]].append(card[0])
    verbfile = VERBFILE + '.txt'
    reversefile = REVERSEFILE + '.txt'
    if tenses:
        verbfile = VERBFILE + '.' + tenses + '.txt'
        reversefile = REVERSEFILE + '.' + tenses + '.txt'
    with open(verbfile, 'w') as ff:
        for kk, vv in card_mm.iteritems():
            ff.write(kk + '; ' + '<br>'.join(vv) + "\n")
    with open(reversefile, 'w') as ff:
        for kk, vv in card_rr.iteritems():
            ff.write(kk + '; ' + '<br>'.join(vv) + "\n")


def main():
    args = parse_args()
    if args.showtenses:
        print TENSE
    if args.get:
        prepare_shelf()
    if args.show:
        anki.show_forms(args.show, SHELF)
    if args.anki:
        output_cards(args.tenses)


if __name__ == '__main__':
    global SHELF
    SHELF = shelve.open('verbs.shelf')
    main()
    SHELF.close()
