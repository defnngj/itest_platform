<!--
/**
* @module components
* @author huzhiheng
* @date 2021年1月25日
* @desc 查看日志组件
*/
-->
<template>
  <div id="logs-dialog">
    <el-dialog :visible.sync="logVisible" @close="cancelFlowlog()" width="65%">
      <div slot="title" class="common-title">
        查看流量日志
      </div>
      <div class="log-dialog-content">
        <div class="download-title">
          <span class="span-left">
            <i class="el-icon-document"> </i>
            Lines: {{ result.log_count }}
            <i class="el-icon-coin"></i>
            Bytes: {{ result.file_size }} （仅展示前100行数据）
          </span>
        </div>
        <div class="flowlog-content">
          <div v-for="(item, index) in result.content" :key="index" class="text item">
            Line: {{ index }} <br>
            {{ item }}
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import FlowlogApi from '../../request/flowlog'

export default {
  name: 'FlowlogDialog',
  props: ['flowlogId'],
  data() {
    return {
      logVisible: true,
      result: {
        file_size: 0,
        log_count: 0,
        content: ''
      }
    }
  },

  mounted() {
    this.initLog()
  },

  methods: {
    // 获取日志
    async initLog() {
      const resp = await FlowlogApi.getLog(this.flowlogId)
      if (resp.success === true) {
        this.result = resp.result
      } else {
        this.$message.error(resp.error.message)
      }
    },

    // 关闭弹窗
    cancelFlowlog() {
      this.$emit('cancel', {})
    }
  }
}
</script>

<style>
.download-title {
  height: 50px;
  width: 100%;
}

.log-dialog-content {
  padding-right: 20px;
  padding-left: 20px;
  margin-bottom: 30px;
  text-align: left;
  font-size: 14px;
}

.flowlog-content {
  min-height: 320px;
  max-height: 380px;
  overflow: auto;
  background-color: #f1f3fa;
  box-shadow: 1px 1px 5px 3px #eef2f7;
}
</style>
