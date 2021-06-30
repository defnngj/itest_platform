<!--
/**
* @module components
* @author huzhiheng
* @date 2021年1月22日
* @desc 查看实例详情
*/
-->
<template>
  <div id="env-edit">
    <el-dialog :visible.sync="dialogVisible" @close="cancelEnv()" width="600px">
      <div slot="title" class="common-title">
        实例详情
      </div>
      <div class="details-dialog">
        <el-table :data="tableData" stripe style="width: 100%">
          <el-table-column prop="service_name" label="服务名">
          </el-table-column>
          <el-table-column prop="instance_utilization" label="实例数">
          </el-table-column>
        </el-table>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import MonitorApi from '../../../request/monitor'

export default {
  name: 'envEdit',
  // props: ['envId'],
  data() {
    return {
      dialogVisible: true,
      tableData: [],
      query: {
        current_page: 1,
        page_size: 10,
        service_name: 'klook-kmeter/slaveserv'
      }
    }
  },

  mounted() {
    this.initEnv()
  },

  methods: {
    // 获取项目信息
    async initEnv() {
      const respMonitors = await MonitorApi.getMonitors(this.query)
      if (respMonitors.success === true) {
        this.envId = respMonitors.result.data[0].id
        const resp = await MonitorApi.getMonitor(this.envId)
        if (resp.success === true) {
          this.tableData.push(resp.result.service_detail)
        } else {
          this.$message.error(resp.error.message)
        }
      } else {
        this.$message.error(respMonitors.error.message)
      }
    },

    // 关闭弹窗
    cancelEnv() {
      this.$emit('cancel', {})
    }
  }
}
</script>

<style>
.env-dialog-content {
  padding-right: 50px;
  text-align: left;
  font-size: 14px;
}

.details-dialog {
  margin-left: 20px;
  margin-right: 20px;
  margin-top: 10px;
  margin-bottom: 30px;
  height: 120px
}
</style>
