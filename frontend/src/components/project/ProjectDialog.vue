<!--
/**
* @module components
* @author huzhiheng
* @date 2021年1月8日
* @desc 创建/编辑/查看项目组件
*/
-->
<template>
  <div id="project-dialog">
    <el-dialog :visible.sync="dialogVisible" @close="cancelProject()" width="600px">
      <div slot="title" class="common-title">
        {{ dialogTitle }}
      </div>
      <div class="project-dialog-content">
        <el-form ref="form" :model="form" :rules="rules" label-width="110px">
          <el-form-item label="Orion项目ID" prop="orion_id">
            <el-input cy-data="orion-id" v-model="form.orion_id" placeholder="请输入orion项目ID查询" style="width: 86%"></el-input>
            <el-button type="primary" icon="el-icon-search"></el-button>
          </el-form-item>
          <el-form-item label="名称" prop="name">
            <el-input cy-data="project-name" v-model="form.name" placeholder="请输入项目名称"></el-input>
          </el-form-item>
          <el-form-item label="备注">
            <el-input cy-data="project-desc" type="textarea" v-model="form.describe"></el-input>
          </el-form-item>
        </el-form>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button cy-data="cancel-button" @click="cancelProject()">取消</el-button>
        <el-button cy-data="save-button" v-loading.fullscreen.lock="loading" type="primary" @click="saveProject('form')">保存</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import ProjectApi from '../../request/project'

export default {
  name: 'projectDialog',
  props: ['type', 'projectId'],
  data() {
    return {
      dialogVisible: true,
      loading: false,
      dialogTitle: '',
      form: {
        id: 0,
        orion_id: '',
        name: '',
        describe: ''
      },
      rules: {
        orion_id: [
          { required: true, message: '请输入orion项目ID查询', trigger: 'blur' }
        ],
        name: [
          { required: true, message: '请输入项目名称', trigger: 'blur' }
        ]
      }
    }
  },

  mounted() {
    if (this.type === 'create') {
      this.dialogTitle = '创建项目'
    } else if (this.type === 'edit') {
      this.dialogTitle = '编辑项目'
      this.initProject()
    }
  },

  methods: {
    // 获取项目信息
    async initProject() {
      const resp = await ProjectApi.getProject(this.projectId)
      if (resp.success === true) {
        this.form = resp.result
      } else {
        this.$message.error(resp.error.message)
      }
    },

    // 关闭弹窗
    cancelProject() {
      this.form.id = 0
      this.form.orion_id = ''
      this.form.name = ''
      this.form.describe = ''
      this.$emit('cancel', {})
    },

    // 保存项目
    async saveProject(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          this.loading = true
          if (this.type === 'create') {
            ProjectApi.createProject(this.form).then(resp => {
              if (resp.success === true) {
                this.$message({
                  message: '创建成功！',
                  type: 'success'
                })
                this.cancelProject()
              } else {
                this.$message.error(resp.error.message)
              }
            })
          } else if (this.type === 'edit') {
            ProjectApi.updateProject(this.form).then(resp => {
              if (resp.success === true) {
                this.$message({
                  message: '更新成功！',
                  type: 'success'
                })
                this.cancelProject()
              } else {
                this.$message.error(resp.error.message)
              }
            })
          }
          this.loading = false
        } else {
          this.$message.error('必传字段为空!!')
          return false
        }
      })
    }
  }
}
</script>

<style>
.project-dialog-content {
  padding-right: 50px;
  text-align: left;
  font-size: 14px;
}
</style>
