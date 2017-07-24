<template>
  <div class="manage_page fillcontain">
      <headSecond></headSecond>
    <el-row style="height: 100%; min-width:200px">
      <el-col :span="4"  style="min-height: 100%; background-color: #324057;min-width:200px">
        <el-menu theme="dark" style="height: 100%;" default-active="defaultActive" class="el-menu-vertical-demo">

          <el-menu-item index="/homepageSecond"><i class="el-icon-menu"></i>首页</el-menu-item>

          <el-submenu index="2">
            <template slot="title"><i class="el-icon-menu"></i>金融</template>
            <el-submenu :index="key" v-for="(value,key,index) in items">
              <template slot="title">{{key}}</template>

              <el-menu-item :index="ite" v-for="(ite, index2) in value" v-if="ite!='-'" class="menu-item">
                {{ite}}
                <div class="add-btn">
                <el-button type="primary" size="mini" @click="toggle($event)"><i class="el-icon-plus" ></i></el-button>
                </div>
              </el-menu-item>
              
            </el-submenu>

          </el-submenu>
        </el-menu>
      </el-col>
      <el-col :span="20" style="height: 100%;overflow-x: hidden;overflow-y: auto; background-color: #E8E8E8;">
      <keep-alive>
          <router-view ></router-view>
      </keep-alive>
      </el-col>
    </el-row>
  </div>
</template>

<script>
  import { hasClass, removeClass, addClass } from "../util.js"
  import headSecond from '../components/headSecond'
  import Bus from '../bus'

  export default{
    created:function(){
      Bus.$on("getData", data => {
        this.items=data
      })
    },
    data:function(){

      return{
        items:{}
      }
    },


    components:{
      headSecond
    },
    methods:{
      toggle: function(e) {
        var btn = e.currentTarget;
        var future = btn.parentNode.parentNode.parentNode.parentNode.children[0].innerText.trim();
        var option = btn.parentNode.parentNode.innerText.trim();
        var optionObj = {'future': future, 'option': option};
          
        if (hasClass(btn, 'el-button--primary')) { // 添加，加号变减号
          removeClass(btn, 'el-button--primary');
          addClass(btn, 'el-button--danger');
          removeClass(btn.children[0].children[0], 'el-icon-plus');
          addClass(btn.children[0].children[0], 'el-icon-minus');
          Bus.$emit('addNewOption', optionObj);
          console.log(optionObj);
        } else {
          removeClass(btn, 'el-button--danger');
          addClass(btn, 'el-button--primary');
          removeClass(btn.children[0].children[0], 'el-icon-minus');
          addClass(btn.children[0].children[0], 'el-icon-plus');
          Bus.$emit('removeOption', optionObj);
        }
        e.stopPropagation();
      },
      prevent: function(e) {
        e.stopPropagation();
        return false;
      }
    }

  }


</script>

<style lang="less" scoped>

  @import '../style/common';

  .el-button {
  //float: right;
  //margin-top: 10px;
}
 .el-icon-menu{
  font-family:"YAHEI"
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
 .menu-item{
  font-size: 16px;
 }
</style>