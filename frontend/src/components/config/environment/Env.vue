<!--
/**
* @module components
* @author huzhiheng
* @date 2021年1月21日
* @desc 环境列表组件
*/
-->
<template>
  <div class="env">
    <div style="padding-bottom: 20px; height: 30px;">
      <span class="span-left">
        <h4 class="page-title">环境管理</h4>
      </span>
      <span class="span-breadcrumb">
        <el-breadcrumb separator="/">
          <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
          <el-breadcrumb-item>配置管理</el-breadcrumb-item>
          <el-breadcrumb-item>环境管理</el-breadcrumb-item>
        </el-breadcrumb>
      </span>
    </div>
    <el-card class="main-card">
      <el-table :data="tableData" style="width: 100%">
        <el-table-column prop="name" label="名称"> </el-table-column>
        <el-table-column prop="host" label="HOST"> </el-table-column>
        <el-table-column prop="status" label="状态">
          <template slot-scope="scope">
            <el-tag>{{ scope.row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="user_name" label="创建人"> </el-table-column>
        <el-table-column prop="create_time" label="创建时间"> </el-table-column>
        <el-table-column prop="update_time" label="更新时间"> </el-table-column>
        <el-table-column fixed="right" label="操作">
          <template slot-scope="scope">
            <el-button id="editEnv" type="text" size="small" @click="showEdit(scope.row)">编辑</el-button>
            <el-button id="detailsEnv" type="text" size="small" @click="showDetails(scope.row)">详情</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    <EnvEdit v-if="editFlag" :envId="envId" @cancel="cancelEnv">
    </EnvEdit>
    <EnvDetails v-if="detailsFlag" :envId="envId" @cancel="cancelEnv"></EnvDetails>
  </div>
</template>

<script>
import EnvEdit from './EnvEdit.vue'
import EnvDetails from './EnvDetails.vue'
import EnvApi from '../../../request/environment'

export default {
  name: 'env',
  components: { EnvEdit, EnvDetails },
  data() {
    return {
      envId: 0,
      tableData: [],
      editFlag: false,
      detailsFlag: false,
      query: {
        current_page: 1,
        page_size: 10
      }
    }
  },

  mounted() {
    this.initEnv()
  },

  methods: {
    // 初始化环境列表
    async initEnv() {
      const resp = await EnvApi.getEnvs(this.query)
      if (resp.success === true) {
        this.tableData = resp.result.data
      } else {
        this.$message.error(resp.error.message)
      }
    },

    // 显示编辑弹窗
    showEdit(row) {
      this.envId = row.id
      this.editFlag = true
    },

    // 显示详情弹窗
    showDetails(row) {
      this.envId = row.id
      this.detailsFlag = true
    },

    // 关闭编辑环境组件
    cancelEnv() {
      this.editFlag = false
      this.detailsFlag = false
      this.initEnv()
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
