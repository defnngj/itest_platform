<!--
/**
* @module components
* @author huzhiheng
* @date 2021年1月8日
* @desc 日期组件
*/
-->
<template>
  <div class="calendar">
    <div style="padding-bottom: 20px; height: 30px;">
      <span class="span-left">
        <h4 class="page-title">日程安排</h4>
      </span>
      <span class="span-breadcrumb">
        <el-breadcrumb separator="/">
          <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
          <el-breadcrumb-item>日程安排</el-breadcrumb-item>
        </el-breadcrumb>
      </span>
    </div>
    <el-card class="main-card">
      <FullCalendar defaultView="dayGridMonth" :options="calendarOptions" />
      <el-dialog title="任务" :visible.sync="dialogVisible" width="38%" :before-close="taskClose">
        <el-form ref="form" :model="form" :rules="rules" :label-position="labelPosition" label-width="60px">
          <el-form-item label="名称" prop="name">
            <el-input cy-data="task-name" v-model="form.name"></el-input>
          </el-form-item>
          <el-form-item label="团队" prop="team">
            <el-select cy-data="team" v-model="form.team" filterable placeholder="请选择团队">
              <el-option cy-data="team-list" v-for="item in teamOptions" :key="item.value" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="时间">
            <el-time-select cy-data="start-time" placeholder="起始时间" v-model="show_start_time" :picker-options="{
                start: '00:00',
                step: '00:30',
                end: '24:00'
              }">
            </el-time-select>
            <el-time-select cy-data="end-time" placeholder="结束时间" v-model="show_end_time" :picker-options="{
                start: '00:30',
                step: '00:30',
                end: '24:00',
                minTime: show_start_time
              }">
            </el-time-select>
          </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
          <el-button cy-data="delete-task" v-show="this.editTask.status != false" type="danger" @click="deleteTask()">删除</el-button>
          <el-button cy-data="save-task" type="primary" @click="saveTask('form')">保存</el-button>
        </span>
      </el-dialog>
    </el-card>
  </div>
</template>

<script>
import FullCalendar from '@fullcalendar/vue'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import listPlugin from '@fullcalendar/list'
import interactionPlugin from '@fullcalendar/interaction'
import zhLocale from '@fullcalendar/core/locales/zh-cn'
import CalendarApi from '../../request/scheduling'
import TeamApi from '../../request/team'
import {
  stringToTimestamp,
  timestampToString
} from '../../assets/js/datetime-utils'

