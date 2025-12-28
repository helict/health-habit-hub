import { createRouter, createWebHistory } from "vue-router";
import DonateHabit from "../pages/DonateHabit.vue";
import ManageHabits from "../pages/ManageHabits.vue";

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", redirect: "/donate" },
    { path: "/donate", component: DonateHabit },
    { path: "/manage", component: ManageHabits },
  ],
});
