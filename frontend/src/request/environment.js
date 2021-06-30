import request from '@/HttpCommon.js'

class EnvApi {
  getEnvs(data) {
    return request.get('/api/v1/env/task/list', data)
  }

  createEnv(data) {
    return request.post('/api/v1/env/task/create', data)
  }

  updateEnv(data) {
    return request.post('/api/v1/env/task/update', data)
  }

  deleteEnv(eid) {
    return request.post('/api/v1/env/task/delete', { id: eid })
  }

  getEnv(eid) {
    return request.get('/api/v1/env/task/detail', { id: eid })
  }

  runEvn(tid) {
    return request.post('/api/v1/env/task/run', { task_id: tid })
  }

  envSamples(eid) {
    return request.get('/api/v1/env/search', { env_id: eid })
  }

  getServers(data) {
    return request.get('/api/v1/env/create/server_list', data)
  }

}

export default new EnvApi()
