import Api from '@/services/Api'

export default {
    getText(ver, book, chp, bib) {
        var url = 'api/text/' + ver + '/' + bib + '/' + book + '/' + chp + '/' 
        return Api().get(url)
    },
    getBhsText(book, chp) {
        var url = 'api/text/bhs/' + book + '/' + chp + '/' 
        return Api().get(url)
    },
    getGntText(book, chp) {
        var url = 'api/text/gnt/' + book + '/' + chp + '/'
        return Api().get(url)
    }
}