<template>
<div>
	<div>
	  <input v-model="parentMsg">
	  <br>
	  <child v-bind:message="parentMsg"></child>
	</div>
</div>
</template>

<script>

	export default{


		data() { 
			return{
	hasError: true,
	name: 'Vue.js',
	checked: false,
	parentMsg: '父组件内容'

		}
	},

	methods:{
		greet: function(event){
			alert('Hello ' + this.name + '!')
			if(event){
			alert(event.target.tagName)
		}
		}
	}
}

</script>

<style>

.active {
	width: 100px;
	height: 100px;
	background: green;
}
.text-danger {
	background: red;
}

</style>