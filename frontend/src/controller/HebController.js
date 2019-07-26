// HebController.js
// 히브리어 텍스트 관련 컨트롤러 
// 구문 단위 가리기(display: none)를 적용하게 되면 브라우저가 다운됨. 

import ViewService from '@/services/ViewService'

export default {
    async viewHebWordInfo(node, self) {
        try {
            var result = await ViewService.hebwordinfo(node)
            var arr = result.data.hebwordinfo
            var htmldata = '<br><h4>단어분석</h4><br>'
            htmldata += '<div class=viewhebinfo><table class=table>'
            for(var i=0; i<arr.length; i++) {
                if(arr[i].indexOf('NA')==-1) {
                    htmldata += "<tr><td>" + arr[i]+ "</td></tr>" 
                }                
            }
            htmldata += '</table></div>'
            self.$parent.dataResult = htmldata            

        } catch(error) {
            self.$parent.dataResult = '오류가 발생했습니다. 다시 시도해 주세요'
        }
    },
    async viewHebVerseInfo(node, self) {
        try {
            var result = await ViewService.hebverseInfo(node)
            var arr = result.data.hebverseinfo
            
            var htmldata = '<br><h4>절분석 (' + arr.book + ' ' + arr.chp + ':' + arr.vrs +')</h4><br>'

            htmldata += '<div class=viewhebinfo><table class=table>'
            // htmldata += '<thead><tr><td>단어</td><td>의미</td><td>품사</td><td>성,수,인칭</td><td>인칭접미</td></tr></th>'
            htmldata += '<thead><tr><td>단어</td><td>품사</td><td>성,수,인칭</td><td>인칭접미</td></tr></th>'
            htmldata += '<tbody>'

            for(var i=0; i<arr.words.length; i++) {
                // htmldata += '<tr><td>' + arr.words[i] + '</td><td>' + arr.gloss[i] + '</td><td>' + arr.pdp[i] + '</td><td>' + arr.parse[i] + '</td><td>' + arr.suff[i] + '</td></tr>'
                htmldata += '<tr><td>' + arr.words[i] + '</td><td>' + arr.pdp[i] + '</td><td>' + arr.parse[i] + '</td><td>' + arr.suff[i] + '</td></tr>'
            }

            htmldata += '</tbody></table></div>'
            self.$parent.dataResult = htmldata            

        } catch(error) {
            self.$parent.dataResult = '오류가 발생했습니다. 다시 시도해 주세요'
        }
    }
}