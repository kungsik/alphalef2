'''
bhsVersion.py
Text-Fabric api를 이용한 히브리어 텍스트 가공
로컬 환경에서 데이터 위치
C:/Users/kungs/text-fabric-data/bhsa
C:/Users/kungs/github/text-fabric-data/bhsa
C:/Users/kungs/Dropbox/text-fabric-data/bhsa
'''

from tf.fabric import Fabric
BHSA = 'bhsa'
TH = Fabric(modules=BHSA, silent=False)
bhs = TH.load('''
    book chapter verse
    nu gn ps vt vs st
    otype typ function
    pdp qere_utf8 qere_trailer_utf8
    g_word_utf8 trailer_utf8
    g_prs_utf8 g_uvf_utf8
    prs_gn prs_nu prs_ps 
    phono voc_utf8 
''')
#예비: g_cons_utf8 (본문 자음 형태 검색시 필요함 나중에 판단해서 넣을지 고려.), lex_utf8(검색시 필요한 항목. 테스트용으로 빼놓음)
#삭제된 요소들: lex, g_lex_utf8, det, gloss
# gloss를 없애고 나중에 스트롱 코드 매칭하여 의미 추가.

# from collections import OrderedDict
from bibleapi.controller import translate

# 히브리어 텍스트 불러오기
def getBhs(book='Genesis', chapter=1, bhs=bhs):
    chpNode = bhs.T.nodeFromSection((book, chapter))
    verseNode = bhs.L.d(chpNode, otype='verse')
    verse = '''
        <div class='verse_heb' ref='verse'>
        <div style="text-align:left">
        <b-button size='sm' id='syntax_enact' ref='syntax' variant='outline-secondary' @click='hebsyntax'>구문단위표시</b-button>
        </div>
        <ol>
    '''
 
    for v in verseNode:
        verse += '<li>'
        wordsNode = bhs.L.d(v, otype='word')
        for w in wordsNode:
            clauseNode = bhs.L.u(w, otype='clause')
            phraseNode = bhs.L.u(w, otype='phrase')
            firstClauseWordNode = bhs.L.d(clauseNode[0], otype='word')[0]
            firstPhraseWordNode = bhs.L.d(phraseNode[0], otype='word')[0]
            lastClauseWordNode = bhs.L.d(clauseNode[0], otype='word')[-1]
            lastPhraseWordNode = bhs.L.d(phraseNode[0], otype='word')[-1]

            if w == firstClauseWordNode:
                verse += '<span class=clauseNode id=clauseNode clause_node='+str(clauseNode[0])+'>'
                verse += "<span class='syntax clause1 hidden' id=syntax>C:"+ translate.eng_to_kor(bhs.F.typ.v(clauseNode[0]), 'abbr') +"</span>"

            if w == firstPhraseWordNode:
                verse += '<span class=phraseNode id=phraseNode phrase_node='+str(phraseNode[0])+'>'
                verse += "<span class='syntax phrase1 hidden' id=syntax>P:"+ translate.eng_to_kor(bhs.F.typ.v(phraseNode[0]), 'abbr') + "," + translate.eng_to_kor(bhs.F.function.v(phraseNode[0]), 'abbr') + "</span>"

            # 크티브 크리일 경우 크티브는 링크 없이 출력. 크리만 링크 출력.
            if bhs.F.qere_utf8.v(w):
                verse += '<span class=wordNode>'
                verse += bhs.F.g_word_utf8.v(w) + ' '
                verse += '</span>'

                verse += "<span class=wordNode @click='hebwordinfo(" + str(w) + ")'>"
                verse += bhs.F.qere_utf8.v(w)
                verse += '</span>'

                if bhs.F.qere_trailer_utf8.v(w):
                    verse += '<span class=trailerNode>'
                    verse += bhs.F.qere_trailer_utf8.v(w)
                    verse += '</span>'

            else:
                verse += "<span class=wordNode @click='hebwordinfo(" + str(w) + ")'>"
                verse += bhs.F.g_word_utf8.v(w)
                verse += '</span>'

                if bhs.F.trailer_utf8.v(w):
                    verse += '<span class=trailerNode>'
                    verse += bhs.F.trailer_utf8.v(w)
                    verse += '</span>'

            if w == lastClauseWordNode: verse += '</span>'
            if w == lastPhraseWordNode: verse += '</span>'

        verse += "<i class='fas fa-info-circle fa-sm' @click='hebverseinfo(" + str(v) + ")'></i>"
        verse += '</li>'
    verse += '</ol></div>'
    return verse

