//TextController.js
//텍스트 컨트롤러 번역본과 원어 성서 텍스트 데이터를 처리함.

import BookData from '@/data/BookData'
import TextService from '@/services/TextService'
import HebController from '@/controller/HebController'
import GntController from '@/controller/GntController'
import TextController from '@/controller/TextController'


export default {
    // 텍스트 업데이트. opt가 1이면 장을 1절로 변경함. 0이면 장을 고정.
  async updateText(self, opt) {
    self.verse = ''
    try {
      var result = {}
      if(opt==1) { self.chpselected = 1 }
      if(self.verselected != 'bhs' && self.verselected != 'gnt') {

        if(BookData.old_booklist.map(x => x.value).indexOf(self.bookselected)==-1) {
          var bib = "new"
        }
        else {
          bib = "old"
        }

        result = await TextService.getText(self.verselected, self.bookselected, self.chpselected, bib)
        self.verse = result.data.verse
      }
      //bhs일 경우 vue 컴포넌트로 임베딩 시켜야 메소드가 작동함. 
      else if(self.verselected == 'bhs') {
        result = await TextService.getBhsText(self.bookselected, self.chpselected)
        // self.verse = result.data.verse
        self.verse = {
          // 메인 vue에 child로 임베딩. 나중에 최적화가 필요할 듯.
          template: result.data.verse,
          methods: {
            hebwordinfo(node) {
              HebController.viewHebWordInfo(node, this)
            },
            hebverseinfo(node) {
              HebController.viewHebVerseInfo(node, this)
            },
            hebsyntax() {
              TextController.viewSyntax(this)
            }
          }
        }
      }
      //gnt일 경우
      else if(self.verselected == 'gnt') {
        result = await TextService.getGntText(self.bookselected, self.chpselected)
        self.verse = {
          // 메인 vue에 child로 임베딩. 나중에 최적화가 필요할 듯.
          template: result.data.verse,
          methods: {
            gntwordinfo(node) {
              GntController.viewGntWordInfo(node, this)
            },
            // hebverseinfo(node) {
            //   HebController.viewHebVerseInfo(node, this)
            // },
            gntsyntax() {
              TextController.viewSyntax(this)
            }
          }
        }
      }
      var selectedchplist = []
      var totalchpnum = BookData.chpnum[self.bookselected]+1 

      // bhs외의 번역본은 요엘서와 말라기서 전체 장수가 다른 관계로 보정해 줌. 
      if(self.verselected != 'bhs' && self.bookselected == 'Joel') {
        totalchpnum = totalchpnum - 1
      }
      if(self.verselected != 'bhs' && self.bookselected == 'Malachi') {
        totalchpnum = totalchpnum + 1
      }

      for(var i=1; i < totalchpnum; i++) {
        selectedchplist[i] = {'value': i, 'text': i}
      }
      self.chplist = selectedchplist
    } catch (error) {
      self.verse = '데이터 로드 중 오류가 발생했습니다.'
    }
  },
  viewSyntax(self) {
    let btn = self.$refs['syntax']
    let hebverse = self.$refs['verse']

    if(btn.id=='syntax_enact') {
      btn.innerHTML = '구문단위가리기'
      btn.id = 'syntax_disable'

      let clauseclass = hebverse.getElementsByClassName('clauseNode')
      while(clauseclass.length) {
          clauseclass[0].className = 'clause'
      }
      let phraseclass = hebverse.getElementsByClassName('phraseNode')
      while(phraseclass.length) {
          phraseclass[0].className = 'phrase'
      }
      let clausesyntaxclass = hebverse.getElementsByClassName('syntax clause1 hidden')
      while(clausesyntaxclass.length) {
          clausesyntaxclass[0].className = 'syntax clause1'
      }
      let phrasesyntaxclass = hebverse.getElementsByClassName('syntax phrase1 hidden')
      while(phrasesyntaxclass.length) {
          phrasesyntaxclass[0].className = 'syntax phrase1'
      }
    }
    else if(btn.id=='syntax_disable') {
      btn.innerHTML = '구문단위표시'
      btn.id = 'syntax_enact'
      
      // 임베드 컴포넌트이기 때문에 상위 부모 객체를 인자로 전달
      TextController.updateText(self.$parent, 0)
    }
  }
}