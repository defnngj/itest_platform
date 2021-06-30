import request from '@/HttpCommon.js'

class UserApi {
  getUsers() {
    return request.get('/api/v1/common/user/list')
  }

}

export default new UserApi()
