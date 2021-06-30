<!--
/**
* @module components
* @author lu.Lin
* @date 2021年5月06日
* @desc 更新通知组件
*/
-->
<template>
  <div id="notification-dialog">
    <el-dialog
      :visible.sync="dialogVisible"
      @close="cancelNotification()"
      width="65vw">
      <div slot="title" class="common-title">
        更新日志
      </div>
      <div class="markdown-body" v-loading="loading" element-loading-text="拼命加载中" element-loading-spinner="el-icon-loading">
        <VueMarkdown :source="mdData"></VueMarkdown>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import VueMarkdown from 'vue-markdown';
import axios from 'axios'

export default {
  name: 'notification-dialog',
  props: [''],
  components: { VueMarkdown },
  data() {
    return {
      dialogVisible: true,
      loading: true,
      mdData: ''
    }
  },

  mounted() {
    this.getMarkdown()
  },
  methods: {
    async getMarkdown() {
      const url = '/update/UPDATE.md';
      axios.get(url).then(response => {
        this.mdData = response.data;
        this.loading = false
      });
    },
    cancelNotification() {
      this.$emit('cancel', {})
    }
  }
}
</script>

<style scoped>

/deep/ .el-dialog__header {
  border-bottom: 1px solid #e5e5e5;
}
::v-deep .el-dialog__body {
  padding: 0 20px 30px;
}
.markdown-body {
  text-align: left;
}

</style>
