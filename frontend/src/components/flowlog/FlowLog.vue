<template>
  <div class="flowlog">
    <div style="padding-bottom: 20px; height: 30px;">
      <span class="span-left">
        <h4 class="page-title">流量日志</h4>
      </span>
      <span class="span-breadcrumb">
        <el-breadcrumb separator="/">
          <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
          <el-breadcrumb-item>流量日志</el-breadcrumb-item>
        </el-breadcrumb>
      </span>
    </div>
    <el-card class="main-card">
      <div style="padding-bottom: 20px; height: 45px;">
        <span class="span-right">
          <el-button type="primary" @click="searchFlowlog">搜索</el-button>
        </span>
        <span class="span-right">
          <el-input v-model="query.keyword" clearable placeholder="请输入内容"></el-input>
        </span>
        <span class="span-left">
          <el-button type="primary" @click="showCreate">创建</el-button>
        </span>
      </div>
      <el-table v-loading="loading" :data="tableData" style="width: 100%">
        <el-table-column prop="name" label="名称" width="100"> </el-table-column>
        <el-table-column prop="params.protocol" label="协议" min-width="80"> </el-table-column>
        <el-table-column prop="params.url_path" label="接口"> </el-table-column>
        <el-table-column prop="method" label="方法" min-width="80">
          <template slot-scope="scope">
            <span class="request-method">{{ scope.row.params.method }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="start_time" label="脚本时间" min-width="160">
          <template slot-scope="scope">
            <span>{{ scope.row.start_time }}</span> <br>
            <span>{{ scope.row.end_time }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="user_name" label="创建人" min-width="120"> </el-table-column>
        <el-table-column prop="status" label="状态" width="90">
          <template slot-scope="scope">
            <el-tag :type="(scope.row.status == 'Update' ? '' : (scope.row.status == 'Done' ? 'success' : (scope.row.status == 'Error' ? 'danger' : (scope.row.status == 'Running' ? 'warning' : 'info'))))" size="mini">
              {{ scope.row.status == 'Update' ? 'Update' : (scope.row.status == 'Done' ? 'Done' : (scope.row.status == 'Error' ? 'Error' : (scope.row.status == 'Running' ? 'Running' : 'Create'))) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="create_time" label="创建时间" min-width="160"> </el-table-column>
        <el-table-column fixed="right" label="操作" min-width="80">
          <template slot-scope="scope">
            <span>
              <el-button cy-data="edit-flowlog" @click="showEdit(scope.row)" type="text" size="small" :disabled="scope.row.status === 'Running'?true:false">编辑</el-button>
              <!--  -->
            </span> <br>
            <el-button cy-data="delete-flowlog" @click="deleteFlowlog(scope.row)" type="text" size="small" :disabled="scope.row.status === 'Running'?true:false">删除</el-button>
          </template>
        </el-table-column>
        <el-table-column fixed="right" label="日志" min-width="80">
          <template slot-scope="scope">
            <span v-if="scope.row.status !== 'Done'">
                <el-button cy-data="generate-log" @click="generateLog(scope.row)" type="text" size="small" :disabled="scope.row.status === 'Running'?true:false">生成日志</el-button>
            </span>
            <span v-if="scope.row.status === 'Done'">
              <el-button cy-data="show-log" @click="showLog(scope.row)" type="text" size="small">日志详情</el-button>
            </span>
          </template>
        </el-table-column>
      </el-table>
      <!-- 分页功能 -->
      <div class="page">
        <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="query.current_page" :page-sizes="[10, 20, 50]" :page-size="query.page_size" layout="total, sizes, prev, pager, next" :total="total">
        </el-pagination>
      </div>
    </el-card>
    <FlowLogDialog v-if="dialogFlag" :type="dialogType" :flowlogId="flowlogId" @cancel="cancelFlowlog"></FlowLogDialog>
    <LogDialog v-if="logFlag" :flowlogId="flowlogId" @cancel="cancelFlowlog"></LogDialog>
  </div>
</template>

<script>
import FlowLogDialog from './FlowLogDialog.vue'
import LogDialog from './LogDialog.vue'
import FlowlogApi from '../../request/flowlog'

export default {
  components: { FlowLogDialog, LogDialog },
  data() {
    return {
      dialogFlag: false,
      logFlag: false,
      caseFlag: false,
      dialogType: 'create',
      flowlogId: 0,
      flowlogName: '',
      loading: true,
      tableData: [],
      query: {
        current_page: 1,
        page_size: 10,
        keyword: ''
      },
      total: 0
    }
  },

  mounted() {
    this.initFlowlog()
  },

  methods: {
    // 初始化流量日志列表
    async initFlowlog() {
      const resp = await FlowlogApi.getFlowlogs(this.query)
      if (resp.success === true) {
        this.tableData = resp.result.data
        this.total = resp.result.item_count
      } else {
        this.$message.error(resp.error.message)
      }
      this.loading = false
    },

    // 显示创建弹窗
    showCreate() {
      this.dialogType = 'create'
      this.dialogFlag = true
    },

    // 显示编辑弹窗
    showEdit(row) {
      this.dialogType = 'edit'
      this.flowlogId = row.id
      this.dialogFlag = true
    },

    // 删除日志
    deleteFlowlog(row) {
      this.$confirm('确认要删除流量日志？', { type: 'warning' })
        .then(_ => {
          console.log('删除确认', _)
          FlowlogApi.deleteFlowlog(row.id).then(resp => {
            if (resp.success === true) {
              this.$message({
                message: '删除成功！',
                type: 'success'
              })
              this.initFlowlog()
            } else {
              this.$message.error(resp.error.message)
            }
          })
        })
        .catch(_ => {
          console.log('删除取消', _)
        })
    },

    // 生成日志文件
    async generateLog(row) {
      this.loading = true
      const resp = await FlowlogApi.createLog(row.id)
      if (resp.success === true) {
        this.$message({
          message: '生成脚本成功！',
          type: 'success'
        })
        this.initFlowlog()
      } else {
        this.$message.error(resp.error.message)
      }
      this.loading = false
    },

    // 显示日志详情弹窗
    showLog(row) {
      this.flowlogId = row.id
      this.logFlag = true
    },

    // 显示创建用例
    showCase(row) {
      this.flowlogId = row.id
      this.flowlogName = row.name
      this.caseFlag = true
    },

    // 关闭创建/编辑流量日志组件
    cancelFlowlog() {
      this.dialogFlag = false
      this.logFlag = false
      this.caseFlag = false
      this.initFlowlog()
    },

    // 搜索项目
    async searchFlowlog() {
      const resp = await FlowlogApi.getFlowlogs(this.query)
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
    },

    // 改变每页显示数量
    handleSizeChange(val) {
      this.query.page_size = val
      this.initFlowlog()
    },

    // 翻页
    handleCurrentChange(val) {
      this.query.current_page = val
      this.initFlowlog()
    }
  }
}
</script>

<style scoped>
.page {
  float: right;
  margin-top: 10px;
  margin-bottom: 30px;
}

.request-method {
  color: #6c3;
  font-weight: 700;
  float: left;
  font-size: 14px;
}
</style>
