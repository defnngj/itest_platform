<!--
/**
* @module components
* @author huzhiheng
* @date 2021年02月01日
* @desc 监控列表组件
*/ 服务名、团队、Domain、负责人
-->
<template>
  <div class="monitor">
    <div style="padding-bottom: 20px; height: 30px;">
      <span class="span-left">
        <h4 class="page-title">监控分组</h4>
      </span>
      <span class="span-breadcrumb">
        <el-breadcrumb separator="/">
          <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
          <el-breadcrumb-item>配置管理</el-breadcrumb-item>
          <el-breadcrumb-item>监控分组</el-breadcrumb-item>
        </el-breadcrumb>
      </span>
    </div>
    <el-card class="main-card">
      <div style="padding-bottom: 20px; height: 45px;">
        <span class="span-right">
          <el-button type="primary" @click="searchServer">搜索</el-button>
        </span>
        <span class="span-right">
          <el-input v-model="query.service_name" placeholder="请输入服务名" clearable></el-input>
        </span>
      </div>
      <el-table v-loading="loading" :data="tableData" style="width: 100%">
        <el-table-column prop="service_info.service_name" label="服务名"> </el-table-column>
        <el-table-column prop="service_info.team_name" label="团队"> </el-table-column>
        <el-table-column prop="service_info.domain" label="Domain"> </el-table-column>
        <el-table-column prop="service_info.owner" label="负责人"> </el-table-column>
        <el-table-column fixed="right" label="操作" width="120">
          <template slot-scope="scope">
            <el-button id="deleteMonitor" type="text" size="small" @click="showDetails(scope.row)">详情</el-button>
          </template>
        </el-table-column>
      </el-table>
      <!-- 分页功能 -->
      <div class="page">
        <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="query.current_page" :page-sizes="[10, 20, 50]" :page-size="query.page_size" layout="total, sizes, prev, pager, next" :total="total">
        </el-pagination>
      </div>
    </el-card>
     <MonitorDialog v-if="dialogFlag" :monitorId="monitorId" @cancel="cancelMonitor">
    </MonitorDialog>
  </div>
</template>

<script>
import MonitorDialog from './MonitorDialog.vue'
import MonitorApi from '../../../request/monitor'

export default {
  components: { MonitorDialog },
  data() {
    return {
      dialogType: 'create',
      loading: true,
      monitorId: 0,
      tableData: [],
      dialogFlag: false,
      query: {
        current_page: 1,
        page_size: 10,
        service_name: ''
      },
      total: 0
    }
  },

  mounted() {
    this.initMonitor()
  },

  methods: {
    // 初始化监控分组列表
    async initMonitor() {
      const resp = await MonitorApi.getMonitors(this.query)
      if (resp.success === true) {
        this.tableData = resp.result.data
        this.total = resp.result.item_count
      } else {
        this.$message.error(resp.error.message)
      }
      this.loading = false
    },

    // 关闭编辑监控分组组件
    cancelMonitor() {
      this.dialogFlag = false
      this.initMonitor()
    },

    // 搜索监控分组
    async searchServer() {
      this.loading = true
      const resp = await MonitorApi.getMonitors(this.query)
      if (resp.success === true) {
        this.tableData = resp.result.data
        this.total = resp.result.item_count
        this.$message({
          message: '搜索完成！',
          type: 'success'
        })
      } else {
        this.$message.error(resp.error.message)
      }
      this.loading = false
    },

    // 显示详情
    showDetails(row) {
      this.monitorId = row.id
      this.dialogFlag = true
    },

    // 改变每页显示数量
    handleSizeChange(val) {
      this.query.page_size = val
      this.initMonitor()
    },

    // 翻页
    handleCurrentChange(val) {
      this.query.current_page = val
      this.initMonitor()
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.page {
  float: right;
  margin-top: 10px;
  margin-bottom: 30px;
}
</style>
