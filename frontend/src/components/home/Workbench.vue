<template>
  <div class="workbench">
    <div style="padding-bottom: 20px; height: 30px;">
      <span class="span-left">
        <h4 class="page-title">工作台</h4>
      </span>
      <span class="span-breadcrumb">
        <el-breadcrumb separator="/">
          <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
          <el-breadcrumb-item>工作台</el-breadcrumb-item>
        </el-breadcrumb>
      </span>
    </div>
    <!-- <div style="width: 100%; height: 170px;">
      <span class="span-card">
        <el-card>
          <i class="el-icon-date" /> 周执行
          <el-divider class="divider-card"></el-divider>
          <h3>153 次</h3>
        </el-card>
      </span>
      <span class="span-card">
        <el-card><i class="el-icon-document-checked" /> 今日执行
          <el-divider class="divider-card"></el-divider>
          <h3>15 次</h3>
        </el-card>
      </span>
      <span class="span-card">
        <el-card><i class="el-icon-finished" /> 成功率
          <el-divider class="divider-card"></el-divider>
          <h3>80 %</h3>
        </el-card>
      </span>
      <span class="span-card">
        <el-card><i class="el-icon-timer" /> 平均耗时
          <el-divider class="divider-card"></el-divider>
          <h3>200 S</h3>
        </el-card>
      </span>
      <span class="span-card">
        <el-card><i class="el-icon-s-data" /> 用例数
          <el-divider class="divider-card"></el-divider>
          <h3>1249 个</h3>
        </el-card>
      </span>
      <span class="span-card-end">
        <el-card><i class="el-icon-s-order" /> 任务数
          <el-divider class="divider-card"></el-divider>
          <h3>3249 个</h3>
        </el-card>
      </span>
    </div> -->
    <div class="cards">
      <div class="left-cards" style="margin-bottom: 30px;">
        <el-card>
          <div slot="header" class="clearfix" style="text-align: left;">
            <span class="cart-title">我的压测任务</span>
            <span style="float: right;">
              <el-popover trigger="click" popper-class="home-popover">
                <el-button slot="reference" type="button" icon="el-icon-s-grid" size="small"></el-button>
                <el-checkbox :indeterminate="casesIsIndeterminate" v-model="casesCheckAll" @change="casesHandleCheckAllChange">全选</el-checkbox>
                <el-checkbox-group v-model="casesFilter" @change="casesHandleCheckedChange">
                  <el-checkbox v-for="item in casesOptions" :key="item" :label="item" style="display:block;">{{ item }}</el-checkbox>
                </el-checkbox-group>
              </el-popover>
            </span>
          </div>
          <el-table ref="cases-table" v-loading="loading" :data="casesData" stripe style="width: 100%">
            <el-table-column prop="name" label="名称" min-width="100" show-overflow-tooltip v-if="showCasesColumn('名称')"></el-table-column>
            <el-table-column prop="type" label="类型" min-width="80" v-if="showCasesColumn('类型')">
              <template slot-scope="scope">
                <span v-if="scope.row.type === true"><el-tag class="tag-create" size="mini">手动创建</el-tag></span>
                <span v-else ><el-tag class="tag-auto" size="mini">自动生成</el-tag></span>
              </template>
            </el-table-column>
            <el-table-column prop="team_name" label="团队" min-width="120" show-overflow-tooltip v-if="showCasesColumn('团队')"> </el-table-column>
            <el-table-column prop="env_name" label="环境" min-width="80" v-if="showCasesColumn('环境')"> </el-table-column>
            <el-table-column prop="status" label="状态" v-if="showCasesColumn('状态')">
              <template slot-scope="scope">
                <el-tag size="mini">{{ scope.row.status }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="thread_group.target_concurrency" label="目标并发" v-if="showCasesColumn('目标并发')">
              <template slot-scope="scope">
                <div style="height: 40px;line-height: 40px;display: flex;">
                  <span style='overflow:hidden;text-overflow:ellipsis;white-space: nowrap;' v-show="!scope.row.edit_concurrency">{{scope.row.thread_group.target_concurrency}}</span>
                  <el-input :ref='"valueinput"+scope.$index'
                            @blur="concurrencyBlur(scope.$index,scope.row)"
                            @keyup.enter.native="$event.target.blur"
                            v-show="scope.row.edit_concurrency"
                            size="small"
                            class="cell-edit"
                            oninput="value=value.replace(/[^\d]/g,'')"
                            v-model="scope.row.thread_group.target_concurrency"
                            placeholder="Input">
                  </el-input>
                  <el-button class='edit-button' icon="el-icon-edit" size="mini"
                             v-show="!scope.row.edit_concurrency"
                             @click="changeConcurrency(scope.$index,scope.row)">
                  </el-button>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="thread_group.hold_target_rate_time" label="持续时间" v-if="showCasesColumn('持续时间')">
              <template slot-scope="scope">
                <div @dblclick="changeRatetime(scope.$index,scope.row)" style="height: 40px;line-height: 40px;display: flex;">
                  <span style='overflow:hidden;text-overflow:ellipsis;white-space: nowrap;' v-show="!scope.row.edit_ratetime">{{scope.row.thread_group.hold_target_rate_time}}</span>
                  <el-input :ref='"valueinput"+scope.$index'
                            @blur="ratetimeBlur(scope.$index,scope.row)"
                            @keyup.enter.native="$event.target.blur"
                            v-show="scope.row.edit_ratetime"
                            size="small"
                            class="cell-edit"
                            v-model="scope.row.thread_group.hold_target_rate_time"
                            placeholder="Input">
                  </el-input>
                  <el-button class='edit-button' icon="el-icon-edit" size="mini"
                             v-show="!scope.row.edit_ratetime"
                             @click="changeRatetime(scope.$index,scope.row)">
                  </el-button>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="user_name" label="创建人" min-width="120" v-if="showCasesColumn('创建人')"> </el-table-column>
            <el-table-column prop="create_time" label="创建时间" min-width="140" v-if="showCasesColumn('创建时间')"></el-table-column>
            <el-table-column prop="update_time" label="更新时间" min-width="140" v-if="showCasesColumn('更新时间')"></el-table-column>
            <el-table-column label="操作" align="center" min-width="160" v-if="showCasesColumn('操作')">
              <template slot-scope="scope">
                <el-button cy-data="run-case" type="text" size="mini" @click="runingCase(scope.row)">执行</el-button>
                <el-button cy-data="edit-case" type="text" size="mini" @click="showEdit(scope.row)">编辑</el-button>
                <el-button cy-data="delete-case" type="text" size="mini" @click="deleteCase(scope.row)">删除</el-button>
                <el-button cy-data="show-case" type="text" size="mini" @click="showDetails(scope.row)">详情</el-button>
              </template>
            </el-table-column>
            <el-table-column label="报告" align="center" min-width="80" v-if="showCasesColumn('报告')">
              <template slot-scope="scope">
                <router-link type="primary" :to="{path:'/report', name:'Reports', params: { case: scope.row.id }}">
                  <el-button cy-data="link-to-report" type="text" size="mini">查看报告</el-button>
                </router-link>
              </template>
            </el-table-column>
          </el-table>
          <!-- 分页功能 -->
          <div class="page">
            <el-pagination
            @size-change="(val) => handleSizeChange(val,'cases')"
            @current-change="(val) => handleCurrentChange(val,'cases')"
            :current-page="caseQuery.current_page"
            :page-sizes="[5, 10, 15]"
            :page-size="caseQuery.page_size"
            layout="total, sizes, prev, pager, next"
            :total="casesTotal">
            </el-pagination>
          </div>
        </el-card>
      </div>
      <div class="right-cards" style="margin-bottom: 30px;">
        <el-card>
          <div slot="header" class="clearfix" style="text-align: left;">
            <span class="cart-title">我的压测报告</span>
            <span style="float: right;">
              <el-popover trigger="click" popper-class="home-popover">
                <el-button slot="reference" type="button" icon="el-icon-s-grid" size="small"></el-button>
                <el-checkbox :indeterminate="reportsIsIndeterminate" v-model="reportsCheckAll" @change="reportsHandleCheckAllChange">全选</el-checkbox>
                <el-checkbox-group v-model="reportsFilter" @change="reportsHandleCheckedChange">
                  <el-checkbox v-for="item in reportsOptions" :key="item" :label="item" style="display:block;">{{ item }}</el-checkbox>
                </el-checkbox-group>
              </el-popover>
            </span>
          </div>
          <el-table ref="reports-table" v-loading="loading" :data="reportsData" stripe style="width: 100%" :default-sort = "{prop: 'create_time', order: 'descending'}">
            <el-table-column prop="name" label="名称" min-width="120" show-overflow-tooltip v-if="showReportsColumn('名称')"> </el-table-column>
            <el-table-column prop="status" label="状态" min-width="100" v-if="showReportsColumn('状态')">
              <template slot-scope="scope">
                <el-tag size="mini">{{ scope.row.status }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="case_name" label="用例名称" min-width="120" show-overflow-tooltip v-if="showReportsColumn('用例名称')"> </el-table-column>
            <el-table-column prop="thread_group.target_concurrency" label="并发目标" v-if="showReportsColumn('并发目标')"> </el-table-column>
            <el-table-column prop="user_name" label="执行人" min-width="120" v-if="showReportsColumn('执行人')"> </el-table-column>
            <el-table-column prop="create_time" label="执行时间" min-width="140" v-if="showReportsColumn('执行时间')"> </el-table-column>
            <el-table-column label="操作" align="center" min-width="160" v-if="showReportsColumn('操作')">
              <template slot-scope="scope">
                <el-button id="editReport" type="text" size="mini" @click="showReportdetails(scope.row)">详情</el-button>
                <el-button id="deleteReport" type="text" size="mini" @click="deleteReport(scope.row)">删除</el-button>
                <el-button id="handleExport" type="text" size="mini" @click="handleExport(scope.row)">下载</el-button>
                <el-button id="stopReport" type="text" size="small" @click="stopRunning(scope.row)">停止</el-button>
              </template>
            </el-table-column>
          </el-table>
          <!-- 分页功能 -->
          <div class="page">
            <el-pagination
            @size-change="(val) => handleSizeChange(val,'report')"
            @current-change="(val) => handleCurrentChange(val,'report')"
            :current-page="reportQuery.current_page"
            :page-sizes="[5, 10, 15]"
            :page-size="reportQuery.page_size"
            layout="total, sizes, prev, pager, next"
            :total="reportTotal">
            </el-pagination>
          </div>
        </el-card>
      </div>
      <div class="left-cards" style="margin-bottom: 30px;">
        <el-card>
          <div slot="header" class="clearfix" style="text-align: left;">
            <span class="cart-title">团队排期</span>
          </div>
          <el-table :data="scheduleData" stripe style="width: 100%">
            <el-table-column prop="name" label="名称" width="120"> </el-table-column>
            <el-table-column prop="team_name" label="团队" width="100"> </el-table-column>
            <el-table-column prop="user_name" label="创建人" min-width="120"> </el-table-column>
            <el-table-column prop="start_time" label="排期开始" min-width="140"> </el-table-column>
            <el-table-column prop="end_time" label="排期结束" min-width="140"> </el-table-column>
          </el-table>
          <!-- 分页功能 -->
          <div class="page">
            <el-pagination
            @size-change="(val) => handleSizeChange(val,'schedule')"
            @current-change="(val) => handleCurrentChange(val,'schedule')"
            :current-page="scheduleQuery.current_page"
            :page-sizes="[5, 10, 15]"
            :page-size="scheduleQuery.page_size"
            layout="total, sizes, prev, pager, next"
            :total="scheduleTotal">
            </el-pagination>
          </div>
        </el-card>
      </div>
      <div class="right-cards" style="margin-bottom: 30px;">
        <el-card>
          <div slot="header" class="clearfix" style="text-align: left;">
            <span class="cart-title">测试日历</span>
          </div>
          <calendar-heatmap id='heatmap' :values="colorDate" :end-date="endDate" :range-color="colorRange"/>
        </el-card>
      </div>
    </div>
    <!-- 编辑/查看用例 -->
    <div class="case-create" v-if="caseShow">
      <CasePageDialog :type="pageType" :caseId="caseId" @cancel="cancelCase"></CasePageDialog>
    </div>
    <!-- 报告详情 -->
    <div class="case-details" v-if="reportShow">
      <DetailsPageDialog :reportId="reportId" @cancel="cancelReport"></DetailsPageDialog>
    </div>
    <ReportExport v-if="showReportExport" id="testReportExport" :reportId="reportId"></ReportExport>
  </div>
</template>

<script>
import { CalendarHeatmap } from 'vue-calendar-heatmap'
import HomeApi from '../../request/homepage'
import CaseApi from '../../request/case'
import ReportApi from '../../request/report'
import CasePageDialog from '../case/CasePageDialog'
import DetailsPageDialog from '../report/DetailsPageDialog'
import ReportExport from '../report/ReportExport'
import html2canvas from 'html2canvas'
import { exportPdf } from '../../assets/js/file-download.js'

export default {
  name: 'Workbench',
  components: { CalendarHeatmap, CasePageDialog, DetailsPageDialog, ReportExport },
  data() {
    return {
      loading: true,
      caseShow: false,
      reportShow: false,
      showReportExport: false,
      colorDate: [],
      endDate: new Date().getTime() + 7 * 24 * 60 * 60 * 1000,
      colorRange: ['#eef2f7', '#9efae0', '#6df8d0', '#3cf6c1', '#0cf3b1'],
      scheduleData: [],
      casesData: [],
      reportsData: [],
      casesCheckAll: false,
      reportsCheckAll: false,
      casesIsIndeterminate: true,
      reportsIsIndeterminate: true,
      caseQuery: {
        current_page: 1,
        page_size: 5
      },
      reportQuery: {
        current_page: 1,
        page_size: 5
      },
      scheduleQuery: {
        current_page: 1,
        page_size: 5
      },
      casesTotal: 0,
      reportTotal: 0,
      scheduleTotal: 0,
      casesOptions: ['名称', '类型', '团队', '环境', '状态', '目标并发', '持续时间', '创建人', '创建时间', '更新时间', '操作', '报告'],
      casesFilter: ['名称', '目标并发', '持续时间', '操作', '报告'],
      reportsOptions: ['名称', '状态', '用例名称', '并发目标', '执行人', '执行时间', '操作'],
      reportsFilter: ['名称', '状态', '用例名称', '并发目标', '操作']
    }
  },

  mounted() {
    this.initCases()
    this.initReport()
    this.initCalendar()
    this.initSchedule()
  },

  methods: {
    // 初始化首页用例列表
    async initCases() {
      const resp = await HomeApi.getCases(this.caseQuery)
      if (resp.success === true) {
        this.casesData = resp.result.data
        this.casesTotal = resp.result.item_count
      } else {
        this.$message.error(resp.error.message)
      }
      this.loading = false
    },
    // 初始化首页报告列表
    async initReport() {
      const resp = await HomeApi.getReports(this.reportQuery)
      if (resp.success === true) {
        this.reportsData = resp.result.data
        this.reportTotal = resp.result.item_count
      } else {
        this.$message.error(resp.error.message)
      }
      this.loading = false
    },
    // 初始化排期数据
    async initSchedule() {
      const resp = await HomeApi.getTasks(this.scheduleQuery)
      if (resp.success === true) {
        this.scheduleData = resp.result.data
        this.scheduleTotal = resp.result.item_count
      } else {
        this.$message.error(resp.error.message)
      }
    },

    // 初始化日历数据
    async initCalendar() {
      const resp = await HomeApi.getCalendar()
      if (resp.success === true) {
        this.colorDate = resp.result
      } else {
        this.$message.error(resp.error.message)
      }
    },

    // 改变每页显示数量
    handleSizeChange(val, type) {
      if (type === 'cases') {
        this.caseQuery.page_size = val
        this.initCases()
      } else if (type === 'report') {
        this.reportQuery.page_size = val
        this.initReport()
      } else if (type === 'schedule') {
        this.scheduleQuery.page_size = val
        this.initSchedule()
      }
    },

    // 翻页
    handleCurrentChange(val, type) {
      if (type === 'cases') {
        this.caseQuery.current_page = val
        this.initCases()
      } else if (type === 'report') {
        this.reportQuery.current_page = val
        this.initReport()
      } else if (type === 'schedule') {
        this.scheduleQuery.current_page = val
        this.initSchedule()
      }
    },
    // 编辑目标并发值
    changeConcurrency(index, row) {
      this.casesData[index].edit_concurrency = !this.casesData[index].edit_concurrency
      this.casesData = [...this.casesData];
      setTimeout(() => {
        this.$refs['valueinput' + index].focus()
        // 缓存目标并发修改前的值
        this.concurrencyTemp = row.thread_group.target_concurrency
      }, 1)
    },

    // 编辑持续时间值
    changeRatetime(index, row) {
      this.casesData[index].edit_ratetime = !this.casesData[index].edit_ratetime
      this.casesData = [...this.casesData];
      setTimeout(() => {
        this.$refs['valueinput' + index].focus()
        // 缓存持续时间修改前的值
        this.ratetimeTemp = row.thread_group.hold_target_rate_time
      }, 1)
    },

    // 目标并发的失焦保存
    async concurrencyBlur(index, row) {
      this.caseId = row.id
      this.casesData[index].edit_concurrency = !this.casesData[index].edit_concurrency
      this.casesData = [...this.casesData];
      // 判断值是否有变化，有变化时更新
      if (this.concurrencyTemp !== this.casesData[index].thread_group.target_concurrency) {
        const resp = await CaseApi.getCase(this.caseId)
        if (resp.success === true) {
          this.form = resp.result
          this.form.thread_group.target_concurrency = parseInt(this.casesData[index].thread_group.target_concurrency)
          CaseApi.updateCase(this.form).then(resp => {
            if (resp.success === true) {
              this.$message({
                message: '更新成功！',
                type: 'success'
              })
              this.cancelCase()
            } else {
              this.$message.error(resp.error.message)
            }
          })
        }
      }
    },

    // 持续时间的失焦保存
    async ratetimeBlur(index, row) {
      this.caseId = row.id
      this.casesData[index].edit_ratetime = !this.casesData[index].edit_ratetime
      this.casesData = [...this.casesData];
      // 判断值是否有变化，有变化时更新
      if (this.ratetimeTemp !== this.casesData[index].thread_group.hold_target_rate_time) {
        const resp = await CaseApi.getCase(this.caseId)
        if (resp.success === true) {
          this.form = resp.result
          this.form.thread_group.hold_target_rate_time = parseInt(this.casesData[index].thread_group.hold_target_rate_time)
          CaseApi.updateCase(this.form).then(resp => {
            if (resp.success === true) {
              this.$message({
                message: '更新成功！',
                type: 'success'
              })
              this.cancelCase()
            } else {
              this.$message.error(resp.error.message)
            }
          })
        }
      }
    },

    // 用例表选择展示列
    casesHandleCheckAllChange(val) {
      this.$nextTick(() => {
        this.casesFilter = val ? this.casesOptions : [];
        this.casesIsIndeterminate = false;
        this.$refs['cases-table'].doLayout();
      })
    },
    casesHandleCheckedChange(value) {
      this.$nextTick(() => {
        const checkedCount = value.length;
        this.casesCheckAll = checkedCount === this.casesOptions.length;
        this.casesIsIndeterminate = checkedCount > 0 && checkedCount < this.casesOptions.length;
        this.$refs['cases-table'].doLayout();
      })
    },

    // 报告表选择展示列
    reportsHandleCheckAllChange(val) {
      this.$nextTick(() => {
        this.reportsFilter = val ? this.reportsOptions : [];
        this.reportsIsIndeterminate = false;
        this.$refs['reports-table'].doLayout();
      })
    },
    reportsHandleCheckedChange(value) {
      this.$nextTick(() => {
        const checkedCount = value.length;
        this.reportsCheckAll = checkedCount === this.reportsOptions.length;
        this.reportsIsIndeterminate = checkedCount > 0 && checkedCount < this.reportsOptions.length;
        this.$refs['reports-table'].doLayout();
      })
    },

    // 用例表列是否显示
    showCasesColumn(val) {
      if (this.casesFilter.includes(val)) {
        return true
      }
      return false
    },

    // 报告表列是否显示
    showReportsColumn(val) {
      if (this.reportsFilter.includes(val)) {
        return true
      }
      return false
    },

    // 显示用例编辑弹窗
    showEdit(row) {
      this.caseId = row.id
      this.pageType = 'edit'
      this.caseShow = true
    },

    // 显示用例详情弹窗
    showDetails(row) {
      this.caseId = row.id
      this.pageType = 'edtails'
      this.caseShow = true
    },

    // 关闭用例弹窗
    cancelCase() {
      this.caseShow = false
      this.initCases()
    },

    // 执行测试
    runingCase(row) {
      this.$confirm('确认要执行用例？', { type: 'warning' })
        .then(_ => {
          console.log('执行确认', _)
          this.loading = true
          CaseApi.runCase(row.id).then(resp => {
            if (resp.success === true) {
              this.$message({
                message: '执行成功！',
                type: 'success'
              })
              this.initCases()
            } else {
              this.$message.error(resp.error.message)
            }
            this.loading = false
          })
        })
        .catch(_ => {
          console.log('执行取消', _)
        })
    },

    // 删除用例
    deleteCase(row) {
      this.$confirm('确认要删除用例？', { type: 'warning' })
        .then(_ => {
          console.log('删除确认', _)
          CaseApi.deleteCase(row.id).then(resp => {
            if (resp.success === true) {
              this.$message({
                message: '删除成功！',
                type: 'success'
              })
              // 删除最后一页的最后一条数据时能成功跳转回最后一页的上一页
              const totalPage = Math.ceil((this.casesTotal - 1) / this.caseQuery.page_size) // 总页数
              this.caseQuery.current_page = this.caseQuery.current_page > totalPage ? totalPage : this.caseQuery.current_page
              this.caseQuery.current_page = this.caseQuery.current_page < 1 ? 1 : this.caseQuery.current_page
              this.initCases()
            } else {
              this.$message.error(resp.error.message)
            }
          })
        })
        .catch(_ => {
          console.log('删除取消', _)
        })
    },

    // 显示报告详情
    showReportdetails(row) {
      this.reportId = row.id
      this.title = '报告详情'
      this.reportShow = true
    },

    // 关闭报告详情组件
    cancelReport() {
      this.reportShow = false
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
              // 删除最后一页的最后一条数据时能成功跳转回最后一页的上一页
              const totalPage = Math.ceil((this.reportTotal - 1) / this.reportQuery.page_size) // 总页数
              this.reportQuery.current_page = this.reportQuery.current_page > totalPage ? totalPage : this.reportQuery.current_page
              this.reportQuery.current_page = this.reportQuery.current_page < 1 ? 1 : this.reportQuery.current_page
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
    }
  }
}
</script>

<style>
.el-popover.home-popover {
  width: 70px;
  min-width: auto;
}
</style>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin-bottom: 0px;
}
.span-card {
  float: left;
  margin-right: 2%;
  width: 15%;
}
.span-card-end {
  float: left;
  width: 15%;
}
.divider-card {
  margin-top: 12px;
  margin-right: 0px;
  margin-bottom: 12px;
  margin-left: 0px;
}
.cart-title {
  font-size: 16px;
  font-weight: 600;
}
.page {
  float: right;
  margin-top: 10px;
  margin-bottom: 30px;
}
.cards{
  display:flex;
  flex-direction:row;
  flex-wrap:wrap;
  height:calc(100vh - 100px);
  margin-bottom: 50px;
}
.left-cards {
  margin-right: 1%;
  height: 50%;
  width: 49%;
}
.right-cards {
  height: 50%;
  width: 50%;
}
.el-card {
  height: 100%;
  position:relative;
}
.el-card /deep/ .el-card__body{
  padding-top: 0px;
  padding-right: 20px;
  padding-bottom: 20px;
  padding-left: 20px;
  height: calc(100% - 40px);
}
.el-table {
  height: calc(100% - 80px);
  width: 99.9%;
  overflow-y: auto;
  cursor:pointer;
  font-size: 12px;
}
.el-table::before {
  display: none;
}
::v-deep .cell-edit input {
  background-color: transparent;
  height: 20px;
  line-height: 20px;
}
::v-deep .el-checkbox__label {
  font-size: 12px;
}
.edit-button {
  border: none;
  box-shadow: 0 0 0 0 rgba(114, 124, 245, 0.5);
  background: unset;
  padding: 7px 7px;
}
.tag-auto {
  background-color: #0acf97!important;
  color: #fff;
  font-weight:900;
  border-style:none !important;
}
.tag-create {
  background-color: #fa5c7c!important;
  color: #fff!important;
  font-weight:900;
  border-style:none !important;
}
</style>
