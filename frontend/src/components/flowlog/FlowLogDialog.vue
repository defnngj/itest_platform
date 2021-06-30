<!--
/**
* @module components
* @author huzhiheng
* @date 2021年1月25日
* @desc 创建/编辑流量日志组件
*/
-->
<template>
  <div id="flowlog-dialog">
    <el-dialog :visible.sync="dialogVisible" @close="cancelFlowlog()" width="600px">
      <div slot="title" class="common-title">
        {{ dialogTitle }}
      </div>
      <div class="flowlog-dialog-content">
        <el-form ref="form" :model="form" :rules="rules" label-width="100px">
          <el-form-item label="名称" prop="name">
            <el-input cy-data="name" v-model="form.name"></el-input>
          </el-form-item>
          <el-form-item label="备注">
            <el-input cy-data="desc" type="textarea" v-model="form.describe"></el-input>
          </el-form-item>
          <el-divider content-position="left">查询规则</el-divider>
          <el-form-item label="服务名称" prop="params.service_name">
            <el-select cy-data="service-name" v-model="form.params.service_name" filterable placeholder="服务名称">
              <el-option cy-data="service-name-list" v-for="item in serviceOptions" :key="item.value" :label="item.label" :value="item.label">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="接口" prop="params.url_path">
            <el-select cy-data="url-path" v-model="form.params.url_path" filterable placeholder="接口">
              <el-option cy-data="url-path-list" v-for="item in urlpathOptions" :key="item.value" :label="item.label" :value="item.label">
              </el-option>
            </el-select>
          </el-form-item>
          <el-row>
            <el-col :span="12">
              <el-form-item label="协议" prop="params.protocol">
                  <el-select cy-data="protocol" v-model="form.params.protocol" placeholder="协议">
                    <el-option cy-data="protocol-list" v-for="item in protocolOption" :key="item.value" :label="item.label" :value="item.value">
                    </el-option>
                  </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="方法" prop="params.method">
                <el-select cy-data="method" v-model="form.params.method" placeholder="方法">
                  <el-option cy-data="method-list" v-for="item in methodOption" :key="item.value" :label="item.label" :value="item.value">
                  </el-option>
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
          <el-form-item label="日期" prop="start_time">
            <span class="data-time">
              <el-input cy-data="start-time" placeholder="请输入开始时间" suffix-icon="el-icon-date" v-model="form.start_time"> </el-input>
            </span>
            <span class="data-time">
              <el-input cy-data="end-time" placeholder="请输入结束时间" suffix-icon="el-icon-date" v-model="form.end_time"> </el-input>
            </span>
          </el-form-item>
        </el-form>
      </div>
      <span slot="footer" class="dialog-footer">
        <!-- <el-button cy-data="show-log" type="danger" @click="showLog('form')">查看日志</el-button> -->
        <!-- <span v-if this.type === 'edit' -->
        <el-button cy-data="cancel-button" @click="cancelFlowlog()">取消</el-button>
        <el-button cy-data="save-button" v-loading.fullscreen.lock="loading" type="primary" @click="saveFlowlog('form')">保存</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import FlowlogApi from '../../request/flowlog'
import MonitorApi from '../../request/monitor'
import { timestampToString, stringToTimestamp } from '../../assets/js/datetime-utils'

