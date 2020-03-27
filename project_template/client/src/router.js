import Vue from "vue";

import Router from "vue-router";

import store from "./store";

Vue.use(Router);

const router = new Router({
  // mode: 'history',
  routes: [
    {
      path: "/",
      redirect: "/home"
    },
    {
      path: "/login",
      name: "login",
      component: () => import("./views/Login.vue")
    },
    {
      path: "/home",
      name: "home",
      component: () => import("./views/Home.vue")
    }
  ],
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    } else {
      return { x: 0, y: 0 };
    }
  }
});

const whiteList = ["/login"];

router.beforeEach((to, from, next) => {
  let token = store.getters.token;
  if (token) {
    if (to.path === "/login") {
      // 如果登录过，直接跳转到首页
      next({ path: "/" });
    } else {
      next();
    }
  } else {
    if (whiteList.indexOf(to.path) !== -1) {
      next();
    } else {
      next({ path: `/login` });
    }
  }
});

// 每次跳出之后清除定时任务
router.afterEach(() => {
  router.app.$store.commit("clearIntervals");
  router.app.$store.commit("clearTimeout");
});

export default router;
