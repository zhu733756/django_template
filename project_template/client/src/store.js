import Vue from "vue";

import Vuex from "vuex";

import VuexPersist from "vuex-persist";

Vue.use(Vuex);

const vuexPersist = new VuexPersist({
  key: "XmnCms",
  storage: localStorage
});

export default new Vuex.Store({
  state: {
    lang: "zh",
    auth: {
      user: null,
      token: null
    },
    color: {
      primary: "#35CBAA",
      success: "#35CBAA",
      warning: "#F6B93D",
      danger: "#EF6372",
      error: "#EF6372",
      info: "#60BCFE"
    },
    timeout: null,
    intervals: [],
    dateFormat: "yyyy-MM-dd hh:mm:ss",
    url: {
      user: {
        auth: "api/user/auth"
      },
      util: {
       
      },
    }
  },
  mutations: {
    setLang(state, lang) {
      state.lang = lang;
    },
    // auth
    setToken(state, token) {
      state.auth.token = token;
    },
    clearToken(state) {
      state.auth.token = null;
    },
    // user
    setUser(state, user) {
      state.auth.user = user;
    },
    clearUser(state) {
      state.auth.user = null;
    },
    // timeout
    setTimeout: (state, timeout) => {
      if (state.timeout) {
        clearTimeout(state.timeout);
      }
      state.timeout = timeout;
    },
    clearTimeout: state => {
      clearTimeout(state.timeout);
    },
    addInterval: (state, interval) => {
      state.intervals.push(interval);
    },
    clearIntervals: state => {
      state.intervals.forEach(interval => {
        clearInterval(interval);
      });
      state.intervals = [];
    },
  },
  getters: {
    token: state => {
      return state.auth.token;
    },
    user: state => {
      return state.auth.user;
    }
  },
  plugins: [vuexPersist.plugin],
});
