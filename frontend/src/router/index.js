import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

const homepage = r => require.ensure([], () => r(require('@/page/homepage')), 'homepage');
const login = r => require.ensure([], () => r(require('@/page/login')), 'login');
const use = r => require.ensure([], () => r(require('@/page/use')), 'use');
const carousel = r => require.ensure([], () => r(require('@/page/carousel')), 'carousel');
const productIntro = r => require.ensure([], () => r(require('@/page/productIntro')), 'productIntro');
const homepageSecond = r => require.ensure([], () => r(require('@/page/homepageSecond')), 'homepageSecond');
const option1 = r => require.ensure([], () => r(require('@/page/option1')), 'option1');




const routes = [
{
	// mode: 'history',
	path: '/',
	component: homepage,
	name: 'homepage',
	children: [
	{
		path: '',
		component: carousel,
		name: 'carousel'
	},
	{
		path: '/login',
		component: login,
		name: 'login'
	},{
		path: '/use',
		component: use,
		name: 'use'
	},{
		path: '/productIntro',
		component: productIntro,
		name: 'productIntro',
		children: [
		{
			path: '',
			component: homepageSecond,
			name: 'homepageSecond'
		},
		{
			path: '/option1',
			component: option1,
			name: 'option1'
		}
		]
	}
	]
}
]


export default new Router({
	mode:'history',
	routes
})

