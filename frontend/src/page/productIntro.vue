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
                选项1                 
              <el-button type="primary" size="mini"><i class="el-icon-plus" style="margin-left : 10px"></i>
              </el-button>
              </el-menu-item>
              <el-menu-item index="/option1">
              选项2
              <el-button type="danger" size="mini"><i class="el-icon-minus " style="margin-left : 10px"></i>
              </el-button>

              </el-menu-item>
            </el-menu-item-group>
            <el-menu-item-group title="分组2">
              <el-menu-item index="1-3">选项3</el-menu-item>
            </el-menu-item-group>
            <el-submenu index="1-4">
              <template slot="title">选项4</template>
              <el-menu-item index="1-4-1">选项1</el-menu-item>
            </el-submenu>
          </el-submenu>

          <el-submenu index="2">
            <template slot="title"><i class="el-icon-menu"></i>金融</template>
            <el-submenu index="2-1">
              <template slot="title">期货一号</template>
              <el-menu-item index="">期权1号</el-menu-item>
              <el-menu-item index="2-1-2">期权2号</el-menu-item>
              <el-menu-item index="2-1-3">期权3号</el-menu-item>
            </el-submenu>
            <el-submenu index="3-1">
              <template slot="title">期货三号</template>
              <el-menu-item index="3-1-1">期权1号</el-menu-item>
              <el-menu-item index="3-1-2">期权2号</el-menu-item>
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

  import headSecond from '../components/headSecond'
	export default{

    components:{
      headSecond
    },

		data(){
			return{
		}

	}
}

</script>

<style lang="less" scoped>

@import '../style/common';

.el-button {
  margin-left:120px;
}


</style>