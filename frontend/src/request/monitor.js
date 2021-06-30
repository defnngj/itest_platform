import request from '@/HttpCommon.js'

class MonitorApi {
  getMonitors(data) {
    return request.get('/api/v1/monitor/list', data)
  }

  getMonitor(mid) {
    return request.get('api/v1/monitor/group/detail', { id: mid })
  }

}

export default new MonitorApi()
