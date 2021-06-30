import request from '@/HttpCommon.js'

class CaseApi {
  getCases(data) {
    return request.get('/api/v1/loadtest/list', data)
  }

  getCase(cid) {
    return request.get('/api/v1/loadtest/detail', { id: cid })
  }

  createCase(data) {
    return request.post('/api/v1/loadtest/create', data)
  }

  updateCase(data) {
    return request.post('/api/v1/loadtest/update', data)
  }

  deleteCase(cid) {
    return request.post('/api/v1/loadtest/delete', { id: cid })
  }

  runCase(cid) {
    return request.post('/api/v1/loadtest/run', { id: cid })
  }

  deleteFile(fid) {
    return request.post('/api/v1/loadtest/file/delete', { id: fid })
  }

  // 下载测试脚本
  downloadFile(fid) {
    return request.get('/api/v1/loadtest/download', { id: fid }, 'blob')
  }

}

export default new CaseApi()
