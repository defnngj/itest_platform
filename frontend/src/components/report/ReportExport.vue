<!--
/**
* @module components
* @author huzhiheng
* @date 2021年3月24日
* @desc 下载测试报告组件
*/
-->
<template>
  <div class="report-export">
    <br>
    <el-card class="main-card">
      <div style="overflow:auto; margin-bottom: 50px;">
        <el-button type="info" size="small" class="report-button">
          <img src='../../assets/logo.png' class="img-logo" />
        </el-button>
        <div class="span-left" style="width: 50%">
          <el-table :data="baseTable" :show-header="false">
            <el-table-column prop="title" label="标题" width="90"> </el-table-column>
            <el-table-column prop="data" label="数据" width="200"> </el-table-column>
            <el-table-column prop="jmeter" label="JMeter标题" width="180"> </el-table-column>
            <el-table-column prop="number" label="数字"> </el-table-column>
          </el-table>
        </div>
      </div>
      <el-divider content-position="left">聚合报告</el-divider>
      <div class="charts-line">
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
      </div>
      <el-divider content-position="left">JMeter信息</el-divider>
      <JMeterChart :reportId="reportId"></JMeterChart>
    </el-card>
  </div>
</template>

<script>
import ReportApi from '../../request/report'
import JMeterChart from './Charts/JMeterChart'

export default {
  name: 'report-export',
  components: { JMeterChart },
  props: ['reportId'],
  data() {
    return {
      activeName: 'first',
      loading: false,
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
    this.initReportDetails()
    this.initReportAggregate()
  },

  methods: {
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
