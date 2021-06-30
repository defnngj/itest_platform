import request from '@/HttpCommon.js'

class ReportApi {
  getReports(data) {
    return request.get('/api/v1/reports/list', data)
  }

  deleteReport(rid) {
    return request.post('/api/v1/reports/delete', { id: rid })
  }

  downloadReport(rid) {
    return request.get('/api/v1/reports/download', { id: rid })
  }

  getReportInfo(rid) {
    return request.get('/api/v1/reports/base/message', { id: rid })
  }

  // JMeter聚合报告
  getReportAggregate(rid) {
    return request.get('/api/v1/reports/aggregate', { id: rid })
  }

  // 报告日志
  getReportLog(rid) {
    return request.get('/api/v1/reports/log/detail', { id: rid })
  }

  // 报告实例度量
  regReportInstance(rid) {
    return request.get('/api/v1/reports/instance/detail', { id: rid })
  }

  // charts 图表数据
  getReportCharts(data) {
    return request.get('/api/v1/reports/jmeter/chart', data)
  }

  // 停止测试执行
  stopReport(rid) {
    return request.post('/api/v1/reports/stop', { id: rid })
  }

  // 下载JTL
  downloadJtl(rid) {
    return request.get('/api/v1/reports/jtl/download', { report_id: rid }, 'blob')
  }

  // 标记报告
  tagReport(data) {
    return request.post('/api/v1/reports/update/tag', data)
  }

  // 获取监控分组列表
  getMonitors(rid) {
    return request.get('/api/v1/monitor/service/list', { id: rid })
  }

  // 获取服务信息
  getServiceInfo(data) {
    return request.post('/api/v1/monitor/service/info', data)
  }

}

export default new ReportApi()
