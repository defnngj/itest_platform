<!--
/**
* @module components
* @author lu.lin
* @date 2021年4月25日
* @desc 文件列表组件
*/
-->

<template>
  <div class="files" v-loading="downloadLoading">
    <div style="padding-bottom: 20px; height: 30px;">
      <span class="span-left">
        <h4 class="page-title" v-if="ListShow">文件管理</h4>
        <!-- <h4 class="page-title" v-if="detailsShow">{{ title }}</h4> -->
      </span>
      <span class="span-breadcrumb">
        <el-breadcrumb separator="/">
          <span v-if="ListShow">
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>文件管理</el-breadcrumb-item>
          </span>
        </el-breadcrumb>
      </span>
    </div>
    <div v-if="ListShow">
      <el-card class="main-card">
        <div style="padding-bottom: 20px; height: 45px;">
          <span class="span-right">
            <el-button type="primary" @click="searchFile">搜索</el-button>
          </span>
          <span class="span-right">
            <el-input v-model="query.name" placeholder="请输入关键字额" clearable></el-input>
          </span>
        </div>
        <el-table v-loading="loading" :data="tableData" style="width: 100%">
          <el-table-column label="ID" min-width='60px'>
            <template slot-scope="scope">{{ scope.$index+(query.current_page - 1) * query.page_size + 1 }}</template>
          </el-table-column>
          <el-table-column prop="file_name" label="文件名"> </el-table-column>
          <el-table-column prop="file_size" label="文件大小" min-width='100px'></el-table-column>
          <el-table-column prop="last_edit_time" label="创建时间"> </el-table-column>
          <el-table-column fixed="right" label="操作" width="140">
            <template slot-scope="scope">
              <el-button id="editFile" type="text" size="small" @click="showDetails(scope.row)">详情</el-button>
              <el-button id="handleFile" type="text" size="small" @click="handleDownload(scope.row)">下载</el-button>
              <el-button id="deleteFile" type="text" size="small" @click="deleteFile(scope.row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
        <!-- 分页功能 -->
        <div class="page">
          <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="query.current_page" :page-sizes="[10, 20, 50]" :page-size="query.page_size" layout="total, sizes, prev, pager, next" :total="total">
          </el-pagination>
        </div>
      </el-card>
    </div>

    <!-- 文件详情 -->
    <div class="file-details" v-if="detailsShow">
      <FileDetailDialog :fileName="name" @cancel="cancelFile"></FileDetailDialog>
    </div>
  </div>
</template>

<script>
import FileApi from '../../request/file'
import FileDetailDialog from './FileDetailDialog'
import { downloadFile } from '../../assets/js/file-download.js'

export default {
  components: { FileDetailDialog },
  data() {
    return {
      title: '文件详情',
      downloadLoading: false,
      loading: true,
      name: '',
      result: {},
      ListShow: true,
      detailsShow: false,
      tableData: [],
      query: {
        current_page: 1,
        page_size: 10,
        name: ''
      },
      total: 0
    }
  },

  mounted() {
    this.notification()
    this.initFiles()
  },

  methods: {
    // 提示
    notification() {
      const h = this.$createElement;
      this.$notify({
        title: '提示',
        message: h('i', '文件需保存在/opt/testcase/datasets/目录'),
        type: 'success',
        duration: 3000
      });
    },

    // 初始化文件列表
    async initFiles() {
      const resp = await FileApi.getFiles(this.query)
      if (resp.success === true) {
        this.tableData = resp.result.data
        // this.tableData = resp.result
        this.total = resp.result.item_count
      } else {
        this.$message.error(resp.error.message)
      }
      this.loading = false
    },

    // 显示文件详情
    showDetails(row) {
      this.name = row.file_name
      this.ListShow = true
      this.$nextTick(() => {
        this.detailsShow = true
      })
    },

    // 关闭报告详情组件
    cancelFile() {
      this.ListShow = true
      this.detailsShow = false
    },

    // 删除文件
    deleteFile(row) {
      this.$confirm('确认要删除文件？', { type: 'warning' })
        .then(_ => {
          console.log('删除确认', _)
          FileApi.deleteFile(row.file_name).then(resp => {
            if (resp.success === true) {
              this.$message({
                message: '删除成功！',
                type: 'success'
              })
              this.initFiles()
            } else {
              this.$message.error(resp.error.message)
            }
          })
        })
        .catch(_ => {
          console.log('删除取消', _)
        })
    },

    // 下载文件
    handleDownload(row) {
      this.downloadLoading = true
      this.result = FileApi.downloadFile(row.file_name).then(res => {
        const name = row.file_name;
        downloadFile(name, res)
      }).catch(e => {
        this.$message.error({ message: e.message, showClose: true });
      })
        .finally(() => {
          this.downloadLoading = false
        });
    },

    // 搜索报告
    async searchFile() {
      this.loading = true
      const resp = await FileApi.getFiles(this.query)
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
      this.initFiles()
    },

    // 翻页
    handleCurrentChange(val) {
      this.query.current_page = val
      this.initFiles()
    }
  }
}
</script>
<style>
  .el-notification {
    min-width: 360px;
  }
  .el-notification.right {
    top: 5% !important;
    left: 50% !important;
    transform: translate(-50%, -50%) !important;
  }
  .el-notification__content {
    text-align: left !important;
  }
</style>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.page {
  float: right;
  margin-top: 10px;
  margin-bottom: 30px;
}
</style>
