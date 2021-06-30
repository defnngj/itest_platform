<!--
/**
* @module components
* @author huzhiheng
* @date 2021年1月27日
* @desc 报告列表组件
*/
-->
<template>
  <div class="reports" v-loading="downloadLoading">
    <div style="padding-bottom: 20px; height: 30px;">
      <span class="span-left">
        <h4 class="page-title" v-if="ListShow">报告管理</h4>
        <!-- <h4 class="page-title" v-if="detailsShow">{{ title }}</h4> -->
      </span>
      <span class="span-breadcrumb">
        <el-breadcrumb separator="/">
          <span v-if="ListShow">
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>报告管理</el-breadcrumb-item>
          </span>
        </el-breadcrumb>
      </span>
    </div>
    <div v-if="ListShow">
      <el-card class="main-card">
        <div style="padding-bottom: 20px; height: 45px;">
          <span class="span-right">
            <el-button type="primary" @click="searchReport">搜索</el-button>
          </span>
          <span class="span-right">
            <el-input v-model="query.keyword" placeholder="请输入关键字额" clearable></el-input>
          </span>
          <span class="span-right">
            <el-select v-model="query.case" filterable clearable placeholder="请选择用例名称">
              <el-option v-for="item in caseOptions" :key="item.value" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </span>
          <span class="span-right">
            <el-popover trigger="click" popper-class="report-popover">
                <el-button slot="reference" type="button" icon="el-icon-s-grid"></el-button>
                <el-radio-group v-model="query.tag" @change='filterReport'>
                  <el-radio :label="''">全部</el-radio>
                  <el-radio :label="'Important'">星标</el-radio>
                  <el-radio :label="'Normal'">非星标</el-radio>
                </el-radio-group>
              </el-popover>
          </span>
        </div>
        <el-table v-loading="loading" :data="tableData" style="width: 100%">
          <el-table-column prop="name" label="名称"> </el-table-column>
          <el-table-column prop="status" label="状态">
            <template slot-scope="scope">
              <el-tag size='small'>{{ scope.row.status }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="case_name" label="用例名称"> </el-table-column>
          <el-table-column prop="thread_group.target_concurrency" label="并发目标"> </el-table-column>
          <el-table-column prop="user_name" label="执行人"> </el-table-column>
          <el-table-column prop="create_time" label="执行时间" min-width="150"> </el-table-column>
          <el-table-column fixed="right" label="操作" min-width="80">
            <template slot-scope="scope">
              <span>
                <el-button id="editReport" type="text" size="small" @click="showDetails(scope.row)">详情</el-button>
                <el-button id="stopReport" type="text" size="small" @click="stopRunning(scope.row)">停止</el-button>
              </span> <br>
              <span>
                <el-button id="handleExport" type="text" size="small" @click="handleExport(scope.row)">下载</el-button>
                <el-button id="deleteReport" type="text" size="small" @click="deleteReport(scope.row)">删除</el-button>
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="tag" fixed="right" label="星标" min-width="50">
            <template slot-scope="scope">
              <span v-if="scope.row.tag === 'Important'">
                <i class="el-icon-star-on" style='color: #ffcd5d; font-size: 18px' @click="isFavorite(scope.row,'Normal')"></i>
              </span>
              <span v-else><i class="el-icon-star-off" @click="isFavorite(scope.row,'Important')"></i></span>
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

    <!-- 报告详情 -->
    <div class="case-details" v-if="detailsShow">
      <DetailsPageDialog :reportId="reportId" @cancel="cancelReport"></DetailsPageDialog>
    </div>
    <ReportExport v-if="showReportExport" id="testReportExport" :reportId="reportId"></ReportExport>
  </div>
</template>

<script>
import ReportApi from '../../request/report'
import CaseApi from '../../request/case'
import DetailsPageDialog from './DetailsPageDialog'
import ReportExport from './ReportExport'
import { exportPdf } from '../../assets/js/file-download.js'
import html2canvas from 'html2canvas'

export default {
  components: { DetailsPageDialog, ReportExport },
  data() {
    return {
      title: '报告详情',
      loading: true,
      downloadLoading: false,
      showReportExport: false,
      reportId: 0,
      ListShow: true,
      detailsShow: false,
      tableData: [],
      caseOptions: [],
      query: {
        current_page: 1,
        page_size: 10,
        case: '',
        keyword: '',
        tag: ''
      },
      total: 0
    }
  },

  mounted() {
    this.initCase()
    // 从用例列表跳转过来，自动带上用例名称搜索
    if (typeof this.$route.params.case !== undefined) {
      this.query.case = this.$route.params.case
    }
    this.initReport()
  },

  methods: {
    // 初始化报告列表
    async initReport() {
      const resp = await ReportApi.getReports(this.query)
      if (resp.success === true) {
        this.tableData = resp.result.data
        this.total = resp.result.item_count
      } else {
        this.$message.error(resp.error.message)
      }
      this.loading = false
    },

    // 初始化用例
    async initCase() {
      const query = {
        current_page: 1,
        page_size: 1000,
        keyword: ''
      }
      const resp = await CaseApi.getCases(query)
      if (resp.success === true) {
        const data = resp.result.data
        for (const i in data) {
          this.caseOptions.push({
            value: data[i].id,
            label: data[i].name
          })
        }
      } else {
        this.$message.error(resp.error.message)
      }
    },

    // 显示详情
    showDetails(row) {
      this.reportId = row.id
      this.title = '报告详情'
      this.ListShow = true
      this.detailsShow = true
    },

    // 关闭报告详情组件
    cancelReport() {
      this.ListShow = true
      this.detailsShow = false
    },

    // 显示报告列表
    showList() {
      this.title = '报告管理'
      this.ListShow = true
      this.detailsShow = false
    },

    // 删除报告
    deleteReport(row) {
      this.$confirm('确认要删除报告？', { type: 'warning' })
        .then(_ => {
          console.log('删除确认', _)
          ReportApi.deleteReport(row.id).then(resp => {
            if (resp.success === true) {
              this.$message({
                message: '删除成功！',
                type: 'success'
              })
              this.initReport()
            } else {
              this.$message.error(resp.error.message)
            }
          })
        })
        .catch(_ => {
          console.log('删除取消', _)
        })
    },

    // 下载报告
    handleExport(row) {
      if (row.status === 'Running') {
        this.$message.error('报告正在运行中！')
        return
      }
      this.reportId = row.id
      const name = row.name
      this.downloadLoading = true
      this.showReportExport = true
      const reset = this.exportReportReset

      this.$nextTick(function() {
        setTimeout(() => {
          html2canvas(document.getElementById('testReportExport'), {
            scale: 2
          }).then(function(canvas) {
            exportPdf(name, [canvas]);
            reset()
          });
        }, 2000);
      });
    },

    exportReportReset() {
      this.showReportExport = false
      this.downloadLoading = false
    },

    // 停止运行报告
    async stopRunning(row) {
      this.loading = true
      this.reportId = row.id
      const resp = await ReportApi.stopReport(this.reportId)
      if (resp.success === true) {
        this.$message({
          message: '已停止运行！',
          type: 'success'
        })
      } else {
        this.$message.error(resp.error.message)
      }
      this.loading = false
    },

    // 搜索报告
    async searchReport() {
      this.loading = true
      const resp = await ReportApi.getReports(this.query)
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
    async filterReport() {
      this.loading = true
      const resp = await ReportApi.getReports(this.query)
      if (resp.success === true) {
        this.tableData = resp.result.data
        this.total = resp.result.item_count
        this.$message({
          message: '筛选完成！',
          type: 'success'
        })
      } else {
        this.$message.error(resp.error.message)
      }
      this.loading = false
    },

    // 标记报告
    async isFavorite(row, str) {
      this.reportId = row.id
      ReportApi.tagReport({ id: row.id, tag: str }).then(resp => {
        if (resp.success === true) {
          this.$message({
            message: '标记成功！',
            type: 'success'
          })
          this.initReport()
        } else {
          this.$message.error(resp.error.message)
        }
      })
    },

    // 改变每页显示数量
    handleSizeChange(val) {
      this.query.page_size = val
      this.initReport()
    },

    // 翻页
    handleCurrentChange(val) {
      this.query.current_page = val
      this.initReport()
    }
  }
}
</script>
<style>
.el-popover.report-popover {
  width: 70px;
  min-width: auto;
}
</style>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.page {
  float: right;
  margin-top: 10px;
  margin-bottom: 30px;
}
.el-icon-star-off:hover
{
  color: #ffcd5d;
}

</style>
