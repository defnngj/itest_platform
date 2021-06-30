import request from '@/HttpCommon.js'

class FileApi {
  // 获取文件列表
  getFiles(data) {
    return request.get('/api/v1/file/list', data)
  }

  // 获取文件详情
  getFile(str) {
    return request.get('/api/v1/file/detail', { name: str })
  }

  // 下载文件
  downloadFile(str) {
    return request.get('/api/v1/file/download', { name: str }, 'blob')
  }

  // 删除文件
  deleteFile(str) {
    return request.post('/api/v1/file/delete', { name: str })
  }

}

export default new FileApi()
