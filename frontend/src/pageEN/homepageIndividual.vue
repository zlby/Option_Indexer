<template>
  <div class="manage_page fillcontain">
    <el-row style="height: 100%; min-width:200px">
      <el-col :span="5"  style="min-height: 100%; background-color: #324057;min-width:200px">
        <el-menu theme="dark" style="height: 100%;" default-active="defaultActive" class="el-menu-vertical-demo" router>

          <el-menu-item index="/en/homepageIndividual"><i class="el-icon-menu"></i>Personal Info</el-menu-item>
          <el-menu-item index="/en/homepageIndividual/list"><i class="el-icon-menu"></i>Subscribe List</el-menu-item>
          <el-menu-item index="/en/homepageIndividual/infoReminder"><i class="el-icon-menu"></i>Notification</el-menu-item>

        </el-menu>
      </el-col>

      <el-col :span="19" style="height: 100%;overflow-y: auto; background-color: #E8E8E8;">
          <router-view ></router-view>
      </el-col>
    </el-row>
  </div>
</template>

<script>
  import headSecond from '../componentsEN/headSecond'

  export default{

    data:function(){

      return{

      }
    },


    components:{
      headSecond
    },

    methods:{

    }

  }


</script>

<style lang="less" scoped>

  @import '../style/common';

  .el-button {

}

button span i {
  margin-left: 10px
}
 .add-btn{
  positon:relative;
  // top:10px;
  // right:0px;
  float: right;
  margin-right:20px;
 }
 .el-menu-item{
  padding-right:0px;
  position:relative;
  white-space: normal;
 }
</style>
