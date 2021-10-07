import request from '@/HttpCommon.js'

class ProjectApi {
  getProjects(data) {
    return request.get('/interface/v1/project/', data)
  }

  getProject(pid) {
    return request.get('/interface/v1/project/detail', { id: pid })
  }

  deleteProject(pid) {
    return request.post('/interface/v1/project/delete', { id: pid })
  }

  createProject(data) {
    return request.post('/interface/v1/project/create', data)
  }

  updateProject(data) {
    return request.post('/interface/v1/project/update', data)
  }

}

export default new ProjectApi()
