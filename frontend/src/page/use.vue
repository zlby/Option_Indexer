<template>
	<div>
		<section class="Collapse">
			<el-row>
				<el-col :span="16" :offset="2">
					<el-card class="box-card">
						<div slot="header" class="clearfix">
							<span style="line-height: 36px;">产品使用</span>
							<el-button style="float: right;" type="primary">操作按钮</el-button>
						</div>


						<el-table
						:data="tableData"
						style="width: 100%">
						<el-table-column
						prop="date"
						label="日期"
						width="180">
					</el-table-column>
					<el-table-column
					prop="name"
					label="姓名"
					width="180">
				</el-table-column>
				<el-table-column
				prop="address"
				label="地址">
			</el-table-column>
		</el-table>
		<br><br>
		<el-form ref="form" :model="form" label-width="80px">
			<el-form-item label="期权选择">
				<el-select v-model="form.region" placeholder="请选择期权">
					<el-option label="期权1" value="shanghai"></el-option>
					<el-option label="期权2" value="beijing"></el-option>
				</el-select>
			</el-form-item>
			<el-form-item label="价格">
				<el-col :span="11">
					<el-input placeholder="价格1" v-model="form.date1" style="width: 100%;"></el-input>
				</el-col>
				<el-col class="line" :span="2"></el-col>
				<el-col :span="11">
					<el-input placeholder="价格2" v-model="form.date2" style="width: 100%;"></el-input>
				</el-col>
			</el-form-item>
			<el-form-item>
				<el-dropdown>
					<el-button type="primary">
						隐含波动率区间1<i class="el-icon-caret-bottom el-icon--right"></i>
					</el-button>
					<el-dropdown-menu slot="dropdown">
						<el-dropdown-item>黄金糕</el-dropdown-item>
					</el-dropdown-menu>
				</el-dropdown>
			</el-form-item>
			<el-form-item>
				<el-dropdown>
					<el-button type="primary">
						隐含波动率区间2<i class="el-icon-caret-bottom el-icon--right"></i>
					</el-button>
					<el-dropdown-menu slot="dropdown">
						<el-dropdown-item>黄金糕</el-dropdown-item>
					</el-dropdown-menu>
				</el-dropdown>
			</el-form-item>
			<el-form-item>
				<el-dropdown>
					<el-button type="primary">
						隐含波动率区间3<i class="el-icon-caret-bottom el-icon--right"></i>
					</el-button>
					<el-dropdown-menu slot="dropdown">
						<el-dropdown-item>黄金糕</el-dropdown-item>
					</el-dropdown-menu>
				</el-dropdown>
			</el-form-item>
			<el-form-item>
				<el-button type="primary" @click="onSubmit">进行策略套利</el-button>
			</el-form-item>

			<el-form-item label="输出结果">
				<el-input type="textarea" v-model="form.desc"></el-input>
			</el-form-item>


		</el-form>

</el-card>
</el-col>






<el-col :span="4">
	<el-card class="box-card">
		<div slot="header" class="clearfix">
			<span style="line-height: 36px;">策略列表</span>
			<el-button style="float: right;" type="primary">操作按钮</el-button>
		</div>
		<div v-for="o in 10" :key="o" class="text item">
			{{'列表内容 ' + o }}
		</div>
	</el-card>
</el-col>
</el-row>
</section>
</div>
</template>

<script>

	export default{
		data(){
			return{
				tableData: [{
            date: '2016-05-02',
            name: '王小虎',
            address: '上海市普陀区金沙江路 1518 弄'
          }, {
            date: '2016-05-04',
            name: '王小虎',
            address: '上海市普陀区金沙江路 1517 弄'
          }, {
            date: '2016-05-01',
            name: '王小虎',
            address: '上海市普陀区金沙江路 1519 弄'
          }, {
            date: '2016-05-03',
            name: '王小虎',
            address: '上海市普陀区金沙江路 1516 弄'
          }],
          form: {


          }



		}
	}
}

</script>

<style>
</style>