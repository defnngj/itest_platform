<!--
/**
* @module components
* @author huzhiheng
* @date 2021年3月16日
* @desc 查看日志组件
*/
-->
<template>
  <div id="logs-dialog">
    <el-dialog :visible.sync="logVisible" @close="cancelCreate(0)" width="50%" append-to-body>
      <div slot="title" class="common-title">
        生成测试用例
      </div>
      <div class="pargress">
        <div class="progress-bar">
          <el-steps :space="200" :active="step" finish-status="success">
            <el-step :title="step_one"></el-step>
            <el-step :title="step_two"></el-step>
            <el-step :title="step_three"></el-step>
            <el-step :title="step_end"></el-step>
          </el-steps>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import FlowlogApi from '../../../request/flowlog'

export default {
  name: 'FlowlogDialog',
  props: ['flowlogData'],
  data() {
    return {
      logVisible: true,
      step: 0,
      flowlogResp: {},
      step_one: '保存配置',
      step_two: '生成日志',
      step_three: '生成用例',
      step_end: '完成',
      result: {
        file_size: 0,
        log_count: 0,
        content: ''
      }
    }
  },

  mounted() {
    this.creatCaseFlow()
  },

  methods: {
    // 休眠方法
    sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms))
    },

    // 创建用例流程
    async creatCaseFlow() {
      // 生成用例
      this.step = 2
      const data = { id: this.flowlogData.id, case_name: this.flowlogData.name + ' - 用例' }
      const resp = await FlowlogApi.createCase(data)
      if (resp.success === true) {
        this.step = 3
        // 4.完成
        await this.sleep(500)
        this.step = 4
        this.cancelCreate(resp.result.id)
      } else {
        this.step_three = '生成用例失败'
      }
    },

    // 关闭弹窗
    cancelCreate(cid) {
      this.$emit('createRsult', { caseId: cid })
    }
  }
}
</script>

<style>
.download-title {
  height: 50px;
  width: 100%;
}

.progress-bar {
  margin-left: 7%;
  padding-right: 20px;
  padding-left: 20px;
  margin-bottom: 30px;
  text-align: left;
  font-size: 14px;
  width: 100%;
}
.pargress {
  padding-left: 15%;
  padding-right: 15%;
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
