<!--
/**
* @module components
* @author huzhiheng
* @date 2021年3月15日
* @desc 自动创建用例 - 流量日志组件
*/
-->
<template>
  <div class="caseCreate">
    <!-- 流量日志 -->
    <div v-show="step === 1">
      <div class="select-flowlog">
        选择:
        <el-select cy-data="flowlog" v-model="query.team" filterable placeholder="请选择已有流量日志" @change="selectFlowlog">
          <el-option cy-data="flowlog-list" v-for="item in flowlogOptions" :key="item.value" :label="item.label" :value="item.value" :disabled="item.disabled">
            <span style="float: left">{{ item.label }}</span>
            <span style="float: right; color: #c0c4cc; font-size: 13px">{{ item.status }}</span>
          </el-option>
        </el-select>
        <!-- or <el-button cy-data="create-flowlog" type="primary" @click="newFlowlog()">新建</el-button> -->
      </div>
      <el-form :inline="true" ref="form" :model="form" :rules="rules" class="demo-form-inline">
        <!-- 基本信息 -->
        <el-divider content-position="left">基本信息</el-divider>
        <div>
          <span class="span-left">
            <el-form-item label="名称" prop="name" class="base-info-option" >
              <el-input cy-data="flowlog-name" v-model="form.name" placeholder="请输入名称" :disabled="isEdit"></el-input>
            </el-form-item>
          </span>
          <el-form-item label="备注" prop="describe" class="base-info-option">
            <el-input cy-data="flowlog-desc" v-model="form.describe" type="textarea" :rows="2" placeholder="请输入备注" :disabled="isEdit">
            </el-input>
          </el-form-item>
        </div>
        <!-- 系统配置 -->
        <el-divider content-position="left">配置规则</el-divider>
        <div>
          <span class="span-left">
            <el-form-item label="接口" prop="params.url_path" class="base-info-option">
              <el-input cy-data="url-path" v-model="form.params.url_path" :disabled="isEdit"></el-input>
            </el-form-item>
          </span>
          <el-form-item label="协议" prop="params.protocol" class="base-info-option">
            <el-select cy-data="protocol" v-model="form.params.protocol" placeholder="协议" :disabled="isEdit">
              <el-option cy-data="protocol-list" v-for="item in protocolOption" :key="item.value" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
        </div>
        <div style="overflow:auto;">
          <span class="span-left">
            <el-form-item label="日期" prop="start_time" class="base-info-option">
              <span class="data-time">
                <el-input cy-data="start-time" placeholder="请输入开始时间" suffix-icon="el-icon-date" v-model="form.start_time" :disabled="isEdit"> </el-input>
              </span>
              <span class="data-time">
                <el-input cy-data="end-time" placeholder="请输入结束时间" suffix-icon="el-icon-date" v-model="form.end_time" :disabled="isEdit"> </el-input>
              </span>
            </el-form-item>
          </span>
          <el-form-item label="方法" prop="params.method" class="base-info-option">
            <el-select cy-data="method" v-model="form.params.method" placeholder="方法" :disabled="isEdit">
              <el-option cy-data="method-list" v-for="item in methodOption" :key="item.value" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
        </div>
        <div class="foot-button">
          <!-- <el-button cy-data="show-log" type="danger" @click="showLog('form')">查看日志</el-button> -->
          <el-button cy-data="generate-case" type="primary" @click="createCase('form')">生成用例</el-button>
        </div>
      </el-form>
    </div>
    <LogDialog v-if="logFlag" :flowlogData="form" @cancel="cancelDialog"></LogDialog>
    <CreateDialog v-if="createFlag" :flowlogData="form" @cancel="cancelDialog" @createRsult="createRsult"></CreateDialog>
  </div>
</template>

<script>
import FlowlogApi from '../../../request/flowlog'
import CreateDialog from './CreateDialog'
import LogDialog from './LogDialog'
import { timestampToString } from '../../../assets/js/datetime-utils'

