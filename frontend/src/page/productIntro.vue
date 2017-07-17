<template>
  <div class="manage_page fillcontain">
  <headSecond></headSecond>
    <el-row style="height: 100%;">
      <el-col :span="4"  style="min-height: 100%; background-color: #324057;">
      <el-menu theme="dark" style="min-height: 100%;" default-active="defaultActive" class="el-menu-vertical-demo" router>

        <el-menu-item index="productIntro"><i class="el-icon-menu"></i>首页</el-menu-item>

          <el-submenu index="1">
            <template slot="title"><i class="el-icon-document"></i>全部</template>
            <el-menu-item-group>
              <template slot="title">金融</template>
              <el-menu-item index="/option1">
                图表1                
                <el-button type="primary" size="mini" @click="toggle($event)"><i class="el-icon-plus"></i>
                </el-button>
              </el-menu-item>
              <el-menu-item index="/option1">
              图表2
              <el-button type="danger" size="mini"><i class="el-icon-minus "></i>
              </el-button>

              </el-menu-item>
            </el-menu-item-group>
          </el-submenu>

          <el-submenu index="2">
            <template slot="title"><i class="el-icon-menu"></i>金融</template>
            <el-submenu index="2-1">
              <template slot="title">期货一号</template>
              <el-menu-item index="/option1">
                期权1号
                <el-button type="primary" size="mini" @click="toggle($event)"><i class="el-icon-plus"></i></el-button>
              </el-menu-item>
              <el-menu-item index="2-1-2">期权2号</el-menu-item>
              <el-menu-item index="2-1-3">期权3号</el-menu-item>
            </el-submenu>
            <el-submenu index="3-1">
              <template slot="title">期货三号</template>

              <el-menu-item >期权1号</el-menu-item>
              <el-menu-item >期权2号

              <el-button type="primary" size="large">
              </el-button>

              </el-menu-item>
              <el-menu-item index="3-1-3">期权3号</el-menu-item>
            </el-submenu>
          </el-submenu>
        </el-menu>
      </el-col>

      <el-col :span="20" style="height: 1500px;overflow-x: hidden;overflow-y: auto; ">
        <transition name="slide">
          <router-view></router-view>
        </transition>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { hasClass, removeClass, addClass } from "../util.js"
import headSecond from '../components/headSecond'
import Bus from '../bus'

	export default{

    components:{
      headSecond
    },

    methods:{
      toggle: function(e) {
        var btn = e.currentTarget;
        if (hasClass(btn, 'el-button--primary')) { // 添加，加号变减号
          removeClass(btn, 'el-button--primary');
          addClass(btn, 'el-button--danger');
          removeClass(btn.children[0].children[0], 'el-icon-plus');
          addClass(btn.children[0].children[0], 'el-icon-minus');
          var future = btn.parentNode.parentNode.parentNode.children[0].innerText.trim();
          var option = btn.parentNode.innerText.trim();
          var optionObj = {'future': future, 'option': option};
          Bus.$emit('addNewOption', optionObj);
        } else {
          removeClass(btn, 'el-button--danger');
          addClass(btn, 'el-button--primary');
          removeClass(btn.children[0].children[0], 'el-icon-minus');
          addClass(btn.children[0].children[0], 'el-icon-plus');
        } 
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

button span i {
  margin-left: 10px
}

</style>