<!--
/**
* @module components
* @author huzhiheng
* @date 2021年3月15日
* @desc 自动创建用例组件
*/
-->
<template>
  <div class="caseCreate">
    <el-card class="main-card">
      <div style="">
        <div style="text-align: left;">
          <el-steps :active="step">
            <el-step title="流量日志"></el-step>
            <el-step title="生成用例"></el-step>
            <el-step title="完成"></el-step>
          </el-steps>
        </div>
      </div>
      <!-- 流量日志 -->
      <div v-show="step === 1">
        <Flowlog v-if="step === 1" @cancel="cancelCase" @caseId="caseAccomplish"></Flowlog>
      </div>
      <!-- 生成用例 -->
      <div v-show="step == 2">
        <el-form :inline="true" ref="form" :model="form" :rules="rules" class="demo-form-inline">
          <!-- 基本信息 -->
          <el-divider content-position="left">基本信息</el-divider>
          <div>
            <span class="span-left">
              <el-form-item label="名称" prop="name" class="base-info-option">
                <el-input cy-data='case-name' v-model="form.name" placeholder="请用例名称"></el-input>
              </el-form-item>
            </span>
            <el-form-item label="团队" prop="team" class="base-info-option">
              <el-select cy-data="team" v-model="form.team" filterable placeholder="请选择团队名称">
                <el-option cy-data="team-list" v-for="item in teamOptions" :key="item.value" :label="item.label" :value="item.value">
                </el-option>
              </el-select>
            </el-form-item>
          </div>
          <div style="overflow:auto;">
            <span class="span-left">
              <el-form-item label="备注" prop="describe" class="base-info-option">
                <el-input cy-data="case-desc" v-model="form.describe" type="textarea" :rows="2" placeholder="请输入备注">
                </el-input>
              </el-form-item>
            </span>
            <el-form-item label="环境" prop="env" class="base-info-option">
              <el-select cy-data="env" v-model="form.env" filterable placeholder="请选择环境" @change="changeEnv($event)">
                <el-option cy-data="env-list" v-for="item in envOptions" :key="item.value" :label="item.label" :value="item.value">
                </el-option>
              </el-select>
              <div class="hint">
                当前环境施压实例数为: {{ this.slave_max }}
              </div>
            </el-form-item>
          </div>
          <!-- 系统配置 -->
          <el-divider content-position="left">系统配置</el-divider>
          <div style="min-height: 80px; overflow:auto;">
            <span class="span-left">
              <el-form-item label="监控分组" prop="monitor_list" class="base-info-option">
                <el-select multiple filterable v-model="form.monitor_list" placeholder="选择监控分组">
                  <el-option v-for="item in monitorOptions" :key="item.value" :label="item.label" :value="item.value">
                  </el-option>
                </el-select>
              </el-form-item>
            </span>
            <el-form-item label="邮件分组" prop="email_list" class="base-info-option">
              <el-select multiple filterable v-model="form.email_list" placeholder="选择邮箱分组">
                <el-option v-for="item in emailOptions" :key="item.value" :label="item.label" :value="item.value">
                </el-option>
              </el-select>
            </el-form-item>
          </div>
          <!-- JMeter配置 -->
          <el-divider content-position="left">JMeter配置</el-divider>
          <div>
            <span class="span-left">
              <el-form-item label="HOST" prop="host" class="base-info-option">
                <el-input cy-data="host" v-model="form.host" placeholder="输入host"></el-input>
              </el-form-item>
            </span>
            <el-form-item label="Assertion" prop="assertion" class="base-info-option">
              <el-input cy-data="assertion" v-model="form.assertion" placeholder="输入断言信息"></el-input>
            </el-form-item>
          </div>
          <!-- bzm-Concurrency Thread Group -->
          <div class="thread-group">
            <el-link class="thread-group-title" type="primary" target="_blank" href="https://jmeter-plugins.org/wiki/ConcurrencyThreadGroup/">bzm-Concurrency Thread Group <i class="el-icon-question"></i></el-link>
          </div>
          <div style="height: 320px;">
            <div class="span-left" style="width: 35%;">
              <!-- 实例数 -->
              <span class="span-left">
                <el-form-item label="施压实例数" class="thread-info-option">
                  <el-input-number cy-data="slave-count" v-model="slave_count" size="small" @change="tgChange" :min="1" :max="this.slave_max" :disabled="isEdit"></el-input-number>
                </el-form-item>
              </span>
              <!-- 并发用户数 -->
              <span class="span-left">
                <el-form-item label="目标并发" class="thread-info-option">
                  <el-input-number v-model="target_concurrency" size="small" @change="tgChange" :min="1" label="目标并发"></el-input-number>
                </el-form-item>
              </span>
              <!-- 启动时间 -->
              <span class="span-left">
                <el-form-item label="爬坡时间(sec)" class="thread-info-option">
                  <el-input-number v-model="ramp_up_time" size="small" @change="tgChange" :min="ramp_up_steps_count"></el-input-number>
                </el-form-item>
              </span>
              <!-- 启动步骤数 -->
              <span class="span-left">
                <el-form-item label="爬坡次数" class="thread-info-option">
                  <el-input-number v-model="ramp_up_steps_count" size="small" @change="tgChange" :min="1" :max="ramp_up_time"></el-input-number>
                </el-form-item>
              </span>
              <!-- 持续运行时间 -->
              <span class="span-left">
                <el-form-item label="持续时间(s)" class="thread-info-option">
                  <el-input-number v-model="hold_target_rate_time" size="small" @change="tgChange" :min="1"></el-input-number>
                </el-form-item>
              </span>
            </div>
            <div class="span-right" style="width: 55%;">
              <div id="evaluation" style="height: 300px" />
            </div>
          </div>
          <!-- 脚本上传 -->
          <el-divider content-position="left">测试脚本</el-divider>
          <div style="overflow:auto">
            <div class="span-left">
              <el-upload multiple drag list-type="text" accept=".jmx, .csv" :action="uploadURL" :on-success="uploadSuccess" :show-file-list=false>
                <i class="el-icon-upload"></i>
                <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                <div slot="tip" class="el-upload__tip">仅支持JMX/CSV文件</div>
              </el-upload>
            </div>
            <div class="span-right" style="width: 55%;">
              <el-table :data="form.file_info" style="width: 100%">
                <el-table-column prop="name" label="文件"> </el-table-column>
                <el-table-column prop="size" label="大小">
                  <template slot-scope="scope"> {{ scope.row.size }} B </template>
                </el-table-column>
                <el-table-column fixed="right" label="操作">
                  <template slot-scope="scope">
                    <el-button @click="deleteFile(scope.row)" type="danger" size="mini" icon="el-icon-delete" circle></el-button>
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </div>
          <div class="foot-button">
            <el-button cy-data="previous-step" @click="previousStep()">上一步</el-button>
            <el-button cy-data="save-case" type="primary" @click="saveCase('form')">保存</el-button>
          </div>
        </el-form>
      </div>
    </el-card>
  </div>
