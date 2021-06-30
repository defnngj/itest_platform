<!--
/**
* @module components
* @author huzhiheng
* @date 2021年3月31日
* @desc 监控服务组件
*/
-->
<template>
  <div>
    <div style="float: left" v-loading="loading">
      <p>监控服务列表</p>
      <el-tree :data="seviceTree" :props="defaultProps" @node-click="handleNodeClick"></el-tree>
    </div>
    <div class="charts-style">
      <div class="heartbeat-style">
        <el-select v-model="heartbeat" size="small" @change="hbChange" placeholder="选择心跳时间" style="width: 120px;" :disabled="isEdit">
          <el-option v-for="item in timeOptions" :key="item.value" :label="item.label" :value="item.value">
            <span style="float: left">{{ item.label }}</span>
            <span style="float: right; color: #727cf5;"><i class="el-icon-refresh"></i></span>
          </el-option>
        </el-select>
      </div>
      <el-card shadow="hover">
        <div v-if="defaultInfo === true">
          <span>请点击服务</span>
        </div>
        <div id="cpu" style="height: 300px" />
      </el-card>
    </div>
    <div class="charts-style">
      <el-card shadow="hover">
        <div v-if="defaultInfo === true">
          <span>请点击服务</span>
        </div>
        <div id="memory" style="height: 300px" />
      </el-card>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import ReportApi from '../../../request/report'

export default {
  name: 'ErrorsCharts',
  props: ['reportId'],
  data() {
    return {
      loading: false,
      chart: '',
      seviceTree: [],
      defaultInfo: true,
      isEdit: true,
      defaultProps: {
        children: 'children',
        label: 'label'
      },
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
      query: {
        id: 2,
        service_name: 'klook-apiconn/jrpassserv',
        child_name: 'klook-prod-inf-1'
      },
      chartOption: {
        color: [],
        title: {
          text: ''
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: []
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        toolbox: {
          feature: {
            // saveAsImage: {}
          }
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: []
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name: 'Errors',
            type: 'line',
            stack: '总量',
            data: []
          }
        ]
      }
    }
  },
  mounted() {
    this.initServiceList()
  },

  destroyed() {
    // 离开页面，关闭心跳
    clearInterval(this.runInterval)
  },

  methods: {
    // 获得监控分组列表
    async initServiceList() {
      this.loading = true
      const resp = await ReportApi.getMonitors(this.reportId)
      if (resp.success === true) {
        this.seviceTree = resp.result
      } else {
        this.$message.error(resp.error.message)
      }
      this.loading = false
    },

    // 初始化CPU
    initCPU(option) {
      const cpuElem = document.getElementById('cpu')
      if (cpuElem !== null) {
        echarts.dispose(cpuElem)
      }
      this.chart = echarts.init(cpuElem)
      option.color = [
        '#ff679b',
        '#fa5c7c',
        '#fd7e14',
        '#ffbc00',
        '#02a8b5',
        '#39afd1',
        '#2c8ef8',
        '#727cf5',
        '#6b5eae',
        '#0acf97'
      ]
      option.title.text = 'CPU/时间'
      option.legend = {
        orient: 'vertical',
        left: 'right',
        align: 'left',
        padding: [0, 25]
      }
      this.chart.setOption(option)
    },

    // 初始化MEMORY
    initMemory(option) {
      const memoryElem = document.getElementById('memory')
      if (memoryElem !== null) {
        echarts.dispose(memoryElem)
      }
      this.chart = echarts.init(memoryElem)
      option.color = [
        '#ff679b',
        '#fa5c7c',
        '#fd7e14',
        '#ffbc00',
        '#02a8b5',
        '#39afd1',
        '#2c8ef8',
        '#727cf5',
        '#6b5eae',
        '#0acf97'
      ]
      option.title.text = 'Memory/时间'
      option.legend = {
        orient: 'vertical',
        left: 'right',
        align: 'left',
        padding: [0, 25]
      }
      this.chart.setOption(option)
    },

    // 获取服务数据
    async getChartsData() {
      const resp = await ReportApi.getServiceInfo(this.query)
      if (resp.success === true) {
        // 填充cpu数据
        const cpus = resp.result.cpu
        this.chartOption.xAxis.data = resp.result.time
        this.chartOption.legend.data = []
        this.chartOption.series = []
        for (let i = 0; i < cpus.length; i++) {
          this.chartOption.legend.data.push(cpus[i].name)
          this.chartOption.series.push({
            name: cpus[i].name,
            type: 'line',
            areaStyle: {},
            stack: '总量',
            data: cpus[i].data
          })
        }
        this.initCPU(this.chartOption)
        // 填充memory数据
        const memerys = resp.result.memory
        this.chartOption.legend.data = []
        this.chartOption.series = []
        for (let i = 0; i < memerys.length; i++) {
          this.chartOption.legend.data.push(memerys[i].name)
          this.chartOption.series.push({
            name: memerys[i].name,
            type: 'line',
            areaStyle: {},
            stack: '总量',
            data: memerys[i].data
          })
        }
        this.initMemory(this.chartOption)
      } else {
        this.$message.error(resp.error.message)
      }
    },

    // 开启心跳
    startHeartbeat() {
      this.getChartsData()
      if (this.runInterval !== undefined) {
        clearInterval(this.runInterval)
      }
      this.runInterval = setInterval(this.getChartsData, this.heartbeat)
    },

    // 点击监控节点
    async handleNodeClick(data) {
      this.isEdit = false
      this.defaultInfo = false
      this.query.id = this.reportId
      this.query.service_name = data.service_mame
      this.query.child_name = data.label
      this.startHeartbeat()
    },

    hbChange() {
      if (this.runInterval !== undefined) {
        clearInterval(this.runInterval)
      }
      this.runInterval = setInterval(this.getChartsData, this.heartbeat)
    }
  }
}
</script>

<style scoped>
.charts-style {
  margin-top: 10px;
  margin-bottom: 10px;
  width: 68%;
  float: right;
}

.heartbeat-style {
  text-align: right;
  height: 50px;
}
</style>
