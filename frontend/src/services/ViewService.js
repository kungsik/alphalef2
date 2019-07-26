import Api from '@/services/Api'

export default {
    hebwordinfo(node) {
        var url = 'api/word/heb/' + node + '/'
        return Api().get(url)
    },
    hebverseInfo(node) {
        var url = 'api/verse/heb/' + node + '/'
        return Api().get(url)
    },
    gntwordinfo(node) {
        var url = 'api/word/gnt/' + node + '/'
        return Api().get(url)
    }
}