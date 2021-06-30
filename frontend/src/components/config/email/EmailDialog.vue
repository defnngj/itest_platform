<!--
/**
* @module components
* @author huzhiheng
* @date 2021年1月8日
* @desc 创建/编辑/查看项目组件
*/
-->
<template>
  <div id="email-dialog">
    <el-dialog :visible.sync="dialogVisible" @close="cancelEmail()" width="600px">
      <div slot="title" class="common-title">
        {{ dialogTitle }}
      </div>
      <div class="dialog-content">
        <el-form ref="form" :model="form" :rules="rules" label-width="100px">
          <el-form-item label="名称" prop="name">
            <el-input cy-data="name" v-model="form.name"></el-input>
          </el-form-item>
          <el-form-item label="发送邮件" prop="mail_to">
            <el-select cy-data="select-email" v-model="form.mail_to" filterable multiple placeholder="请选择用户邮件">
              <el-option cy-data="email-list" v-for="item in email.options" :key="item.value" :label="item.label" :value="item.value">
                <span style="float: left">{{ item.label }}</span>
                <span style="float: right; color: #8492a6; font-size: 13px">{{ item.email }}</span>
              </el-option>
            </el-select>
          </el-form-item>
        </el-form>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button cy-data="cancel-button" @click="cancelEmail()">取消</el-button>
        <el-button cy-data="save-button" type="primary" @click="saveEmail('form')">保存</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import EmailApi from '../../../request/email'
import UserApi from '../../../request/user'

export default {
  name: 'emailDialog',
  props: ['type', 'emailId'],
  data() {
    return {
      dialogVisible: true,
      dialogTitle: '',
      form: {
        id: 0,
        name: '',
        mail_to: ''
      },
      rules: {
        email_name: [
          { required: true, message: '请输入项目名称', trigger: 'blur' }
        ]
      },
      email: {
        options: [],
        loading: false
      }
    }
  },

  mounted() {
    this.initUser()
    if (this.type === 'create') {
      this.dialogTitle = '创建邮件分组'
    } else if (this.type === 'edit') {
      this.dialogTitle = '编辑邮件分组'
      this.initEmail()
    }
  },

  methods: {
    // 初始化用户列表
    async initUser() {
      const resp = await UserApi.getUsers()
      if (resp.success === true) {
        const data = resp.result
        for (const i in data) {
          this.email.options.push({
            value: data[i].id,
            label: data[i].name,
            email: data[i].email
          })
        }
      } else {
        this.$message.error(resp.error.message)
      }
    },

    // 获取项目信息
    async initEmail() {
      const resp = await EmailApi.getEmail(this.emailId)
      if (resp.success === true) {
        this.form = resp.result
      } else {
        this.$message.error(resp.error.message)
      }
    },

    // 关闭弹窗
    cancelEmail() {
      this.form.id = 0
      this.form.name = ''
      this.form.mail_to = ''
      this.$emit('cancel', {})
    },

    // 保存邮件分组
    async saveEmail(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          if (this.type === 'create') {
            EmailApi.createEmail(this.form).then(resp => {
              if (resp.success === true) {
                this.$message({
                  message: '创建成功！',
                  type: 'success'
                })
                this.cancelEmail()
              } else {
                this.$message.error(resp.error.message)
              }
            })
          } else if (this.type === 'edit') {
            EmailApi.updateEmail(this.form).then(resp => {
              if (resp.success === true) {
                this.$message({
                  message: '更新成功！',
                  type: 'success'
                })
                this.cancelEmail()
              } else {
                this.$message.error(resp.error.message)
              }
            })
          }
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
.dialog-content {
  padding-right: 50px;
  text-align: left;
  font-size: 14px;
}
</style>
