<!--
/**
* @module components
* @author huzhiheng
* @date 2021年1月21日
* @desc 编辑产线环境实例
*/
-->
<template>
  <div id="env-edit">
    <el-dialog :visible.sync="dialogVisible" @close="cancelEnv()" width="600px">
      <div slot="title" class="common-title">
        实例编辑
      </div>
      <div class="env-dialog-content">
        <el-form ref="form" :model="form" :rules="rules" label-width="100px">
          <el-form-item label="施压机数量" prop="jmeter_params">
            <el-input v-model="form.jmeter_params"></el-input>
            <div class="hint">
              施压机最大并发数: {{ form.jmeter_params }} x 1000
            </div>
          </el-form-item>
          <el-form-item label="备注">
            <el-input type="textarea" :rows="3" v-model="form.describe"></el-input>
          </el-form-item>
        </el-form>
      </div>
      <span slot="footer" v-if="isEdit == false">
        <el-button @click="cancelEnv()">取消</el-button>
        <el-button type="primary" @click="saveEnv('form')">保存</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import EnvApi from '../../../request/environment'

export default {
  name: 'envDialog',
  props: ['envId'],
  data() {
    return {
      dialogVisible: true,
      form: {
        id: 0,
        jmeter_params: '',
        describe: ''
      },
      rules: {
        jmeter_params: [
          { required: true, message: '请输入实例数量', trigger: 'blur' }
        ]
      },
      isEdit: false
    }
  },

  mounted() {
    this.form.id = this.envId
    this.initEnv()
  },

  methods: {
    // 获取项目信息
    async initEnv() {
      const resp = await EnvApi.getEnv(this.envId)
      if (resp.success === true) {
        this.form = resp.result
      } else {
        this.$message.error(resp.error.message)
      }
    },

    // 关闭弹窗
    cancelEnv() {
      this.$emit('cancel', {})
    },

    // 保存环境
    async saveEnv(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          EnvApi.updateEnv(this.form).then(resp => {
            if (resp.success === true) {
              this.$message({
                message: '更新成功！',
                type: 'success'
              })
              this.cancelEnv()
            } else {
              this.$message.error(resp.error.message)
            }
          })
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
.env-dialog-content {
  padding-right: 50px;
  text-align: left;
  font-size: 14px;
}

.hint {
  background-color: #e7faf5;
  color: #0ACF97;
  padding: 0px 16px;
}
</style>
