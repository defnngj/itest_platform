<!--
/**
* @module components
* @author huzhiheng
* @date 2021年1月27日
* @desc 报告详情组件
*/
-->
<template>
  <div class="report-details">
    <el-card class="main-card" v-loading="loading">
      <div style="overflow:auto; margin-bottom: 50px;">
        <el-button type="primary" size="small" class="report-button" @click="stopRunning" :disabled="stopRun">停止运行</el-button>
        <div class="span-left" style="width: 50%">
          <el-table :data="baseTable" :show-header="false">
            <el-table-column prop="title" label="标题" width="90"> </el-table-column>
            <el-table-column prop="data" label="数据" width="200"> </el-table-column>
            <el-table-column prop="jmeter" label="JMeter标题" width="180"> </el-table-column>
            <el-table-column prop="number" label="数字"> </el-table-column>
          </el-table>
        </div>
      </div>
      <el-tabs v-model="activeName" @tab-click="switchTabs" style="margin-bottom: 50px">
        <el-tab-pane label="JMeter信息" name="first">
          <div class="main-card">
            <el-divider content-position="left">聚合报告</el-divider>
            <el-table :data="aggregateTable" border style="width: 100%" :header-cell-style="{background:'#F1F3FA'}">
              <el-table-column prop="label" label="Label"> </el-table-column>
              <el-table-column prop="samples" label="Sample"> </el-table-column>
              <el-table-column prop="average" label="Average"> </el-table-column>
              <el-table-column prop="tp90" label="90% Line"> </el-table-column>
              <el-table-column prop="tp95" label="95% Line"> </el-table-column>
              <el-table-column prop="tp99" label="99% Line"> </el-table-column>
              <el-table-column prop="min" label="Min"> </el-table-column>
              <el-table-column prop="max" label="Max"> </el-table-column>
              <el-table-column prop="ko" label="Errors"> </el-table-column>
              <el-table-column prop="error" label="Errors(%)"> </el-table-column>
              <el-table-column prop="transactions" label="TPS"> </el-table-column>
              <el-table-column prop="sent" label="Sent KB/s"> </el-table-column>
            </el-table>
            <br>
            <el-divider content-position="left">JMeter监控</el-divider>
            <JMeterChart v-if="jmeterTab === true" :reportId="reportId"></JMeterChart>
          </div>
        </el-tab-pane>
        <el-tab-pane label="监控服务" name="second">
          <div class="main-card">
            <SeverChart v-show="monitorTab === true" :reportId="reportId"></SeverChart>
          </div>
        </el-tab-pane>
        <el-tab-pane label="日志详情" name="third">
          <div class="main-card">
            <div class="charts-line">
              <div class="log-content">
                <div v-for="(item, i) in reportLogs" :key="i" class="text item">
                  {{ item }}
                </div>
              </div>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script>
import ReportApi from '../../request/report'
import JMeterChart from './Charts/JMeterChart'
import SeverChart from './Charts/SeverChart.vue'

export default {
  name: 'report-details',
  components: { JMeterChart, SeverChart },
  props: ['reportId'],
  data() {
    return {
      activeName: 'first',
      jmeterTab: true,
      monitorTab: false,
      loading: false,
      stopRun: false,
      runInterval: '',
      baseTable: [
        {
          title: '名称:',
          data: '',
          jmeter: '施压实例数:',
          number: ''
        },
        {
          title: '状态:',
          data: '',
          jmeter: '目标并发:',
          number: ''
        },
        {
          title: '执行人:',
          data: '',
          jmeter: '爬坡时间(s):',
          number: ''
        },
        {
          title: '开始时间:',
          data: '',
          jmeter: '爬坡次数:',
          number: ''
        },
        {
          title: '结束时间:',
          data: '',
          jmeter: '持续时间(s):',
          number: ''
        }
      ],
      aggregateTable: [],
      instanceTable: [],
      reportLogs: []
    }
  },

  mounted() {
    this.initReportAggregate()
    this.initReportDetails()
    // 进入页面，开启心跳
    this.runInterval1 = setInterval(this.initReportDetails, 10000)
    this.runInterval2 = setInterval(this.initReportAggregate, 10000)
  },

  destroyed() {
    // 离开页面，关闭心跳
    clearInterval(this.runInterval1)
    clearInterval(this.runInterval2)
  },

  methods: {
    // 切换标签
    switchTabs(tab) {
      if (tab.index === '0') {
        // JMeter信息 标签页
        this.jmeterTab = true
        this.monitorTab = false
      } else if (tab.index === '1') {
        // 监控服务 标签页
        this.monitorTab = true
        this.jmeterTab = false
      } else if (tab.index === '2') {
        // 日志详情 标签页
        this.initReportLog()
        this.monitorTab = false
        this.jmeterTab = false
      }
    },

    // 初始化报告详情
    async initReportDetails() {
      const resp = await ReportApi.getReportInfo(this.reportId)
      if (resp.success === true) {
        const ret = resp.result
        this.baseTable[0].data = ret.name
        this.baseTable[1].data = ret.status
        this.baseTable[2].data = ret.user_name
        this.baseTable[3].data = ret.start_time
        this.baseTable[4].data = ret.end_time
        this.baseTable[0].number = ret.slave_count
        this.baseTable[1].number = ret.thread_group.target_concurrency
        this.baseTable[2].number = ret.thread_group.ramp_up_time
        this.baseTable[3].number = ret.thread_group.ramp_up_steps_count
        this.baseTable[4].number = ret.thread_group.hold_target_rate_time
        if (ret.status !== 'Running') {
          this.stopRun = true
          clearInterval(this.runInterval)
        }
      } else {
        this.$message.error(resp.error.message)
      }
    },

    // 初始化聚合报告
    async initReportAggregate() {
      const resp = await ReportApi.getReportAggregate(this.reportId)
      if (resp.success === true) {
        this.aggregateTable = []
        this.aggregateTable.push(resp.result)
      } else {
        this.$message.error(resp.error.message)
      }
    },

    // 初始化报告实例度量细节
    async initReportInstance() {
      const resp = await ReportApi.regReportInstance(this.reportId)
      if (resp.success === true) {
        this.instanceTable = []
        this.instanceTable = resp.result
      } else {
        this.$message.error(resp.error.message)
      }
    },

    // 初始化日志报告
    async initReportLog() {
      const resp = await ReportApi.getReportLog(this.reportId)
      if (resp.success === true) {
        const data = resp.result
        this.reportLogs = []
        for (const i in data) {
          this.reportLogs.push(data[i])
        }
      } else {
        this.$message.error(resp.error.message)
      }
    },

    // 停止运行报告
    async stopRunning() {
      this.loading = true
      const resp = await ReportApi.stopReport(this.reportId)
      if (resp.success === true) {
        this.$message({
          message: '已停止运行！',
          type: 'success'
        })
      } else {
        this.$message.error(resp.error.message)
      }
      this.loading = false
    }
  }
}
</script>

<style>
.charts-line {
  margin-top: 30px;
  height: auto;
  overflow: auto;
}

.report-button {
  float: right;
  margin-left: 10px !important;
}

.log-content {
  text-align: left;
  max-height: 500px;
  overflow: auto;
  background-color: #f1f3fa;
  box-shadow: 1px 1px 5px 3px #eef2f7;
  white-space: pre-line;
}
</style>
