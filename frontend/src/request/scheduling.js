import request from '@/HttpCommon.js'

class CalendarApi {
  getTasks(data) {
    return request.get('/api/v1/calendar/schedule/list', data)
  }

  getTaskInfo(taskId) {
    return request.get('/api/v1/calendar/schedule/detail', { id: taskId })
  }

  createTask(data) {
    return request.post('/api/v1/calendar/schedule/create', data)
  }

  updateTask(data) {
    return request.post('/api/v1/calendar/schedule/update', data)
  }

  deleteTask(taskId) {
    return request.post('/api/v1/calendar/schedule/delete', { id: taskId })
  }
}

export default new CalendarApi()
