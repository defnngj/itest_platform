<!--
/**
* @module components
* @author huzhiheng
* @date 2021年1月8日
* @desc 项目列表组件
*/
-->
<template>
  <div class="project">
    <div style="padding-bottom: 20px; height: 30px;">
      <span class="span-left">
        <h4 class="page-title">项目管理</h4>
      </span>
      <span class="span-breadcrumb">
        <el-breadcrumb separator="/">
          <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
          <el-breadcrumb-item>项目管理</el-breadcrumb-item>
        </el-breadcrumb>
      </span>
    </div>
    <el-card class="main-card">
      <div style="padding-bottom: 20px; height: 45px;">
        <span class="span-right">
          <el-button cy-data="search-button" type="primary" @click="searchProject">搜索</el-button>
        </span>
        <span class="span-right">
          <el-input cy-data="search-project" v-model="query.name" placeholder="请输入项目名称" clearable></el-input>
        </span>
        <span class="span-left">
          <el-button cy-data="create-project" type="primary" @click="showCreate">创建</el-button>
        </span>
      </div>
      <!-- 项目表格 -->
      <el-table v-loading="loading" :data="tableData" style="width: 100%">
        <el-table-column prop="name" label="名称">
          <template slot-scope="scope">
            <router-link  type="primary" :to="{path:'/cases', name:'Cases', params: { project: scope.row.id }}">
              {{ scope.row.name }}
              <i class="el-icon-connection"></i>
            </router-link>
          </template>
        </el-table-column>
        <el-table-column prop="describe" label="备注"> </el-table-column>
        <el-table-column prop="status" label="状态">
         <template slot-scope="scope">
            <span v-if="scope.row.status === true">开启</span>
            <span v-else> 关闭 </span>
          </template>
        </el-table-column>
        <el-table-column prop="create_time" label="创建时间"> </el-table-column>
        <el-table-column prop="update_time" label="更新时间"> </el-table-column>
        <el-table-column fixed="right" label="操作" width="120">
          <template slot-scope="scope">
            <el-button cy-data="edit-project" type="text" size="small" @click="showEdit(scope.row)">编辑</el-button>
            <el-button cy-data="delete-project" type="text" size="small" @click="deleteProject(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <!-- 分页功能 -->
      <div class="page">
        <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="query.current_page" :page-sizes="[10, 20, 50]" :page-size="query.page_size" layout="total, sizes, prev, pager, next" :total="total">
        </el-pagination>
      </div>
    </el-card>
    <ProjectDialog v-if="dialogFlag" :type="dialogType" :projectId="projectId" @cancel="cancelProject">
    </ProjectDialog>
  </div>
</template>

<script>
import ProjectDialog from './ProjectDialog.vue'
import ProjectApi from '../../request/project'

export default {
  components: { ProjectDialog },
  data() {
    return {
      dialogType: 'create',
      projectId: 0,
      loading: true,
      tableData: [],
      dialogFlag: false,
      query: {
        page: 1,
        size: 10,
        name: ''
      },
      total: 0
    }
  },

  mounted() {
    this.initProject()

  },

  methods: {
    // 初始化项目列表
    async initProject() {
      const resp = await ProjectApi.getProjects(this.query)
      if (resp.success === true) {
        this.tableData = resp.data.projectList
        this.total = resp.data.total
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
      this.projectId = row.id
      this.dialogFlag = true
    },

    // 关闭编辑项目组件
    cancelProject() {
      this.dialogFlag = false
      this.initProject()
    },

    // 删除项目
    deleteProject(row) {
      this.$confirm('确认要删除项目？', { type: 'warning' })
        .then(_ => {
          console.log('删除确认', _)
          ProjectApi.deleteProject(row.id).then(resp => {
            if (resp.success === true) {
              this.$message({
                message: '删除成功！',
                type: 'success'
              })
              this.initProject()
            } else {
              this.$message.error(resp.error.message)
            }
          })
        })
        .catch(_ => {
          console.log('删除取消', _)
        })
    },

    // 搜索项目
    async searchProject() {
      this.initProject()
      // const resp = await ProjectApi.getProjects(this.query)
      // if (resp.success === true) {
      //   this.tableData = resp.result.data
      //   this.total = resp.result.item_count
      //   this.$message({
      //     message: '搜索完成！',
      //     type: 'success'
      //   })
      // } else {
      //   this.$message.error(resp.error.message)
      // }
    },

    // 改变每页显示数量
    handleSizeChange(val) {
      this.query.size = val
      this.initProject()
    },

    // 翻页
    handleCurrentChange(val) {
      this.query.page = val
      this.initProject()
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