export default {
  name: 'caseCreate',
  props: ['caseId'],
  components: { LogDialog, CreateDialog },
  data() {
    return {
      step: 1,
      logFlag: false,
      createFlag: false,
      envIds: [],
      flowlogOptions: [],
      protocolOption: [
        {
          value: 'HTTP',
          label: 'HTTP'
        },
        {
          value: 'gRPC',
          label: 'gRPC'
        }
      ],
      methodOption: [
        {
          value: 'GET',
          label: 'GET'
        }
      ],
      form: {
        id: 0,
        orion_id: '',
        name: '',
        describe: '',
        params: {
          url_path: '',
          protocol: 'HTTP',
          method: 'GET'
        },
        start_time: '',
        end_time: ''
      },
      rules: {
        name: [{ required: true, message: '请输入名称', trigger: 'blur' }],
        start_time: [{ required: true, message: '请输入开始结束时间', trigger: 'blur' }],
        params: {
          url_path: [
            { required: true, message: '请输入接口名称', trigger: 'blur' }
          ],
          protocol: [
            { required: true, message: '请选择协议', trigger: 'blur' }
          ],
          method: [{ required: true, message: '请选择方法', trigger: 'blur' }]
        }
      },
      isEdit: true,
      query: {
        current_page: 1,
        page_size: 10000,
        monitor_name: ''
      }
    }
  },

  mounted() {
    this.initFlowlog()
    const date = new Date()
    this.form.start_time = timestampToString(date.getTime() - 3600 * 1000 * 24)
    this.form.end_time = timestampToString(date.getTime())
  },

  methods: {
    // 初始化流量日志列表
    async initFlowlog() {
      const resp = await FlowlogApi.getFlowlogs(this.query)
      if (resp.success === true) {
        this.flowlogOptions = []
        const data = resp.result.data
        for (const i in data) {
          if (data[i].status === 'Done') {
            this.flowlogOptions.push({
              value: data[i].id,
              label: data[i].name,
              status: data[i].status,
              disabled: false
            })
          } else {
            this.flowlogOptions.push({
              value: data[i].id,
              label: data[i].name,
              status: data[i].status,
              disabled: true
            })
          }
        }
        this.total = resp.result.item_count
      } else {
        this.$message.error(resp.error.message)
      }
    },

    // 选择已有流量日志
    async selectFlowlog(selVal) {
      const resp = await FlowlogApi.getFlowlog(selVal)
      if (resp.success === true) {
        this.form = resp.result
      } else {
        this.$message.error(resp.error.message)
      }
    },

    // 新建流量日志 - 清空表单
    newFlowlog() {
      this.form.id = 0
      this.cleanFlowlog()
    },

    // 查看流量日志
    async showLog(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          // 判断日期不能为空
          if (this.form.end_time === '') {
            this.$message.error('请输入结束时间!')
            return
          }
          this.logFlag = true
        } else {
          this.$message.error('必传字段为空!!')
          return false
        }
      })
    },

    // 生成用例
    createCase(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          // 判断日期不能为空
          if (this.form.end_time === '') {
            this.$message.error('请选择截取流量日期!')
            return
          }
          this.createFlag = true
        } else {
          this.$message.error('必传字段为空!!')
          return false
        }
      })
    },

    // 关闭创建/编辑流量日志组件
    cancelDialog() {
      this.logFlag = false
      this.createFlag = false
    },

    // 创建进度 - 返回结果
    createRsult(data) {
      if (data.caseId !== 0) {
        this.$emit('caseId', data)
      }
      this.createFlag = false
      this.initFlowlog()
    },

    // 清空表单
    cleanFlowlog() {
      this.query.team = ''
      this.form.name = ''
      this.form.describe = ''
      this.form.params.url_path = ''
    }
  }
}
</script>

<style>
.page-title {
  font-size: 18px;
  margin: 0;
}

.select-flowlog {
  text-align: left;
  margin-top: 30px;
  margin-bottom: 50px;
  margin-left: 40px;
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
  width: 180px;
}
</style>
