import {
    createRouter,
    createWebHashHistory
} from "vue-router"

const routes = [{ // login
    path: '/',
    name: 'login',
    component: () => import( /*webpackChunkName:'Login'*/ '@/page/login/login.vue')
},
{
    path: '/index',
    name: 'index',
    meta: {
        title: 'summary'
    },
    component: () => import( /*webpackChunkName:'Index'*/ '@/page/index/index.vue'),
    children: [
        {
            path: '/reports',
            name: 'reports',
            meta: {
                title: 'reports'
            },
            component: () => import( /*webpackChunkName:'Reports'*/ '@/page/report/report.vue')
        },
        {
            path: '/users',
            name: 'users',
            meta: {
                title: 'users'
            },
            component: () => import( /*webpackChunkName:'Users'*/ '@/page/user/user.vue')
        }
    ]
}
]

const router = createRouter({
    history: createWebHashHistory(),
    routes
})

router.beforeEach((to, from, next) => {
    if (to.path == '/') {
        next()
    } else {
        const token = window.sessionStorage.getItem('token')
        if (!token) {
            next('/')
        } else {
            next()
        }
    }
})

export default router