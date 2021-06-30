<!--
/**
* @module components
* @author huzhiheng
* @date 2021年4月1日
* @desc JMeter监控图标组件
*/
-->
<template>
  <div>
    <div class="heartbeat-style">
      <el-select v-model="heartbeat" size="small" @change="hbChange" placeholder="选择心跳时间" style="width: 120px;" :disabled="isEdit">
        <el-option v-for="item in timeOptions" :key="item.value" :label="item.label" :value="item.value">
          <span style="float: left">{{ item.label }}</span>
          <span style="float: right; color: #727cf5;"><i class="el-icon-refresh"></i></span>
        </el-option>
      </el-select>
    </div>
    <div class="jmeter-echarts">
      <div class="charts-line">
        <div class="left-charts">
          <el-card shadow="hover">
            <div id="tps" style="height: 300px" />
          </el-card>
        </div>
        <div class="right-charts">
          <el-card shadow="hover">
            <div id="resp_time" style="height: 300px" />
          </el-card>
        </div>
      </div>
      <div class="charts-line">
        <div class="left-charts">
          <el-card shadow="hover">
            <div id="thread" style="height: 300px" />
          </el-card>
        </div>
        <div class="right-charts">
          <el-card shadow="hover">
            <div id="errors" style="height: 300px" />
          </el-card>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import ReportApi from '../../../request/report'

export default {
  name: 'jmeter-echarts',
  props: ['reportId'],
  data() {
    return {
      chart: '',
      timeOptions: [
        {
          value: '5000',
          label: '5秒'
        },
        {
          value: '10000',
          label: '10秒'
        },
        {
          value: '20000',
          label: '20秒'
        },
        {
          value: '30000',
          label: '30秒'
        },
        {
          value: '60000',
          label: '1分钟'
        },
        {
          value: '300000',
          label: '5分钟'
        }
      ],
      heartbeat: '20000',
      isEdit: false,
      tpsOption: {
        color: [], // 颜色
        title: {
          text: '' // 标题
        },
        tooltip: {
          show: true,
          trigger: 'axis',
          confine: true
        },
        legend: {
          data: [], // 名称
          left: 'right',
          padding: [0, 25]
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        toolbox: {
          feature: {
            // saveAsImage: {}  // 下载icon
          }
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: [] // X(时间)轴数据
        },
        yAxis: {
          type: 'value'
        },
        series: [] // 数组
      },
      resOption: {
        color: [], // 颜色
        title: {
          text: '' // 标题
        },
        tooltip: {
          show: true,
          trigger: 'axis',
          confine: true
        },
        legend: {
          data: [], // 名称
          left: 'right',
          padding: [0, 25]
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        toolbox: {
          feature: {
            // saveAsImage: {}  // 下载icon
          }
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: [] // X(时间)轴数据
        },
        yAxis: {
          type: 'value'
        },
        series: [] // 数组
      },
      threadOption: {
        color: [], // 颜色
        title: {
          text: '' // 标题
        },
        tooltip: {
          show: true,
          trigger: 'axis',
          confine: true
        },
        legend: {
          data: [], // 名称
          left: 'right',
          padding: [0, 25]
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        toolbox: {
          feature: {
            // saveAsImage: {}  // 下载icon
          }
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: [] // X(时间)轴数据
        },
        yAxis: {
          type: 'value'
        },
        series: [] // 数组
      },
      errorsOption: {
        color: [], // 颜色
        title: {
          text: '' // 标题
        },
        tooltip: {
          show: true,
          trigger: 'axis',
          confine: true
        },
        legend: {
          data: [], // 名称
          left: 'right',
          padding: [0, 25]
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        toolbox: {
          feature: {
            // saveAsImage: {}  // 下载icon
          }
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: [] // X(时间)轴数据
        },
        yAxis: {
          type: 'value'
        },
        series: [] // 数组
      }
    }
  },
  mounted() {
    this.JMeterData('init')
    // 开启心跳
    this.runInterval = setInterval(this.checkStatus, this.heartbeat)
  },

  destroyed() {
    // 离开页面，关闭心跳
    clearInterval(this.runInterval)
  },

  methods: {
    /*
    * 初始化ECharts图表
    * @option: 图表选项
    * @req_type: 请求参数类型
    * @title: 图表标题
    * @data_name: 数据名称
    * @data_color: 数据颜色
    * @elem: 渲染元素对象
    */
    async initECharts(option, req_type, title, data_name, data_color, elem, data_type) {
      const resp = await ReportApi.getReportCharts({ id: this.reportId, type: req_type })
      if (resp.success === true) {
        if (data_type === 'init') {
          option.color = [data_color]
          option.title.text = title
          option.legend.data = [data_name]
          option.xAxis.data = []
          option.series = [{
            name: data_name,
            type: 'line',
            smooth: true,
            // areaStyle: {},
            stack: '总量',
            data: []
          }]
          for (const i in resp.result) {
            option.xAxis.data.push(resp.result[i].xAxis)
            option.series[0].data.push(resp.result[i].yAxis)
          }
          // 渲染页面元素
          if (elem !== null) {
            echarts.dispose(elem)
          }
          this.chart = echarts.init(elem)
          this.chart.setOption(option)
        } else {
          option.color = [data_color]
          option.title.text = title
          option.legend.data = [data_name]
          option.series[0].name = data_name
          option.series[0].type = 'line'
          option.series[0].smooth = true
          option.series[0].stack = '总量'
          for (const i in resp.result) {
            option.xAxis.data.push(resp.result[i].xAxis)
            option.series[0].data.push(resp.result[i].yAxis)
          }
          this.chart = echarts.init(elem)
          setTimeout(this.chart.setOption(option), 500)
        }
      } else {
        this.$message.error(resp.error.message)
      }
    },


    // 渲染图表
    async JMeterData(data_type) {
      this.$nextTick(() => {
      // TPS图表
        const tpsElem = document.getElementById('tps')
        this.initECharts(this.tpsOption, 'tps', 'TPS/时间', 'TPS', '#42d29d', tpsElem, data_type)
        // 响应时间图标
        const respTimeElem = document.getElementById('resp_time')
        this.initECharts(this.resOption, 'responsetime', '响应时间/时间', 'Response Time', '#44badc', respTimeElem, data_type)
        // 线程图标
        const threadElem = document.getElementById('thread')
        this.initECharts(this.threadOption, 'users', 'Thread/时间', 'Thread', '#727cf5', threadElem, data_type)
        // 错误图标
        const errorsElem = document.getElementById('errors')
        this.initECharts(this.errorsOption, 'errors', 'Errors/时间', 'Errors', '#fa5c7c', errorsElem, data_type)
      })
    },

    // 检查报告状态
    async checkStatus() {
      const resp = await ReportApi.getReportInfo(this.reportId)
      if (resp.success === true) {
        if (resp.result.status !== 'Running') {
          // 结束心跳
          this.isEdit = true
          clearInterval(this.runInterval)
        } else {
          this.JMeterData('add')
        }
      } else {
        this.$message.error(resp.error.message)
      }
    },

    hbChange() {
      if (this.runInterval !== undefined) {
        clearInterval(this.runInterval)
      }
      this.runInterval = setInterval(this.checkStatus, this.heartbeat)
    }

  }
}
</script>

<style scoped>
.charts-line {
  margin-top: 30px;
  height: auto;
  overflow: auto;
}

.left-charts {
  width: 48%;
  float: left;
}

.right-charts {
  width: 48%;
  float: right;
}
.heartbeat-style {
  text-align: right;
  height: 35px;
}
</style>
