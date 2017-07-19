import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

const homepage = r => require.ensure([], () => r(require('@/page/homepage')), 'homepage');
const register = r => require.ensure([], () => r(require('@/page/register')), 'register');
const login = r => require.ensure([], () => r(require('@/page/login')), 'login');
const use = r => require.ensure([], () => r(require('@/page/use')), 'use');
const carousel = r => require.ensure([], () => r(require('@/page/carousel')), 'carousel');
const productIntro = r => require.ensure([], () => r(require('@/page/productIntro')), 'productIntro');
const homepageSecond = r => require.ensure([], () => r(require('@/page/homepageSecond')), 'homepageSecond');
const option1 = r => require.ensure([], () => r(require('@/page/option1')), 'option1');
const homepageIndividual = r => require.ensure([], () => r(require('@/page/homepageIndividual')), 'homepageIndividual');
const infoIndividual = r => require.ensure([], () => r(require('@/page/infoIndividual')), 'infoIndividual');
const list = r => require.ensure([], () => r(require('@/page/list')), 'list');
const infoReminder = r => require.ensure([], () => r(require('@/page/infoReminder')), 'infoReminder');




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
		path: '/register',
		component: register,
		name: 'register'
	},{
		path: '/login',
		component: login,
		name: 'login'
	},{
		path: '/use',
		component: use,
		name: 'use'
	},{
		path: '/homepageIndividual',
		component: homepageIndividual,
		name: 'homepageIndividual',
		children:[{
			path: '',
			component: infoIndividual,
			name: 'infoIndividual'
		},{
			path: '/homepageIndividual/list',
			component: list,
			name: 'list'
		},{
			path: '/homepageIndividual/infoReminder',
			component: infoReminder,
			name: 'infoReminder'
		},{
			path: '/homepageIndividual/infoIndividual',
			component: infoIndividual,
			name: 'infoIndividual'
		}
		]
	},{
		path: '/productIntro',
		component: productIntro,
		name: 'productIntro',
		children: [
		{
			path: '',
			component: option1,
			name: 'option1'
		},
		{
			path: '/option1',
			component: option1,
			name: 'option1'
		},
		{
			path: '/homepageSecond',
			component: homepageSecond,
			name: 'homepageSecond'
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