export default {
  name: 'Calendar',
  props: {
    msg: String
  },
  components: {
    FullCalendar
  },
  data() {
    return {
      dialogVisible: false,
      query: {
        start_date: '',
        end_date: ''
      },
      calendarOptions: {
        plugins: [dayGridPlugin, timeGridPlugin, listPlugin, interactionPlugin],
        initialView: 'dayGridMonth',
        locale: zhLocale,
        displayEventEnd: true,
        dateClick: this.handleDateClick,
        eventClick: this.showTask,
        datesSet: this.handleDates,
        headerToolbar: {
          left: 'prev,next today',
          center: 'title',
          right: 'listMonth,dayGridMonth,timeGridWeek'
        },
        events: []
      },
      show_start_time: '',
      show_end_time: '',
      save_date: '',
      form: {
        id: '',
        name: '',
        team: '',
        start_time: '',
        end_time: ''
      },
      rules: {
        name: [{ required: true, message: '请输入任务名称', trigger: 'blur' }],
        team: [{ required: true, message: '请选择团队', trigger: 'blur' }]
      },
      teamOptions: [],
      labelPosition: 'right',
      editTask: {
        status: false, // 编辑任务标记
        id: ''
      }
    }
  },

  mounted() {
    this.initTeam()
  },

  methods: {
    // 监测数据标签切换
    handleDates(dateInfo) {
      const startFormat = dateInfo.startStr.slice(0, 10) + ' 00:00:00'
      const endFormat = dateInfo.endStr.slice(0, 10) + ' 00:00:00'
      if (
        startFormat !== this.query.start_date &&
        endFormat !== this.query.end_date
      ) {
        this.query.start_date = startFormat
        this.query.end_date = endFormat
        this.initTask()
      }
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

    // 初始化任务
    async initTask() {
      const resp = await CalendarApi.getTasks(this.query)
      if (resp.success === true) {
        const data = resp.result
        this.calendarOptions.events = []
        for (const i in data) {
          this.calendarOptions.events.push({
            id: data[i].id,
            title: data[i].name + ' - ' + data[i].user_name,
            start: data[i].start_time,
            end: data[i].end_time,
            backgroundColor: data[i].color
          })
        }
      } else {
        this.$message.error(resp.error.message)
      }
    },

    // 点击日期添加任务
    handleDateClick(arg) {
      const dateSTR = arg.dateStr
      // 月模式，添加任务 dateSTR: 2021-01-06
      if (dateSTR.length === 10) {
        this.show_start_time = '10:00'
        this.show_end_time = '11:00'
        this.save_date = dateSTR
      }
      // 周模式，添加任务 dateSTR:2021-01-14T06:30:00+08:00
      if (dateSTR.length === 25) {
        this.save_date = dateSTR.slice(0, 10)
        this.show_start_time = dateSTR.slice(11, 16)
        const dateTime = dateSTR.slice(0, 10) + ' ' + dateSTR.slice(11, 19)
        const timestamp = stringToTimestamp(dateTime)
        const dataString = timestampToString(timestamp + 3600 * 1000)
        this.show_end_time = dataString.slice(11, 16)
      }
      this.dialogVisible = true
    },

    // 查看任务
    async showTask(taskInfo) {
      this.editTask.status = true
      this.editTask.id = taskInfo.event._def.publicId
      const resp = await CalendarApi.getTaskInfo(this.editTask.id)
      if (resp.success === true) {
        this.dialogVisible = true
        const result = resp.result
        this.form.name = result.name
        this.form.team = result.team
        this.save_date = result.start_time.slice(0, 10)
        this.show_start_time = result.start_time.slice(11, 16)
        this.show_end_time = result.end_time.slice(11, 16)
      } else {
        this.$message.error(resp.error.message)
      }
    },

    // 关闭任务窗口
    taskClose(done) {
      done()
      this.cleanForm()
      this.editTask.status = false
    },

    // 保存任务
    saveTask(formName) {
      this.form.start_time = this.save_date + ' ' + this.show_start_time + ':00'
      this.form.end_time = this.save_date + ' ' + this.show_end_time + ':00'
      this.$refs[formName].validate(valid => {
        if (valid) {
          if (this.editTask.status === false) {
            CalendarApi.createTask(this.form).then(resp => {
              if (resp.success === true) {
                this.dialogVisible = false
                this.$message({
                  message: '保存成功！',
                  type: 'success'
                })
                this.editTask.status = false
                this.initTask()
              } else {
                this.$message.error(resp.error.message)
                return
              }
            })
          } else {
            this.form.id = this.editTask.id
            CalendarApi.updateTask(this.form).then(resp => {
              if (resp.success === true) {
                this.dialogVisible = false
                this.$message({
                  message: '保存成功！',
                  type: 'success'
                })
                this.editTask.status = false
                this.initTask()
              } else {
                this.$message.error(resp.error.message)
                return
              }
            })
          }
        } else {
          this.$message.error('必传字段为空!!')
          return false
        }
        this.cleanForm()
      })
    },

    // 删除任务
    deleteTask() {
      this.$confirm('确认要删除任务？')
        .then(_ => {
          console.log('删除确认', _)
          this.dialogVisible = false
          CalendarApi.deleteTask(this.editTask.id).then(resp => {
            if (resp.success === true) {
              this.$message({
                message: '删除成功！',
                type: 'success'
              })
            } else {
              this.$message.error(resp.error.message)
            }
            this.cleanForm()
            this.editTask.status = false
            this.initTask()
          })
        })
        .catch(_ => {
          console.log('删除取消', _)
        })
    },

    // 清空form
    cleanForm() {
      this.form.name = ''
      this.form.team = ''
      this.form.start_time = ''
      this.show_end_time = ''
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
.fc .fc-toolbar.fc-header-toolbar {
  height: 30px;
}

.el-main {
  line-height: 30px;
}

.el-date-editor.el-input,
.el-date-editor.el-input__inner {
  width: 50% !important;
}

.el-form-item__content .el-select {
  width: 100%;
}

.fc .fc-button-primary {
  background-color: #727cf5 !important;
  border-color: #727cf5;
  box-shadow: 0 2px 6px 0 rgb(114 124 245 / 50%);
}

.fc .fc-button-primary:disabled {
  border-color: #727cf5;
}

.fc .fc-button-primary:hover {
  border-color: #5763eb;
}

.fc .fc-button-primary:not(:disabled).fc-button-active {
  background-color: #4250f2 !important;
  border-color: #4250f2;
}

.fc-button .fc-button-primary {
  box-shadow: 0 2px 6px 0 rgb(114 124 245 / 50%);
}
</style>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
/deep/.el-dialog{
  display: flex;
  flex-direction: column;
  margin:0 !important;
  position:absolute;
  top:50%;
  left:50%;
  transform:translate(-50%,-50%);
  /*height:600px;*/
  height:40%;
  max-width:calc(100% - 360px);
}
</style>
