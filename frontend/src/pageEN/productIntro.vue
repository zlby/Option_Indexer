<template>
  <div class="manage_page fillcontain">
    <el-row style="height: 100%; min-width:200px">
      <el-col :span="5"  style="height: 100%; background-color: #324057;overflow-y:scroll;">
        <el-menu theme="dark" style="height: 100%;min-width:230px;" default-active="defaultActive" class="el-menu-vertical-demo">


          <el-submenu index="2">
            <template slot="title"><i class="el-icon-menu"></i>Options list</template>
            <el-submenu :index="key" v-for="(value,key,index) in items">
              <template slot="title">{{key}}</template>

              <el-menu-item :index="ite" v-for="(ite, index2) in value" v-if="ite!='-'" class="menu-item">
                {{ite}}
                <div class="add-btn">
                <el-button type="primary" size="mini" @click="toggle($event)"><i class="el-icon-plus" ></i>
                </el-button>
                </div>
              </el-menu-item>

            </el-submenu>

          </el-submenu>
        </el-menu>
      </el-col>
      <el-col :span="19" style="height: 100%;overflow-x: hidden;overflow-y: auto; background-color: #E8E8E8;">
      <keep-alive>
          <router-view ></router-view>
      </keep-alive>
      </el-col>
    </el-row>
  </div>
</template>

<script>
  import { hasClass, removeClass, addClass } from "../util.js"
  import headSecond from '../componentsEN/headSecond'
  import Bus from '../bus'

  export default{
    created:function(){
      Bus.$on("getData", data => {
        this.items=data
      })
      Bus.$on("resetAllBtn",function(){
        var btnSet=document.getElementsByClassName("el-button--danger");
        if(btnSet.length==0){
          return ;
        }
        for(;;){
            var btn=btnSet[0];
            removeClass(btn, 'el-button--danger');
            addClass(btn, 'el-button--primary');
            removeClass(btn.children[0].children[0], 'el-icon-minus');
            addClass(btn.children[0].children[0], 'el-icon-plus');
            if(btnSet.length==0){
              break;
            }
        }
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


 /*定义滚动条宽高及背景，宽高分别对应横竖滚动条的尺寸*/
::-webkit-scrollbar{
    width: 5px;
    background-color: #f5f5f5;
}
/*定义滚动条的轨道，内阴影及圆角*/
::-webkit-scrollbar-track{
    -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,.3);
    width:5px;
    background-color: #fff;
}
/*定义滑块，内阴影及圆角*/
::-webkit-scrollbar-thumb{
    /*width: 10px;*/
    height: 5px;
    border-radius: 2px;
    width:5px;
    -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,.3);
    background-color: #555;
}
</style>
