<!--
/**
* @module components
* @author huzhiheng
* @date 2021年1月8日
* @desc 查看监控分组组件
*/
-->
<template>
  <div id="monitorDialog">
    <el-dialog :visible.sync="dialogVisible" @close="cancelMonitor()" width="800px">
      <div slot="title" class="common-title">
        监控分组详情
      </div>
      <div class="dialog-content">
        <div>
          <el-divider content-position="left">服务基础信息</el-divider>
          <el-table :data="baseTable" border style="width: 100%" :header-cell-style="{background:'#F1F3FA'}" v-loading="loading">
            <el-table-column prop="service_name" label="服务名"> </el-table-column>
            <el-table-column prop="team_name" label="团队"> </el-table-column>
            <el-table-column prop="domain" label="Domain"> </el-table-column>
            <el-table-column prop="owner" label="负责人"> </el-table-column>
            <el-table-column prop="instance_utilization" label="实例数"> </el-table-column>
          </el-table>
        </div>
        <div class="details-line">
          <el-divider content-position="left">关联服务信息</el-divider>
          <el-table :data="servicesTable" border style="width: 100%" :header-cell-style="{background:'#F1F3FA'}" v-loading="loading">
            <el-table-column prop="service_name" label="服务名"> </el-table-column>
            <el-table-column prop="team_name" label="团队"> </el-table-column>
            <el-table-column prop="domain" label="Domain"> </el-table-column>
            <el-table-column prop="owner" label="负责人"> </el-table-column>
            <el-table-column prop="instance_utilization" label="实例数"> </el-table-column>
          </el-table>
        </div>
        <div class="details-line">
          <el-divider content-position="left">关联资源信息</el-divider>
          <el-table :data="resourceTable" border style="width: 100%" :header-cell-style="{background:'#F1F3FA'}" v-loading="loading">
            <el-table-column prop="name" label="资源名"> </el-table-column>
            <el-table-column prop="team" label="团队">
              <template slot-scope="scope">
                <div v-for="(item, i) in scope.row.teams" :key="i" class="text item">
                  {{ item.team_name }}
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="code" label="类型"> </el-table-column>
            <el-table-column prop="status" label="状态"> </el-table-column>
          </el-table>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import MonitorApi from '../../../request/monitor'

export default {
  name: 'monitorDialog',
  props: ['type', 'monitorId'],
  data() {
    return {
      loading: false,
      dialogVisible: true,
      dialogTitle: '',
      baseTable: [],
      servicesTable: [],
      resourceTable: []
    }
  },

  mounted() {
    this.initMonitor()
  },

  methods: {
    // 获取分组详情
    async initMonitor() {
      this.loading = true
      const resp = await MonitorApi.getMonitor(this.monitorId)
      if (resp.success === true) {
        this.form = resp.result
        this.baseTable.push(resp.result.service_detail)
        this.servicesTable = resp.result.relate_services
        this.resourceTable = resp.result.relate_resource_utilization
      } else {
        this.$message.error(resp.error.message)
      }
      this.loading = false
    },

    // 关闭弹窗
    cancelMonitor() {
      this.$emit('cancel', {})
    }

  }
}
</script>

<style>
.details-line {
  margin-top: 30px;
  height: auto;
  overflow: auto;
}
.dialog-content {
  padding-right: 50px;
  padding-left: 50px;
  text-align: left;
  font-size: 14px;
}
</style>
