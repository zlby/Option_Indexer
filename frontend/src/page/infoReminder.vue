<template>
<div class="infoborder">
  <el-alert
    title="系统通知"
    type="success"
    :closable="false"
    class="infotitle">
  </el-alert>
  <el-alert
    title="成功提示的文案"
    type="info"
    description="文字说明文字说明文字说明文字说明文字说明文字说明"
    :closable="false"
    class="info">
  </el-alert>
  <el-alert
    title="消息提示的文案"
    type="info"
    description="文字说明文字说明文字说明文字说明文字说明文字说明"
    :closable="false"
    class="info">
  </el-alert>
  <el-alert
    title="警告提示的文案"
    type="info"
    description="文字说明文字说明文字说明文字说明文字说明文字说明"
    :closable="false"
    class="info">
  </el-alert>
  <el-alert
    title="错误提示的文案"
    type="info"
    description="文字说明文字说明文字说明文字说明文字说明文字说明"
    :closable="false"
    class="info">
  </el-alert>
</div>
</template>


<script>
  export default{

  }


</script>

<style lang="less" scoped>

  @import '../style/common';
.info{
  margin-top: 15px;
  padding: 20px;
}
.infotitle{
  margin-top: 10px;
}

.infoborder{
  margin-left: 10px;
  margin-right: 10px;
}
</style>