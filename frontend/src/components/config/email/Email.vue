<!--
/**
* @module components
* @author huzhiheng
* @date 2021年02月03日
* @desc 邮件分组列表组件
*/
-->
<template>
  <div class="email">
    <div style="padding-bottom: 20px; height: 30px;">
      <span class="span-left">
        <h4 class="page-title">邮件分组</h4>
      </span>
      <span class="span-breadcrumb">
        <el-breadcrumb separator="/">
          <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
          <el-breadcrumb-item>配置管理</el-breadcrumb-item>
          <el-breadcrumb-item>邮件分组</el-breadcrumb-item>
        </el-breadcrumb>
      </span>
    </div>
    <el-card class="main-card">
      <div style="padding-bottom: 20px; height: 45px;">
        <span class="span-right">
          <el-button cy-data="search-button" type="primary" @click="searchEmail">搜索</el-button>
        </span>
        <span class="span-right">
          <el-input cy-data="search-email" v-model="query.name" placeholder="请输入邮件分组名称" clearable></el-input>
        </span>
        <span class="span-left">
          <el-button cy-data="create-button" type="primary" @click="showCreate">创建</el-button>
        </span>
      </div>
      <el-table v-loading="loading" :data="tableData" style="width: 100%">
        <el-table-column prop="name" label="名称"> </el-table-column>
        <el-table-column prop="mail_to" label="发送邮箱">
          <template slot-scope="scope">
            <span v-for="(item, index) in scope.row.mail_to" :key="index">
              <el-tag>{{ item }}</el-tag>
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="user_name" label="创建人"> </el-table-column>
        <el-table-column prop="create_time" label="创建时间"> </el-table-column>
        <el-table-column prop="update_time" label="更新时间"> </el-table-column>
        <el-table-column fixed="right" label="操作" width="120">
          <template slot-scope="scope">
            <el-button cy-data="edit-email" type="text" size="small" @click="showEdit(scope.row)">编辑</el-button>
            <el-button cy-data="delete-email" type="text" size="small" @click="deleteEmail(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <!-- 分页功能 -->
      <div class="page">
        <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="query.current_page" :page-sizes="[10, 20, 50]" :page-size="query.page_size" layout="total, sizes, prev, pager, next" :total="total">
        </el-pagination>
      </div>
    </el-card>
    <EmailDialog v-if="dialogFlag" :type="dialogType" :emailId="emailId" @cancel="cancelEmail">
    </EmailDialog>
  </div>
</template>

<script>
import EmailDialog from './EmailDialog.vue'
import EmailApi from '../../../request/email'

export default {
  components: { EmailDialog },
  data() {
    return {
      dialogType: 'create',
      emailId: 0,
      loading: true,
      tableData: [],
      dialogFlag: false,
      query: {
        current_page: 1,
        page_size: 10,
        name: ''
      },
      total: 0
    }
  },

  mounted() {
    this.initEmail()
  },

  methods: {
    // 初始化邮件分组列表
    async initEmail() {
      const resp = await EmailApi.getEmails(this.query)
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
      this.emailId = row.id
      this.dialogFlag = true
    },

    // 关闭编辑邮件分组组件
    cancelEmail() {
      this.dialogFlag = false
      this.initEmail()
    },

    // 删除邮件分组
    deleteEmail(row) {
      this.$confirm('确认要删除邮件分组？', { type: 'warning' })
        .then(_ => {
          console.log('删除确认', _)
          EmailApi.deleteEmail(row.id).then(resp => {
            if (resp.success === true) {
              this.$message({
                message: '删除成功！',
                type: 'success'
              })
              this.initEmail()
            } else {
              this.$message.error(resp.error.message)
            }
          })
        })
        .catch(_ => {
          console.log('删除取消', _)
        })
    },

    // 搜索邮件分组
    async searchEmail() {
      this.loading = true
      const resp = await EmailApi.getEmails(this.query)
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

    // 改变每页显示数量
    handleSizeChange(val) {
      this.query.page_size = val
      this.initEmail()
    },

    // 翻页
    handleCurrentChange(val) {
      this.query.current_page = val
      this.initEmail()
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
