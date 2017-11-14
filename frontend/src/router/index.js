import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)
//中文版
const homepage = r => require.ensure([], () => r(require('@/pageCH/homepage')), 'homepage');
const register = r => require.ensure([], () => r(require('@/pageCH/register')), 'register');
const login = r => require.ensure([], () => r(require('@/pageCH/login')), 'login');
const use = r => require.ensure([], () => r(require('@/pageCH/use')), 'use');
const carousel = r => require.ensure([], () => r(require('@/pageCH/carousel')), 'carousel');
const productIntro = r => require.ensure([], () => r(require('@/pageCH/productIntro')), 'productIntro');
const homepageSecond = r => require.ensure([], () => r(require('@/pageCH/homepageSecond')), 'homepageSecond');
const option1 = r => require.ensure([], () => r(require('@/pageCH/option1')), 'option1');
const homepageIndividual = r => require.ensure([], () => r(require('@/pageCH/homepageIndividual')), 'homepageIndividual');
const infoIndividual = r => require.ensure([], () => r(require('@/pageCH/infoIndividual')), 'infoIndividual');
const list = r => require.ensure([], () => r(require('@/pageCH/list')), 'list');
const infoReminder = r => require.ensure([], () => r(require('@/pageCH/infoReminder')), 'infoReminder');
const beanGroup = r => require.ensure([], () => r(require('@/pageCH/beanGroup')), 'beanGroup');
const crop = r => require.ensure([], () => r(require('@/pageCH/crop')), 'crop');
const assess = r => require.ensure([], () => r(require('@/pageCH/assess')), 'assess');
const calculator = r => require.ensure([], () => r(require('@/pageCH/calculator')), 'calculator');
//
//英文版
const homepage_en = r => require.ensure([], () => r(require('@/pageEN/homepage')), 'homepage_en');
const register_en = r => require.ensure([], () => r(require('@/pageEN/register')), 'register_en');
const login_en = r => require.ensure([], () => r(require('@/pageEN/login')), 'login_en');
const use_en = r => require.ensure([], () => r(require('@/pageEN/use')), 'use_en');
const carousel_en = r => require.ensure([], () => r(require('@/pageEN/carousel')), 'carousel_en');
const productIntro_en = r => require.ensure([], () => r(require('@/pageEN/productIntro')), 'productIntro_en');
const homepageSecond_en = r => require.ensure([], () => r(require('@/pageEN/homepageSecond')), 'homepageSecond_en');
const option1_en = r => require.ensure([], () => r(require('@/pageEN/option1')), 'option1_en');
const homepageIndividual_en = r => require.ensure([], () => r(require('@/pageEN/homepageIndividual')), 'homepageIndividual_en');
const infoIndividual_en = r => require.ensure([], () => r(require('@/pageEN/infoIndividual')), 'infoIndividual_en');
const list_en = r => require.ensure([], () => r(require('@/pageEN/list')), 'list');
const infoReminder_en = r => require.ensure([], () => r(require('@/pageEN/infoReminder')), 'infoReminder_en');
const beanGroup_en = r => require.ensure([], () => r(require('@/pageEN/beanGroup')), 'beanGroup_en');
const crop_en = r => require.ensure([], () => r(require('@/pageEN/crop')), 'crop_en');
const assess_en = r => require.ensure([], () => r(require('@/pageEN/assess')), 'assess_en');
const calculator_en = r => require.ensure([], () => r(require('@/pageEN/calculator')), 'calculator_en');
//
const routes = [
{
	// mode: 'history',
	path: '/',
	component: homepage,
	name: 'homepage',
	alias:'/zh-cn',
	children: [
	{
		path: '',
		component: carousel,
		name: 'carousel'
	},
	{
		path: '/zh-cn/register',
		component: register,
		name: 'register'
	},{
		path: '/zh-cn/login',
		component: login,
		name: 'login'
	},{
		path: '/zh-cn/use',
		component: use,
		name: 'use'
	},{
		path: '/zh-cn/homepageIndividual',
		component: homepageIndividual,
		name: 'homepageIndividual',
		children:[{
			path: '',
			component: infoIndividual,
			name: 'infoIndividual'
		},{
			path: '/zh-cn/homepageIndividual/list',
			component: list,
			name: 'list'
		},{
			path: '/zh-cn/homepageIndividual/infoReminder',
			component: infoReminder,
			name: 'infoReminder'
		},{
			path: '/zh-cn/homepageIndividual/infoIndividual',
			component: infoIndividual,
			name: 'infoIndividual'
		}
		]
	},{
		path: '/zh-cn/productIntro',
		component: productIntro,
		name: 'productIntro',
		children: [
		{
			path: '',
			component: option1,
			name: 'option1'
		},
		{
			path: '/zh-cn/option1',
			component: option1,
			name: 'option1'
		},
		{
			path: '/zh-cn/homepageSecond',
			component: homepageSecond,
			name: 'homepageSecond'
		}
		]
	},{
		path: '/zh-cn/beanGroup',
		component: beanGroup,
		name: 'beanGroup',
	},{
		path: '/zh-cn/crop',
		component: crop,
		name: 'crop',
	},{
		path: '/zh-cn/assess',
		component: assess,
		name: 'assess',
	},{
		path: '/zh-cn/calculator',
		component: calculator,
		name: 'calculator',
	},

	]
},
{
	// mode: 'history',
	path: '/en',
	component: homepage_en,
	name: 'homepage_en',
	children: [
	{
		path: '',
		component: carousel_en,
		name: 'carousel_en'
	},
	{
		path: '/en/register',
		component: register_en,
		name: 'register_en'
	},{
		path: '/en/login',
		component: login_en,
		name: 'login_en'
	},{
		path: '/en/use',
		component: use_en,
		name: 'use_en'
	},{
		path: '/en/homepageIndividual',
		component: homepageIndividual_en,
		name: 'homepageIndividual_en',
		children:[{
			path: '',
			component: infoIndividual_en,
			name: 'infoIndividual_en'
		},{
			path: '/en/homepageIndividual/list',
			component: list_en,
			name: 'list_en'
		},{
			path: '/en/homepageIndividual/infoReminder',
			component: infoReminder_en,
			name: 'infoReminder_en'
		},{
			path: '/en/homepageIndividual/infoIndividual',
			component: infoIndividual_en,
			name: 'infoIndividual_en'
		}
		]
	},{
		path: '/en/productIntro',
		component: productIntro_en,
		name: 'productIntro_en',
		children: [
		{
			path: '',
			component: option1_en,
			name: 'option1_en'
		},
		{
			path: '/en/productIntro/option1',
			component: option1_en,
			name: 'option1_en'
		},
		{
			path: '/en/productIntro/homepageSecond',
			component: homepageSecond_en,
			name: 'homepageSecond_en'
		}
		]
	},{
		path: '/en/beanGroup',
		component: beanGroup_en,
		name: 'beanGroup_en',
	},{
		path: '/en/crop',
		component: crop_en,
		name: 'crop_en',
	},{
		path: '/en/assess',
		component: assess_en,
		name: 'assess_en',
	},{
		path: '/en/calculator',
		component: calculator_en,
		name: 'calculator_en',
	},

	]
}
]


export default new Router({
	routes
})

