<template>
	<div class="container">
		<div class="wrapper" v-for="combo in combos">
			<div class="kind">
				<span>期货品种</span>
				<el-select v-model="combo.future" class="sel">
					<el-option
					v-for="item in futures"
					:key="item"
					:label="item"
					:value="item"/>
				</el-select>
			</div>
			<span>期货持仓</span>
			<el-input class="inp" v-model="combo.hold"/>
		</div>
		<el-button type="warning" @click="add">+</el-button>
	</div>
</template>

<script>
	export default {
		data() {
			return {
				futures: ['A', 'B', 'C', 'D'],
				combos: []
			};
		},
		methods: {
			add: function() {
				this.combos.push({'future': null, 'hold': 0})
			}
		}
	}
</script>

<style>
	.container {
		padding-top: 10px;
		padding-bottom: 10px;
		padding-left: 10px;
		width: 300px;
		height: 500px;
		border-radius: 5px;
		border: 2px solid #2C2E3B;
		overflow: auto;
		background-color: #e4e4e4;
	}
	.wrapper {
		width: 280px;
		padding: 5px;
		border-radius: 5px;
		border: 1px solid #bababd;
		background-color: white;
		margin-bottom: 10px;
	}
	.kind {
		margin-bottom: 5px;
	}
	.sel {
		margin-left: 18px;
		width: 190px;
	}
	.inp {
		margin-left: 18px;
		width: 190px;
	}
</style>