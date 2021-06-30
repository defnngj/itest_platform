import request from '@/HttpCommon.js'

class TeamApi {
  getTeams() {
    return request.get('/api/v1/calendar/team/list')
  }

}

export default new TeamApi()
