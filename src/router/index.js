import Vue from 'vue'
import Router from 'vue-router'
import Tasks from '../components/Tasks.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/task',
      component: Tasks,
    },
  ],
});