</template>

<script>
import CaseApi from '../../request/case'
import TeamApi from '../../request/team'
import MonitorApi from '../../request/monitor'
import EmailApi from '../../request/email'
import EnvApi from '../../request/environment'
import Flowlog from './auto/Flowlog.vue'
import * as echarts from 'echarts'

export default {
  name: 'caseCreate',
  props: [],
  components: { Flowlog },
  data() {
    return {
      uploadURL: '',
      step: 1,
      caseId: '',
      teamIds: [],
      teamOptions: [],
      envIds: [],
      envOptions: [],
      emailOptions: [],
      monitorOptions: [],
      slave_max: 1,
      slave_count: 1,
      target_concurrency: 10,
      ramp_up_time: 5,
      ramp_up_steps_count: 5,
      hold_target_rate_time: 10,
      form: {
        type: true,
        name: '',
        team: '',
        describe: '',
        env: '',
        monitor_list: [],
        email_list: [],
        host: '',
        assertion: 'success',
        slave_count: '',
        thread_group: {
          target_concurrency: '',
          ramp_up_time: '',
          ramp_up_steps_count: '',
          hold_target_rate_time: ''
        },
        file_info: [],
        branch: []
      },
      rules: {
        name: [{ required: true, message: '输入用例名称', trigger: 'blur' }],
        team: [{ required: true, message: '选择团队名称', trigger: 'blur' }],
        env: [{ required: true, message: '选择环境', trigger: 'blur' }],
        // monitor_list: [
        //   { required: true, message: '选择监控分组', trigger: 'blur' }
        // ],
        host: [{ required: true, message: '请输入host', trigger: 'blur' }]
      },
      isEdit: false,
      query: {
        current_page: 1,
        page_size: 10000,
        monitor_name: ''
      },
      option: {
        color: ['#727cf5'],
        title: {
          text: '压力评估图'
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: ['Concurrency']
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          boundaryGap: true,
          data: []
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name: 'Concurrency',
            type: 'line',
            step: 'start',
            areaStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                {
                  offset: 0,
                  color: 'rgba(58,77,233,0.8)'
                },
                {
                  offset: 1,
                  color: 'rgba(58,77,233,0.3)'
                }
              ])
            },
            data: []
          }
        ]
      }
    }
  },

  updated() {
    this.initTestEvaluation()
  },

  methods: {
    // 生成用例--> 上一步
    async previousStep() {
      this.step = 1
    },

    // 创建用例完成
    async caseAccomplish(data) {
      this.caseId = data.caseId
      this.step = 2
      this.initTeam()
      this.initEnv()
      this.initEmail()
      this.initMonitor()
      this.cleanCase()
      this.initCase()
      this.uploadURL = process.env.VUE_APP_URL + '/api/v1/loadtest/upload' // 上传URL
    },

    // 初始化用例
    async initCase() {
      const resp = await CaseApi.getCase(this.caseId)
      if (resp.success === true) {
        this.form = resp.result
        this.form.branch = []
        this.slave_count = resp.result.slave_count
        this.target_concurrency = resp.result.thread_group.target_concurrency
        this.ramp_up_time = resp.result.thread_group.ramp_up_time
        this.ramp_up_steps_count = resp.result.thread_group.ramp_up_steps_count
        this.hold_target_rate_time = resp.result.thread_group.hold_target_rate_time
        if (this.form.team === 0) { this.form.team = '' }
        if (this.form.env === 0) { this.form.env = '' }
        // if (this.teamIds.includes(this.form.team) === false) {
        //   this.form.team = ''
        // }
        if (this.envIds.includes(this.form.env) === false) {
          this.form.env = ''
        }
        this.slave_max = this.slave_count
      } else {
        this.$message.error(resp.error.message)
      }
    },

    // 初始化团队列表
    async initTeam() {
      const query = {
        current_page: 1,
        page_size: 1000
      }
      const resp = await TeamApi.getTeams(query)
      if (resp.success === true) {
        const data = resp.result.data
        for (const i in data) {
          this.teamIds.push(data[i].id)
          this.teamOptions.push({
            value: data[i].id,
            label: data[i].name
          })
        }
        if (this.teamIds.length > 0) {
          this.form.team = this.teamIds[0]
        }
      } else {
        this.$message.error(resp.error.message)
      }
    },

    // 初始化环境
    async initEnv() {
      const resp = await EnvApi.getEnvs(this.query)
      if (resp.success === true) {
        const data = resp.result.data
        for (const i in data) {
          this.envIds.push(data[i].id)
          this.envOptions.push({
            value: data[i].id,
            label: data[i].name
          })
        }
        if (this.envIds.length > 0) {
          this.form.env = this.envIds[0]
          this.changeEnv(this.form.env)
        } else {
          this.slave_max = 0
        }
      } else {
        this.$message.error(resp.error.message)
      }
    },

    // 初始化监控分组
    async initMonitor() {
      const resp = await MonitorApi.getMonitors(this.query)
      if (resp.success === true) {
        const data = resp.result.data
        for (const i in data) {
          this.monitorOptions.push({
            value: data[i].id,
            label: data[i].name
          })
        }
      } else {
        this.$message.error(resp.error.message)
      }
    },

    // 初始化邮件分组
    async initEmail() {
      const resp = await EmailApi.getEmails(this.query)
      if (resp.success === true) {
        const data = resp.result.data
        for (const i in data) {
          this.emailOptions.push({
            value: data[i].id,
            label: data[i].name
          })
        }
      } else {
        this.$message.error(resp.error.message)
      }
    },

    // 初始化压力测试评估
    initTestEvaluation() {
      const evaluationElem = document.getElementById('evaluation')
      if (evaluationElem !== null) {
        echarts.dispose(evaluationElem)
      }
      this.chart = echarts.init(evaluationElem)

      // 初始化节点数量
      const running_time = this.ramp_up_time + this.hold_target_rate_time
      this.option.xAxis.data = []
      for (let num = 1; num <= running_time; num++) {
        this.option.xAxis.data.push(num)
      }

      // 启动时间产生的节点
      const one_concurrency = (this.target_concurrency * this.slave_count) / this.ramp_up_steps_count
      const one_running_time = Math.floor(
        this.ramp_up_time / this.ramp_up_steps_count
      )
      const remainder = this.ramp_up_time % this.ramp_up_steps_count
      this.option.series[0].data = []
      let concurrencys = 0
      for (
        let i = 1;
        i <= Math.floor((this.ramp_up_time - remainder) / one_running_time);
        i++
      ) {
        concurrencys = concurrencys + one_concurrency
        for (let j = 1; j <= one_running_time; j++) {
          this.option.series[0].data.push(concurrencys)
        }
      }
      for (let k = 1; k <= remainder; k++) {
        this.option.series[0].data.push(this.target_concurrency * this.slave_count)
      }

      // 持续运行时间产生的节点
      for (let k = 1; k <= this.hold_target_rate_time; k++) {
        this.option.series[0].data.push(this.target_concurrency * this.slave_count)
      }

      // this.options.
      this.chart.setOption(this.option)
    },

    // 线程组参数修改
    tgChange() {
      this.initTestEvaluation()
    },

    // 上传附件成功
    uploadSuccess(resp, file) {
      if (resp.success === true) {
        this.imageUrl = URL.createObjectURL(file.raw)
        const attFile = resp.result[0]
        this.form.file_info.push({
          id: attFile.id,
          name: attFile.name,
          size: attFile.size
        })
      } else {
        this.$message.error(resp.error.message)
      }
    },

    // 删除上传的文件
    async deleteFile(row) {
      const resp = await CaseApi.deleteFile(row.id)
      if (resp.success === true) {
        this.$message({
          message: '删除成功！',
          type: 'success'
        })
        for (const i in this.form.file_info) {
          if (this.form.file_info[i].id === row.id) {
            this.form.file_info.splice(i, 1)
            break
          }
        }
      } else {
        this.$message.error(resp.error.message)
      }
    },

    // 保存用例
    saveCase(formName) {
      this.form.slave_count = this.slave_count
      this.form.thread_group.target_concurrency = this.target_concurrency
      this.form.thread_group.ramp_up_time = this.ramp_up_time
      this.form.thread_group.ramp_up_steps_count = this.ramp_up_steps_count
      this.form.thread_group.hold_target_rate_time = this.hold_target_rate_time
      if (this.form.monitor_list === '') { this.form.monitor_list = [] }
      if (this.form.email_list === '') { this.form.email_list = [] }
      for (const i in this.fileTable) {
        this.form.file_info.push(this.fileTable[i].id)
      }
      this.$refs[formName].validate(valid => {
        if (valid) {
          CaseApi.updateCase(this.form).then(resp => {
            if (resp.success === true) {
              this.$message({
                message: '创建完成！',
                type: 'success'
              })
              this.cancelCase()
            } else {
              this.$message.error(resp.error.message)
            }
          })
        } else {
          this.$message.error('必传字段为空!!')
          return false
        }
      })
    },

    // 关闭用例页面
    cancelCase() {
      this.$emit('cancel', {})
    },

    // 改变环境
    async changeEnv(val) {
      const resp = await EnvApi.getEnv(val)
      if (resp.success === true) {
        this.slave_max = parseInt(resp.result.jmeter_params)
      } else {
        this.$message.error(resp.error.message)
      }
    },

    // 清空表单
    cleanCase() {
      const data = {
        type: true,
        name: '',
        team: '',
        describe: '',
        env: '',
        monitor_list: [],
        email_list: [],
        host: '',
        assertion: '',
        slave_count: '',
        thread_group: {
          target_concurrency: '',
          ramp_up_time: '',
          ramp_up_steps_count: '',
          hold_target_rate_time: ''
        },
        file_info: [],
        branch: []
      }
      this.form = data
    }
  }
}
</script>

<style>
.page-title {
  font-size: 18px;
  margin: 0;
}

.thread-group {
  width: 100%;
  height: 40px;
  margin-top: 10px;
}

.thread-group-title {
  float: left;
  margin-left: 38px;
  font-size: 14px !important;
  font-weight: 500 !important;
}

.foot-button {
  width: 100%;
  text-align: right;
  margin-top: 20px;
}

.hint {
  background-color: #e7faf5;
  color: #0acf97;
  padding: 0px 16px;
}

.base-info-option .el-form-item__content {
  width: 420px;
}
.base-info-option .el-form-item__label {
  width: 80px;
}
.thread-info-option .el-form-item__label {
  width: 120px !important;
}
</style>
