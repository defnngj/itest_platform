<!--
/**
* @module components
* @author lu.Lin
* @date 2021年4月25日
* @desc 文件详情组件
*/
-->
<template>
  <div id="file-details-dialog">
    <el-dialog :visible.sync="dialogVisible" @close="cancelFile()" width="calc(100vw - 360px)">
      <div slot="title" class="common-title">
        文件详情
      </div>
      <div class="file-content" v-loading="loading" element-loading-text="拼命加载中" element-loading-spinner="el-icon-loading">
        <pre v-highlightjs="xmlString"><code></code></pre>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import FileApi from '../../request/file'
import vkbeautify from 'vkbeautify'

export default {
  name: 'file-details',
  props: ['fileName'],
  data() {
    return {
      dialogVisible: true,
      loading: true,
      xmlString: ''
    }
  },

  mounted() {
    this.initFileDetail()
  },

  methods: {
    // 初始化xml文件
    initFileDetail() {
      this.$nextTick(() => {
        FileApi.getFile(this.fileName).then(resp => {
          if (resp.success === true) {
            const xmlFile = resp.result
            this.loading = false
            this.xmlString = vkbeautify.xml(xmlFile)
          } else {
            this.loading = false
            this.$message.error(resp.error.message)
          }
        })
      })
    },

    cancelFile() {
    // 关闭弹窗
      this.xmlString = ''
      this.$emit('cancel', {})
    }
  }
}
</script>

<style>
.charts-line {
  margin-top: 30px;
  height: auto;
  overflow: auto;
}

.report-button {
  float: right;
  margin-left: 10px !important;
}

.el-dialog{
  display: flex;
  flex-direction: column;
  margin:0 !important;
  position:absolute;
  top:50%;
  left:50%;
  transform:translate(-50%,-50%);
  /*height:600px;*/
  height:calc(100% - 120px);
  max-width:calc(100% - 360px);
}

.file-content {
  text-align: left;
  box-shadow: 1px 1px 5px 5px #eef2f7;
  margin-bottom: 30px;
  min-height:calc(100% - 60px);
}
</style>
