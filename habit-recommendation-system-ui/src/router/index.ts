import { createRouter, createWebHistory } from "vue-router";
import DonateHabit from "../pages/DonateHabit.vue";
import ManageHabits from "../pages/ManageHabits.vue";
import HealthProfile from "../pages/HealthProfile.vue";

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", redirect: "/donate" },
    { path: "/donate", component: DonateHabit },
    { path: "/manage", component: ManageHabits },
    { path: "/profile", component: HealthProfile },
  ],
});
