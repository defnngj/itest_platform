import request from '@/HttpCommon.js'

class FlowlogApi {
  getFlowlogs(data) {
    return request.get('/api/v1/flowlog/list', data)
  }

  createFlowlog(data) {
    return request.post('/api/v1/flowlog/create', data)
  }

  updateFlowlog(data) {
    return request.post('/api/v1/flowlog/update', data)
  }

  deleteFlowlog(tid) {
    return request.post('/api/v1/flowlog/delete', { id: tid })
  }

  getFlowlog(fid) {
    return request.get('/api/v1/flowlog/detail', { id: fid })
  }

  createLog(fid) {
    return request.post('/api/v1/flowlog/run', { id: fid })
  }

  getLog(fid) {
    return request.get('/api/v1/flowlog/result', { id: fid })
  }

  createCase(data) {
    return request.post('/api/v1/flowlog/case/create', data)
  }

  // 查看日志缓存
  getLogCache(data) {
    return request.post('/api/v1/flowlog/result/cache', data)
  }

  // 获取接口列表
  getUrllist(data) {
    return request.get('/api/v1/loki/url/list', data)
  }
}

export default new FlowlogApi()