# 단어 정보 불러오기
def word_function(node):
    w_f = []
    w_f.append("원형: " + bhs.F.voc_utf8.v(bhs.L.u(node, otype='lex')[0]))
    w_f.append("음역: " + bhs.F.phono.v(node))
    w_f.append("품사: " + translate.eng_to_kor(bhs.F.pdp.v(node), 'full'))
    w_f.append("시제: " + translate.eng_to_kor(bhs.F.vt.v(node), 'full'))
    w_f.append("동사형: " + translate.eng_to_kor(bhs.F.vs.v(node), 'full'))
    w_f.append("인칭: " + translate.eng_to_kor(bhs.F.ps.v(node), 'full'))
    w_f.append("성: " + translate.eng_to_kor(bhs.F.gn.v(node), 'full'))
    w_f.append("수: " + translate.eng_to_kor(bhs.F.nu.v(node), 'full'))
    w_f.append("어형: " + translate.eng_to_kor(bhs.F.st.v(node), 'full'))

    if bhs.F.g_prs_utf8.v(node) == '': 
        value1 = 'NA'
    else:
        value1 = bhs.F.g_prs_utf8.v(node)
    if bhs.F.g_uvf_utf8.v(node) == '': 
        value2 = 'NA'
    else:
        value2 = bhs.F.g_uvf_utf8.v(node)
    
    w_f.append("인칭접미어: " + value1)
    w_f.append("부가접미어: " + value2)

    if bhs.F.prs_ps.v(node) == 'unknown':
        value3 = 'NA'
    else:
        value3 = translate.eng_to_kor(bhs.F.prs_ps.v(node), 'full')
    if bhs.F.prs_gn.v(node) == 'unknown':
        value4 = 'NA'
    else:
        value4 = translate.eng_to_kor(bhs.F.prs_gn.v(node), 'full')
    if bhs.F.prs_nu.v(node) == 'unknown':
        value5 = 'NA'
    else:
        value5 = translate.eng_to_kor(bhs.F.prs_nu.v(node), 'full')

    w_f.append("인칭(접미): " + value3)
    w_f.append("성(접미): " + value4)
    w_f.append("수(접미): " + value5)

    # if bhs.F.gloss.v(bhs.L.u(node, otype='lex')[0]) == '<object marker>':
    #     value6 = 'object marker'
    # else:
    #     value6 = bhs.F.gloss.v(bhs.L.u(node, otype='lex')[0])

    # w_f.append("의미: " + value6)

    return w_f

# 절 정보 불러오기
def verse_function(node):
    wordsNode = bhs.L.d(node, otype='word')
    # v_f = {'words': [], 'gloss': [], 'pdp': [], 'parse': [], 'suff': []}
    v_f = {'words': [], 'pdp': [], 'parse': [], 'suff': []}
    for w in wordsNode:
        v_f['words'].append(bhs.F.g_word_utf8.v(w))

        # if bhs.F.gloss.v(bhs.L.u(w, otype='lex')[0]) == "<object marker>":
        #     gloss = "object marker"
        # else: 
        #     gloss = bhs.F.gloss.v(bhs.L.u(w, otype='lex')[0])
        # v_f['gloss'].append(gloss)

        pdp = translate.eng_to_kor(bhs.F.pdp.v(w), 'full')
        if pdp == '동사':
            pdp_str = pdp + "(" + translate.eng_to_kor(bhs.F.vs.v(w), 'abbr') + ")"
            v_f['pdp'].append(pdp_str)
            parse_str = translate.eng_to_kor(bhs.F.vt.v(w), 'abbr') + "." + translate.eng_to_kor(bhs.F.ps.v(w), 'abbr') + translate.eng_to_kor(bhs.F.gn.v(w), 'abbr') + translate.eng_to_kor(bhs.F.nu.v(w), 'abbr')
            v_f['parse'].append(parse_str)
        elif pdp == '명사':
            v_f['pdp'].append(pdp)
            parse_str = translate.eng_to_kor(bhs.F.gn.v(w), 'abbr') + translate.eng_to_kor(bhs.F.nu.v(w), 'abbr')
            v_f['parse'].append(parse_str)
        else:
            v_f['pdp'].append(pdp)
            v_f['parse'].append('')
        if bhs.F.g_prs_utf8.v(w) != "":
            suff_str = "접미." + translate.eng_to_kor(bhs.F.prs_ps.v(w), 'abbr') + translate.eng_to_kor(bhs.F.prs_gn.v(w), 'abbr') + translate.eng_to_kor(bhs.F.prs_nu.v(w), 'abbr')
            v_f['suff'].append(suff_str)
        else:
            v_f['suff'].append('')
    
    section = bhs.T.sectionFromNode(wordsNode[0])
    v_f['book'] = section[0]
    v_f['chp'] = section[1]
    v_f['vrs'] = section[2]

    return v_f
    
    # eng_chp_vrs = translate.heb_vrs_to_eng(section[0], str(section[1]), str(section[2]))
    # verse_str = {"kjv": [], "kor": []}
    # for c_v in eng_chp_vrs:
    #     chp_vrs = re.split(":", c_v)
    #     verse_str['kjv'].append(translate.json_to_verse(section[0], chp_vrs[0], chp_vrs[1], 'kjv'))
    #     verse_str['kor'].append(translate.json_to_verse(section[0], chp_vrs[0], chp_vrs[1], 'korean'))

    # return render_template('v_f.html', v_f=v_f, section=section, verse_str=verse_str)



