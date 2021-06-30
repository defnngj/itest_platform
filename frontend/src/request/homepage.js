import request from '@/HttpCommon.js'

class HomeApi {
  getCalendar() {
    return request.get('/api/v1/homepage/calendar')
  }

  getTasks(data) {
    return request.get('/api/v1/homepage/schedule', data)
  }

  getCases(data) {
    return request.get('/api/v1/homepage/loadtest/list', data)
  }

  getReports(data) {
    return request.get('/api/v1/homepage/reports/list', data)
  }
}

export default new HomeApi()
