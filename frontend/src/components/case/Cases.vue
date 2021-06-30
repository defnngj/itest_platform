<!--
/**
* @module components
* @author huzhiheng
* @date 2021年1月8日
* @desc 项目列表组件
*/
-->
<template>
  <div class="cases">
    <div style="padding-bottom: 20px; height: 30px;">
      <span class="span-left">
        <h4 class="page-title">用例管理</h4>
      </span>
      <span class="span-breadcrumb">
        <el-breadcrumb separator="/">
          <span v-if="ListShow">
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>用例管理</el-breadcrumb-item>
          </span>
        </el-breadcrumb>
      </span>
    </div>
    <el-card class="main-card">
        <div style="padding-bottom: 20px; height: 45px;">
          <span class="span-right">
            <el-button cy-data="search-button" type="primary" @click="searchCase">搜索</el-button>
          </span>
          <span class="span-right">
            <el-input cy-data="search-keyword" v-model="query.keyword" placeholder="请输入关键字搜索" clearable></el-input>
          </span>
          <span class="span-left">
            <el-dropdown @command="createClick">
              <el-button cy-data="create-case" type="primary">
                创建<i class="el-icon-arrow-down el-icon--right"></i>
              </el-button>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item cy-data="automatic" command="automatic">自动生成</el-dropdown-item>
                <el-dropdown-item cy-data="manual" command="manual">手动创建</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </span>
          <span class="span-right">
            <el-select cy-data="team" v-model="query.team" filterable clearable placeholder="请选择团队名称">
              <el-option cy-data="team-list" v-for="item in teamOptions" :key="item.value" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </span>
        </div>
        <el-table v-loading="loading" :data="tableData" style="width: 100%">
          <el-table-column prop="name" label="名称" min-width="120px"></el-table-column>
          <el-table-column prop="type" label="类型">
            <template slot-scope="scope">
              <span v-if="scope.row.type === true"><el-tag class="tag-create" size='small'>手动创建</el-tag></span>
              <span v-else ><el-tag class="tag-auto" size='small'>自动生成</el-tag></span>
            </template>
          </el-table-column>
          <el-table-column prop="team_name" label="团队" min-width="120px"></el-table-column>
          <el-table-column prop="env_name" label="环境"></el-table-column>
          <el-table-column prop="status" label="状态">
            <template slot-scope="scope">
              <el-tag size='mini'>{{ scope.row.status }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="thread_group.target_concurrency" label="目标并发" min-width='100px'>
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
          <el-table-column prop="thread_group.hold_target_rate_time" label="持续时间" min-width='100px'>
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
          <el-table-column prop="user_name" label="创建人" min-width="100"></el-table-column>
          <el-table-column prop="create_time" label="创建时间" min-width="150"> </el-table-column>
          <el-table-column prop="update_time" label="更新时间" min-width="150"> </el-table-column>
          <el-table-column fixed="right" label="操作" min-width="100">
            <template slot-scope="scope">
              <span>
                <el-button cy-data="run-case" type="text" size="small" @click="runingCase(scope.row)">执行</el-button>
                <el-button cy-data="edit-case" type="text" size="small" @click="showEdit(scope.row)">编辑</el-button>
              </span> <br>
              <span>
                <el-button cy-data="delete-case" type="text" size="small" @click="deleteCase(scope.row)">删除</el-button>
                <el-button cy-data="show-case" type="text" size="small" @click="showDetails(scope.row)">详情</el-button>
              </span>
            </template>
          </el-table-column>
          <el-table-column fixed="right" label="报告" min-width="70">
            <template slot-scope="scope">
              <router-link type="primary" :to="{path:'/report', name:'Reports', params: { case: scope.row.id }}">
                <el-button cy-data="link-to-report" type="text" size="small">查看报告</el-button>
              </router-link>
            </template>
          </el-table-column>
        </el-table>
        <!-- 分页功能 -->
        <div class="page">
          <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="query.current_page" :page-sizes="[10, 20, 50]" :page-size="query.page_size" layout="total, sizes, prev, pager, next" :total="total">
          </el-pagination>
        </div>
    </el-card>

    <!-- 创建用例 -->
    <div class="case-create" v-if="caseShow">
      <CasePageDialog :type="pageType" :caseId="caseId" @cancel="cancelCase"></CasePageDialog>
    </div>
    <!-- 自动创建 -->
    <div class="case-create" v-if="autoShow">
      <AutoPageDialog :caseId="caseId" @cancel="cancelCase"></AutoPageDialog>
    </div>

  </div>
</template>

<script>
import CaseApi from '../../request/case'
import TeamApi from '../../request/team'
import CasePageDialog from './CasePageDialog.vue'
import AutoPageDialog from './AutoPageDialog.vue'

export default {
  components: { CasePageDialog, AutoPageDialog },
  data() {
    return {
      dialogType: '创建用例',
      loading: true,
      ListShow: true,
      caseShow: false,
      autoShow: false,
      pageType: 'create',
      caseId: 0,
      tableData: [],
      projectOptions: [],
      teamOptions: [],
      query: {
        current_page: 1,
        page_size: 10,
        team: '',
        keyword: ''
      },
      total: 0,
      form: {
        name: '',
        team: '',
        describe: '',
        env: '',
        monitor_list: [],
        email_list: [],
        host: '',
        assertion: 'success',
        slave_count: '',
        thread_group: {
          target_concurrency: '',
          ramp_up_time: '',
          ramp_up_steps_count: '',
          hold_target_rate_time: ''
        },
        file_info: [],
        branch: []
      }
    }
  },

  mounted() {
    this.initTeam()
    // 从项目列表跳转过来，自动带上项目名称搜索
    if (typeof this.$route.params.project !== undefined) {
      this.query.project = this.$route.params.project
    }
    this.initCases()
  },

  methods: {
    // 初始化用例列表
    async initCases() {
      const resp = await CaseApi.getCases(this.query)
      if (resp.success === true) {
        this.tableData = resp.result.data
        this.total = resp.result.item_count
      } else {
        this.$message.error(resp.error.message)
      }
      this.loading = false
    },

    // 初始化团队列表
    async initTeam() {
      const resp = await TeamApi.getTeams()
      if (resp.success === true) {
        const data = resp.result.data
        for (const i in data) {
          this.teamOptions.push({
            value: data[i].id,
            label: data[i].name
          })
        }
      } else {
        this.$message.error(resp.error.message)
      }
    },

    // 显示创建弹窗
    showCreate() {
      this.title = '创建用例'
      this.pageType = 'create'
      this.ListShow = false
      this.caseShow = true
    },

    // 创建用例
    createClick(command) {
      this.title = '创建用例'
      this.pageType = 'create'
      if (command === 'manual') {
        this.ListShow = true
        this.caseShow = true
      } else if (command === 'automatic') {
        this.ListShow = true
        this.autoShow = true
      }
    },

    // 编辑目标并发值
    changeConcurrency(index, row) {
      this.tableData[index].edit_concurrency = !this.tableData[index].edit_concurrency
      this.tableData = [...this.tableData];
      setTimeout(() => {
        this.$refs['valueinput' + index].focus()
        // 缓存目标并发修改前的值
        this.concurrencyTemp = row.thread_group.target_concurrency
      }, 1)
    },

    // 编辑持续时间值
    changeRatetime(index, row) {
      this.tableData[index].edit_ratetime = !this.tableData[index].edit_ratetime
      this.tableData = [...this.tableData];
      setTimeout(() => {
        this.$refs['valueinput' + index].focus()
        // 缓存持续时间修改前的值
        this.ratetimeTemp = row.thread_group.hold_target_rate_time
      }, 1)
    },

    // 目标并发的失焦保存
    async concurrencyBlur(index, row) {
      this.caseId = row.id
      this.tableData[index].edit_concurrency = !this.tableData[index].edit_concurrency
      this.tableData = [...this.tableData];
      // 判断值是否有变化，有变化时更新
      if (this.concurrencyTemp !== this.tableData[index].thread_group.target_concurrency) {
        const resp = await CaseApi.getCase(this.caseId)
        if (resp.success === true) {
          this.form = resp.result
          this.form.thread_group.target_concurrency = parseInt(this.tableData[index].thread_group.target_concurrency)
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
      this.tableData[index].edit_ratetime = !this.tableData[index].edit_ratetime
      this.tableData = [...this.tableData];
      // 判断值是否有变化，有变化时更新
      if (this.ratetimeTemp !== this.tableData[index].thread_group.hold_target_rate_time) {
        const resp = await CaseApi.getCase(this.caseId)
        if (resp.success === true) {
          this.form = resp.result
          this.form.thread_group.hold_target_rate_time = parseInt(this.tableData[index].thread_group.hold_target_rate_time)
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
    // 显示用例列表
    showList() {
      this.title = '用例管理'
      this.ListShow = true
      this.caseShow = false
      this.autoShow = false
    },

    // 显示编辑
    // showEdit(row) {
    //   this.caseId = row.id
    //   this.pageType = 'edit'
    //   this.title = '编辑用例'
    //   this.ListShow = false
    //   this.caseShow = true
    // },

    // 显示编辑弹窗
    showEdit(row) {
      this.caseId = row.id
      this.pageType = 'edit'
      this.ListShow = true
      this.caseShow = true
    },

    // 显示详情弹窗
    showDetails(row) {
      this.caseId = row.id
      this.pageType = 'edtails'
      this.ListShow = true
      this.caseShow = true
    },

    // 关闭创建/编辑用例组件
    cancelCase() {
      this.ListShow = true
      this.caseShow = false
      this.autoShow = false
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

    // 搜索用例
    async searchCase() {
      const resp = await CaseApi.getCases(this.query)
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
      this.initCases()
    },

    // 翻页
    handleCurrentChange(val) {
      this.query.current_page = val
      this.initCases()
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
.edit-button {
  border: none;
  box-shadow: 0 0 0 0 rgba(114, 124, 245, 0.5);
  background: unset;
  padding: 7px 7px;
}

::v-deep .cell-edit input {
  /* border: none; */
  background-color: transparent;
  padding: 10px
}

::v-deep input::-ms-input-placeholder {
    text-align: center;
}

::v-deep input::-webkit-input-placeholder {
    text-align: center;
}

</style>