export default {
  name: 'FlowlogDialog',
  props: ['type', 'flowlogId'],
  data() {
    const validateTime = (rule, value, callback) => {
      const start_time = stringToTimestamp(value)
      const end_time = stringToTimestamp(this.form.end_time)
      // 计算时间差，分钟为单位
      const interval_time = parseInt((end_time - start_time) / (60 * 1000))
      if (interval_time <= 0) {
        callback(new Error('结束时间应大于开始时间'));
      } else if (interval_time > 60) {
        callback(new Error('时间间隔应小于1小时'));
      } else {
        callback();
      }
    };
    return {
      dialogVisible: true,
      dialogTitle: '',
      loading: false,
      serviceOptions: [],
      urlpathOptions: [],
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
      query: {
        current_page: 1,
        page_size: 10000,
        monitor_name: ''
      },
      form: {
        id: 0,
        orion_id: '',
        name: '',
        describe: '',
        params: {
          service_name: '',
          url_path: '',
          protocol: 'HTTP',
          method: 'GET'
        },
        start_time: '',
        end_time: ''
      },
      rules: {
        name: [{ required: true, message: '请输入名称', trigger: 'blur' }],
        start_time: [
          { required: true, message: '请输入名称', trigger: 'blur' },
          { validator: validateTime, trigger: 'blur' }
        ],

        params: {
          service_name: [
            { required: true, message: '请选择服务名称', trigger: 'blur' }
          ],
          url_path: [
            { required: true, message: '请选择接口名称', trigger: 'blur' }
          ],
          protocol: [
            { required: true, message: '请选择协议', trigger: 'blur' }
          ],
          method: [{ required: true, message: '请选择方法', trigger: 'blur' }]
        }
      }

    }
  },

  mounted() {
    if (this.type === 'create') {
      this.dialogTitle = '创建流量日志'
      const date = new Date()
      this.form.start_time = timestampToString(date.getTime() - 3600 * 1000)
      this.form.end_time = timestampToString(date.getTime())
      this.initServername()
      this.initUrlpath()
    } else if (this.type === 'edit') {
      this.dialogTitle = '编辑流量日志'
      this.initFlowlog()
      this.initServername()
      this.initUrlpath()
    }
  },

  methods: {
    // 获取项目信息
    async initFlowlog() {
      const resp = await FlowlogApi.getFlowlog(this.flowlogId)
      if (resp.success === true) {
        this.form = resp.result
      } else {
        this.$message.error(resp.error.message)
      }
    },

    // 初始化服务名称分组
    async initServername() {
      const resp = await MonitorApi.getMonitors(this.query)
      if (resp.success === true) {
        const data = resp.result.data
        for (const i in data) {
          let name = data[i].name
          name = name.substring(name.indexOf('/') + 1, name.length)
          this.serviceOptions.push({
            value: data[i].id,
            label: name
          })
        }
      } else {
        this.$message.error(resp.error.message)
      }
    },

    // 初始化接口分组
    async initUrlpath() {
      const resp = await FlowlogApi.getUrllist()
      if (resp.success === true) {
        const data = resp.result
        for (const i in data) {
          this.urlpathOptions.push({
            value: data[i].id,
            label: data[i].url
          })
        }
      } else {
        this.$message.error(resp.error.message)
      }
    },

    // 关闭弹窗
    cancelFlowlog() {
      this.form.id = 0
      this.form.name = ''
      this.form.desc = ''
      this.form.params.url_path = ''
      this.form.params.protocol = ''
      this.form.params.method = ''
      this.form.start_time = ''
      this.form.end_time = ''
      this.$emit('cancel', {})
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

    // 保存项目
    async saveFlowlog(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          // 判断日期不能为空
          if (this.form.end_time === '') {
            this.$message.error('请输入结束时间!')
            return
          }
          this.loading = true
          // 创建
          if (this.type === 'create') {
            FlowlogApi.createFlowlog(this.form).then(resp => {
              if (resp.success === true) {
                this.$message({
                  message: '创建成功！',
                  type: 'success'
                })
                this.cancelFlowlog()
              } else {
                this.$message.error(resp.error.message)
              }
            })
            // 编辑
          } else if (this.type === 'edit') {
            FlowlogApi.updateFlowlog(this.form).then(resp => {
              if (resp.success === true) {
                this.$message({
                  message: '更新成功！',
                  type: 'success'
                })
                this.cancelFlowlog()
              } else {
                this.$message.error(resp.error.message)
              }
            })
          }
          this.loading = false
        } else {
          this.$message.error('必填参数为空!!')
          return false
        }
      })
    }
  }
}
</script>

<style>
.flowlog-dialog-content {
  padding-right: 50px;
  text-align: left;
  font-size: 14px;
}
.data-time .el-input {
  width: 50% !important;
}
.protocol .el-select{
  width: 50% !important;
}
.el-dialog{
  display: flex;
  flex-direction: column;
  margin:0 !important;
  position:absolute;
  top:50%;
  left:50%;
  transform:translate(-50%,-50%);
  /*height:600px;*/
  max-height:calc(100% - 120px);
  max-width:calc(100% - 360px);
}

.el-dialog .el-dialog__body{
  flex:1;
  overflow: auto;
}
.el-dialog .el-dialog__footer{
  border-top: hidden ;
}
</style>
