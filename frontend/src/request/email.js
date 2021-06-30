import request from '@/HttpCommon.js'

class EmailApi {
  getEmails(data) {
    return request.get('/api/v1/email/list', data)
  }

  getEmail(eid) {
    return request.get('/api/v1/email/detail', { id: eid })
  }

  createEmail(data) {
    return request.post('/api/v1/email/create', data)
  }

  updateEmail(data) {
    return request.post('/api/v1/email/update', data)
  }

  deleteEmail(eid) {
    return request.post('/api/v1/email/delete', { id: eid })
  }

  searchEmail(data) {
    return request.get('/api/v1/email/search', data)
  }

}

export default new EmailApi()
